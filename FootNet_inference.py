# -*- coding: utf-8 -*-
"""
Process lower limb kinematc data in the required format (see repo for details) 
and predict foot-strike and toe-off events. 

--datapath flag - Optional. Path to directory .mat files. This should either be
                    a path to the directory or the path to a single file. Defaults
                    to repo file structure.

--samplingfreq flag - Optional (but required). Set to 0 by default so it crashes 
                        and users make sure they input it.

--model flag - Optional. Path to directory containing the FootNet model file. 
                Defaults to repo file structure.

Usage:
python3 FootNet_inference.py --datapath /path/to/data/file.mat --samplingfreq float --model path/to/modelfile
For help on arguments run: 
python3 FootNet_inference.py --help
"""

#%% Imports

import os
import scipy.io
import numpy as np
import tensorflow as tf
import argparse

#%% Helper functions

def pre_processor(data, sampling_freq=200):
    """
    This function pre-processes the input features needed to implement FootNet.
    It takes data, an object resulting from loading a matfile using loadmat and 
    extracts the ant-post distal tibia displacement, ankle dorsi-plantar flex angle, 
    and foot com ant-post and vertical displacememnt. Linear velocities are computed by
    calculating the numerical gradient of displacement using 1/sampling_freq as dt
    for the linear variables and then ant-post distal tibia displacement, ankle dorsi-
    plantar flex angle, foot vertical vel and foot ant-post vel are stacked as a 
    1 x timepoints x 4 array. These arrays are returned in a list trial_cycles and 
    a side reference sideref is also returned to keep track of left and right strides.
    """
    # Unpack data from .mat file
    if 'rtib_dist' in data.keys() and 'ltib_dist' not in data.keys():
        tib_dist = data['rtib_dist']
        ank_angle = data['rank']
        foot_com = data['rfoot_com']
        sideref = ['r'] * tib_dist.size
    elif 'ltib_dist' in data.keys() and 'rtib_dist' not in data.keys():
        tib_dist = data['ltib_dist']
        ank_angle = data['lank']
        foot_com = data['lfoot_com']
        sideref = ['l'] * tib_dist.size
    elif 'ltib_dist' in data.keys() and 'rtib_dist' in data.keys():
        tib_dist = np.hstack((data['rtib_dist'], data['ltib_dist']))
        ank_angle = np.hstack((data['rank'], data['lank']))
        foot_com = np.hstack((data['rfoot_com'], data['lfoot_com']))
        sideref = ['r'] * data['rtib_dist'].size
        sideref += ['l'] * data['ltib_dist'].size
    
    # Generate input variables for FootNet
    trial_cycles = []

    for stri in range(tib_dist.shape[1]):
        
        # Distal tibia anteroposterior velocity
        disttib_ap_vel = np.gradient(tib_dist[0, stri][:,1],(1/sampling_freq), axis=0) 
        
        # Ankle dorsi/plantarflex
        ank_dpflex = ank_angle[0, stri][:,0]                                              
        
        # Foot com vertical velocity
        foot_v_vel = np.gradient(foot_com[0, stri][:,2],(1/sampling_freq), axis=0) 
        
        # Foot anteroposterior velocity
        foot_ap_vel = np.gradient(foot_com[0, stri][:,1],(1/sampling_freq), axis=0) 

        # Stack the input features for cycle number stri
        input_features = np.vstack((disttib_ap_vel, ank_dpflex, foot_v_vel, foot_ap_vel)).T
        
        # Reshape input features to (stride x data x features) array and stack them
        t_points = max(np.shape(tib_dist[0, stri]))
        trial_cycles.append(np.reshape(input_features, (1, t_points ,4)))

    return trial_cycles, sideref

def predict_events(input_cycles, model_obj):
    """
    This function uses model_obj to predict the contact phase given 
    input_cycles. It then finds the first and last points of the predicted 
    contact phase and outputs them as foot strike and toe off.
        
    INPUT
        
    input_cycles. raw, not standardised input features required by model_obj 
    to make predictions. they should be organised as a ndarray of shape
    cycle x datapoints x features or in a list of such ndarrays.
    model_obj. FootNet model object
        
    OUTPUT
            
    foot_strike. first timepoint predicted as contact
    toe_off. last timepoint predicted as contact
    contact_phase. entire predicted label vector
    """
    
    # Get standardisation parameters to standardise input data
    zero_mean = model_obj._zero_mean.numpy()
    one_std = model_obj._one_std.numpy()
    
    # if input is not a list, get it into one
    if not isinstance(input_cycles, list):
        input_cycles = [input_cycles]
    
    # initialise vars
    contact = []
    foot_strike = []
    toe_off = []
    
    for cycle in input_cycles:
    
        # Standardise data
        stdised_cycle = (cycle - zero_mean) / one_std
        
        # Predict contact phase and find onset and offset
        y_hat = model_obj.predict(stdised_cycle)
        onset = np.where(y_hat[0,:,0] >= 0.5)[0][0]
        offset = np.where(y_hat[0,onset:,0] < 0.5)[0][0] - 1 + onset
        
        # Append to vars
        contact.append(y_hat)
        foot_strike.append(onset)
        toe_off.append(offset)

    return foot_strike, toe_off, contact

def data_writer(foot_strike_hat, toe_off_hat, contact_hat, sideref, inputfilename):
    """
    Writes out foot_strike_hat, toe_off_hat, contact_hat and sideref as a .mat
    file with inputfilename without extension as filename, adding _contact_events
    """
    # Create outputfilename
    outputfilename = os.path.splitext(inputfilename)[0]
    outputfilename += '_contact_events.mat'    

    # Reshape contact_hat and store them in a dict
    predictions = {}
    for stride in range(len(contact_hat)):
        predictions[sideref[stride]+str(stride)] = np.reshape(contact_hat[stride],(max(np.shape(contact_hat[stride])),1))
    
    # Write dict containing the desired output
    outputdic = {}
    outputdic['predictions'] = predictions
    outputdic['fs'] = foot_strike_hat
    outputdic['to'] = toe_off_hat
    outputdic['sideref'] = sideref

    # Save it as .mat file
    scipy.io.savemat(outputfilename, outputdic)

def main():

    # set up argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-p,", "--datapath", type=str,
                    default="./data",
                    help="path to kinematic data directory")
    ap.add_argument("-sf", "--samplingfreq", required=True, type=float,
                    default=0, help="motion capture sampling frquency")
    ap.add_argument("-m,", "--model", type=str,
                    default="./models/FootNetFinalModel",
                    help="path to tf model")
    args = vars(ap.parse_args())

    # Load model
    print(f"Loading model...")
    FootNet = tf.keras.models.load_model(args['model'])

    # Check if datapath is single file or directory.
    if args['datapath'].endswith(".mat"):
        # Generate processing list
        proc_list = [args['datapath']]
    else:
        # Generate processing list
        proc_list = [os.path.join(args['datapath'], f) for f in os.listdir(args['datapath']) if f.endswith('.mat')]
        # Ignore contact events files that already exist in the directory
        proc_list = [matfile for matfile in proc_list if '_contact_events.mat' not in matfile]

    # Iterate over each file in processing list
    for file in proc_list:
        # Load file
        print(f"Processing: {file}")
        data = scipy.io.loadmat(file)

        # Pre-process data
        trial_cycles, side_ref = pre_processor(data, args['samplingfreq'])

        # predict ground contact events
        foot_strike_hat, toe_off_hat, contact_hat = predict_events(trial_cycles, FootNet)

        # Write results to disk
        data_writer(foot_strike_hat, toe_off_hat, contact_hat, side_ref, file)

    print("Processing complete!")
#%% Call main

if __name__ == "__main__":
    main()
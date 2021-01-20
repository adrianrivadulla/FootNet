# -*- coding: utf-8 -*-
"""
Process lower limb kinematic data and predict foot-strike and toe-off events. 
The input data must be contained as Matlab cells (1 x n) where n is the number 
of gait cycles and contains a matrix of shape datapoints x xyzcoord, where 
xyzcoord are either med-lat, ant-post, vert for linear kinematics or flex/ext,
abd/add and int/ext rotation for joint kinematics. Variables must be named 
following the convention: rtib_dist, ltib_dist, rank, lank, rfoot_com, lfoot_com.
The script is able to deal with features from just one side (right or left) 
or both.

The input features needed for FootNet are:
    
    distal tibia anteroposterior velocity
    ankle dorsi-plantar flexion
    foot vertical velocity
    foot anteroposterior velocity
    
But linear velocities are calculated internally so provide distal tibia and foot
com displacments.

For each cycle, these features must be organised in a ndarray to be fed into
FootNet with shape cycle x datapoints x features.

FootNet is contained in the helper function predictContactEvents. This function
takes the raw input features and performs the standardisation internally for 
convenience, predicts the contact phase within the cycle and then outputs foot 
strike, toe off and the entire predicted label vector.
is the number os strides in the file. 

INPUT

--samplingfreq flag - Optional. Default = 200 Hz

--datapath flag - Optional. Path to directory .mat files. This should either be
                    a path to the directory or the path to a single file. Defaults
                    to repo file structure.

--model flag - Optional. Path to directory containing the FootNet model file. 
                Defaults to repo file structure.

--output flag - Optional. Path to directory where results will be saved. 
                Defaults to input data directory.

OUTPUT

-- foot-strike, toe-off indices and full prediction time-series are saved in a .mat
file with the same name as the input file in the output directory.

Usage:
python3 FootNet_inference.py --datapath /path/to/data/file.mat --samplingfreq float --model path/to/modelfile --output path/to/save/location
For help on arguments run: 
python3 FootNet_inference.py --help

Authors: Adrian R Rivadulla and Laurie Needham

"""

#%% Imports

import os
import scipy.io
import numpy as np
import tensorflow as tf
import argparse

#%% Helper functions

def pre_processor(data, sampling_freq):
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

def data_writer(foot_strike_hat, toe_off_hat, contact_hat, sideref, inputfilename, outputdir):
    """
    Writes out foot_strike_hat, toe_off_hat, contact_hat and sideref as a .mat
    file with inputfilename without extension as filename, adding _contact_events
    """
    # Check outputdir provided
    if os.path.isdir(outputdir):
        # write full path to file in outputdir
        outputfilename = os.path.basename(inputfilename)
        outputfilename = os.path.splitext(outputfilename)[0]
        outputfilename += '_contact_events.mat'
        outputfilename = os.path.join(outputdir, outputfilename) 
    
    elif outputdir == 'write_me':
        # write full path to inputfiledir
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
                    help="path to kinematic data directory. default=./data")
    ap.add_argument("-sf", "--samplingfreq", required=True, type=float,
                    default=200, help="motion capture sampling frequency. default=200")
    ap.add_argument("-m,", "--model", type=str,
                    default="./models/FootNet_v1",
                    help="path to tf model. default=./models/FootNet_v1")
    ap.add_argument("-o", "--output", type=str,
                    default="write_me",
                    help="path to output directory. default=write_me")
    args = vars(ap.parse_args())

    # Load model
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
        
        # Let user know what's going on
        f'Processing {file}...'

        # Load file        
        data = scipy.io.loadmat(file)

        # Pre-process data
        trial_cycles, side_ref = pre_processor(data, args['samplingfreq'])

        # predict ground contact events
        foot_strike_hat, toe_off_hat, contact_hat = predict_events(trial_cycles, FootNet)

        # Write results to disk
        data_writer(foot_strike_hat, toe_off_hat, contact_hat, side_ref, file, args['output'])

#%% Call main

if __name__ == "__main__":
    main()
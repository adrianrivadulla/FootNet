# -*- coding: utf-8 -*-
"""
This script demonstrates how to use FootNet to detect foot strike and toe off.
An example data file (Data_example.mat) containing segment and joint 
kinematics chopped in gait cycles is provided to implement it. The kinematic 
variables are contained in Matlab cells, where each cell is a gait cycle and 
contains a matrix of shape datapoints x xyzcoord, where xyzcoord are 
either med-lat, ant-post, vert for linear kinematics or flex/ext, abd/add and
int/ext rotation for joint kinematics.

The input features needed for FootNet are:
    
    distal tibia anteroposterior velocity
    ankle dorsi-plantar flexion
    foot vertical velocity
    foot anteroposterior velocity
    
The example file provides positions so linear velocities must be calculated.

For each cycle, these features must be organised in a ndarray to be fed into
FootNet with shape cycle x datapoints x features. 

FootNet is contained in the helper function predictContactEvents. This function
takes the raw input features and performs the standardisation internally for 
convenience, predicts the contact phase within the cycle and then outputs foot 
strike, toe off and the entire predicted label vector.

The example file also contains vertical ground reaction forces and the target
label vector so you can compare your results against the gold standard for this
particular file.

Created on Wed Dec  9 13:51:54 2020

@author: arr43

FootNet_inference.py

Process lower limb kinematc data in the required format (see repo for details) 
and predcit foot-strike and toe-off events. 

--datapath flag - Optional. Path to directory .mat files. This should either be
                    a path to the directory or the path to a single file. Defaults
                    to repo file structure.

--model flag - Optional. Path to directory containing the FootNet model file. 
                Defaults to repo file structure.

--output flag - Optional. Path to directory where results will be saved. 
                Defaults to repo file structure.

Usage:
python3 FootNet_inference.py --datapath /path/to/data/file.mat --model path/to/modelfile --output path/to/save/location
For help on arguments run: 
python3 FootNet_inference.py --help
"""


import os
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import argparse

def pre_processor(data, sampling_freq=200):

    # Unpack data from .mat file
    tib_dist = np.hstack((data['rtib_dist'], data['ltib_dist']))
    ank_angle = np.hstack((data['rank'], data['lank']))
    foot_com = np.hstack((data['rfoot_com'], data['lfoot_com']))

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

        return trial_cycles

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
    contact_phase. entire predicted label
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

def data_writer(foot_strike_hat, toe_off_hat, contact_hat, file):
    pass

def main():

    # set up argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-p,", "--datapath", required=True, type=str,
                    default="./data",
                    help="path to kinematic data directory")
    ap.add_argument("-m,", "--model", type=str,
                    default="./models/FootNetFinalModel",
                    help="path to tf model")
    ap.add_argument("-o", "--output", type=str,
                    default="./output/",
                    help="path to output directory")
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

    # Iterate over each file in processing list
    for file in proc_list:
        # Load file
        data = loadmat(file)

        # Pre-process data
        trial_cycles = pre_processor(data)

        # predict ground contact events
        foot_strike_hat, toe_off_hat, contact_hat = predict_events(trial_cycles, FootNet)

        # Write results to disk
        data_writer(foot_strike_hat, toe_off_hat, contact_hat, file)

if __name__ == "__main__":
    main()
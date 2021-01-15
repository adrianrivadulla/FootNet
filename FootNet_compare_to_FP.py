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
"""


import os
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from FootNet_inference import pre_processor, predict_events


def compare(data, foot_strike_hat, toe_off_hat, contact_hat):

    Y_labels = np.hstack((data['rlabels'], data['llabels']))
    foot_strike_true = []
    toe_off_true = []

    for stri in range(Y_labels.shape[1]):
    
        onset = np.where(Y_labels[0,stri][0,:] >= 0.5)[0][0]
        offset = np.where(Y_labels[0,stri][0,onset:] < 0.5)[0][0] - 1 + onset
        
        foot_strike_true.append(onset)
        toe_off_true.append(offset)

    foot_strike_error = np.asarray(foot_strike_true) - np.asarray(foot_strike_hat)
    toe_off_error = np.asarray(toe_off_true) - np.asarray(toe_off_hat)

    plt.figure()

    # Subplot 1. histogram of foot strike error
    plt.subplot(3,1,1)
    labels, counts = np.unique(foot_strike_error, return_counts=True)
    plt.bar(labels, counts, align='center')
    plt.xticks(np.linspace(-5,5,11))
    plt.title('Foot strike error')
    plt.ylabel('Count')
    plt.xlabel('Error (frames)')

    # Subplot 2. histogram of toe off error
    plt.subplot(3,1,2)
    labels, counts = np.unique(toe_off_error, return_counts=True)
    plt.bar(labels, counts, align='center')
    plt.xticks(np.linspace(-5,5,11))
    plt.title('Toe off error')
    plt.ylabel('Count')
    plt.xlabel('Error (frames)')
        
    # Subplot 3. Random case for visualisation
    sel_cycle = int(np.random.randint(low=0, high=len(trial_cycles), size=1))
    plt.subplot(3,1,3)
    plt.plot(Y_labels[0,sel_cycle][:].T,'g')
    plt.plot(contact_hat[sel_cycle][0,:,0],'b')
    plt.legend('Ground truth', 'Predicted')
    plt.title('Ground truth vs predicted')
    plt.ylabel('Label')
    plt.xlabel('Timepoint')

    plt.tight_layout()
    plt.show()

#%% Load data
modeldir = './models/FootNetFinalModel'
data = loadmat('./data/Data_example.mat')

# Load file
data = scipy.io.loadmat(file)

# Pre-process data
trial_cycles, side_ref = pre_processor(data)

# predict ground contact events
foot_strike_hat, toe_off_hat, contact_hat = predict_events(trial_cycles, FootNet)

# Compare to gold standard
compare(data, foot_strike_hat, toe_off_hat, contact_hat)


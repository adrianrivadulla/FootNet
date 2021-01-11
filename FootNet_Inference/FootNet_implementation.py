# -*- coding: utf-8 -*-
"""
This script demonstrates how to use FootNet to detect foot strike and toe off.
An example data file (Data_example.mat) containing segment and joint 
kinematics chopped in gait cycles is provided to implement it. The kinematic 
variable are contained in matlab cells, where each cell is a gait cycle and 
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
#%% Pre-settings

# Make imports

import os
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Helper fuctions

def predictContactEvents(input_cycles, model_obj):
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

#%% Load data

my_own_path = __file__
rootdir = os.path.dirname(my_own_path)
modeldir = rootdir + '/FootNetFinalModel'
data = loadmat(rootdir + '/Data_example.mat')                                                   

#%% Get input data

tib_dist = np.hstack((data['rtib_dist'], data['ltib_dist']))
ank_angle = np.hstack((data['rank'], data['lank']))
foot_com = np.hstack((data['rfoot_com'], data['lfoot_com']))

#%% Calculate and sort input features for FootNet

trial_cycles = []
sampling_freq = 200

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

#%% Predict contact phases using FootNet

# instantiate model
FootNet = tf.keras.models.load_model(modeldir)

foot_strike_hat, toe_off_hat, contact_hat = predictContactEvents(trial_cycles, FootNet)

#%% Compare to gold standard

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

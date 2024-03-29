# -*- coding: utf-8 -*-
"""
This script compares the step events detected by FootNet against those detected
using the vertical GRF. Data_example.mat file is  used for this comparison.
FootNet_inference.py is called in as a module and its functions are used to pre-
process the kinematic input features needed by FootNet, predict the contact phases
and detect foot-strike and toe-off. The example file also contains the original 
label vectors generated using the onset and offset of the vGRF. A graph is produced
to visualise the comparison between both methods.


Created on Wed Dec  9 13:51:54 2020

@author: arr43
"""

import os
import sys
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import FootNet_inference

# Load data
path = "./data/Data_example.mat"
data = loadmat(path)

# Load model
print("[INFO] - Loading tf model...")
FootNet = tf.keras.models.load_model("./models/FootNet_v1")

# Pre-process data
trial_cycles, side_ref = FootNet_inference.pre_processor(data, 200)

# Predict ground contact events
print(f"[INFO] - Processing Example Data: {path}")
foot_strike_hat, toe_off_hat, contact_hat = FootNet_inference.predict_events(trial_cycles, FootNet)

# Find foot-strike and toe-off in the labels generated using the vGRF data
Y_labels = np.hstack((data['rlabels'], data['llabels']))
foot_strike_true = []
toe_off_true = []

for stri in range(Y_labels.shape[1]):
   
    onset = np.where(Y_labels[0,stri][0,:] >= 0.5)[0][0]
    offset = np.where(Y_labels[0,stri][0,onset:] < 0.5)[0][0] - 1 + onset
    
    foot_strike_true.append(onset)
    toe_off_true.append(offset)

# Calculate the difference between true and predicted
foot_strike_error = np.asarray(foot_strike_true) - np.asarray(foot_strike_hat)
toe_off_error = np.asarray(toe_off_true) - np.asarray(toe_off_hat)

# Create figure
plt.figure()

# Subplot 1. histogram of foot strike error

plt.subplot(3,1,1)
labels, counts = np.unique(foot_strike_error, return_counts=True)
plt.bar(labels, counts, align='center')
plt.xticks(np.linspace(-5,5,11))
plt.title('Foot Strike Error Distribution')
plt.ylabel('Count')
plt.xlabel('Error (frames)')

# Subplot 2. histogram of toe off error

plt.subplot(3,1,2)
labels, counts = np.unique(toe_off_error, return_counts=True)
plt.bar(labels, counts, align='center')
plt.xticks(np.linspace(-5,5,11))
plt.title('Toe Off Error Distribution')
plt.ylabel('Count')
plt.xlabel('Error (frames)')

# Subplot 3. Random case for visualisation
sel_cycle = int(np.random.randint(low=0, high=len(trial_cycles), size=1))

plt.subplot(3,1,3)
plt.plot(Y_labels[0,sel_cycle][:].T, 'g', label="Ground Truth")
plt.plot(contact_hat[sel_cycle][0,:,0], 'b', label="Predicted")
plt.title('Example - Ground Truth vs Predicted')
plt.legend()
plt.ylabel('Label')
plt.xlabel('Timepoint')

plt.tight_layout()

# Save figure to output directory
plt.savefig("./output/FootNet_vs_FP_comparison.png")

print("[INFO] - Complete!")
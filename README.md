# Overview

Motion capture running analyses are oftentimes performed on convetional (non-instrumented) treadmills. The absence of force plates can be problematic for the detection of foot strike and toe off, which are critical for the comprehensive biomechanical analysis of running kinematics. In this study, we introduce FootNet an algorithm for the detection of foot strike and toe off events on non-instrumented treadmills using segment and joint kinematics as input. The algorithm is based on an LSTM neural network architecture that has been trained, validated and tested using five datasets collected in three different labs using different motion capture and treadmill systems. The datasets include athletes of different abilities and foot strikes running at a wide range of speeds, and under different gradient, fatigue, and shoe conditions. running conditions and foot tracking models.

This repository contains all the software developed for the data processing, cross validation and testing of FootNet as well as links to download the datasets used.

The pubication associated with this study can be found [here](link2pub).

## FootNet model

The model can be downloaded from [here](link). It has been developed using Tensorflow 2.3.0 on Python 3.6.9. Implementation of the model in Python is demonstated in Python_inference.py. The model can also be implemented in Matlab by importing the neural network's architecture and weights as demonstrated in the Matlab_inference.m script. 

## Study replication

The following sections provide further details about the data and sofware developed and how to replicate  our results (to the extent allowed by the random allocation methods used for training and testing data and the stochastic nature of neural networks). The code provided has been originally developed for use in Visual3D (v6), Matlab (2018b) and Python (3.7). Nevertheless, all the files output by each script are also provided, so users can focus on a specific part of their interest or replicate the parts their software allows. The most important part of the study i.e. FootNet development can be replicated using Google Colab, which is freely accessible to anyone who owns a Gmail account.

The data and software needed to replicate our results can be accessed [here](link2datasoftwareetc). The project directory is organised as follows:

  - StepDetectionStudy
    - Datasets
      - FootStrikes
        - S00n
          - motion files (.c3d) containing marker trajectories and groud reaction forces.
          - Visual3D pipeline (.v3s) to obtain segment and joint kinematics.
          - processed files (.mat) with segment and joint kineamtics and ground reaction forces as exported from Visual3D.
          - gait cycles (Chopped_\*.mat) identified using the highest position of the foot centre of mass.
          - accepted gain cycles (Features_\*.mat) after systematic check of ground reaction forces and visual check of segment and joint kinematics.
      - Speed
      - Footwear
      - Prolonged
      - Inclines
    - Software
      - Visual3D
        - model files (.mdh) for each dataset.
        - pipleine template (.v3s) for each dataset.
      - Dataset_Preparation.m. Script to create subject specific Visual3D pipelines and running them on Visual3D through Matlab. 
      - ContactEvents_Processing.m. Script to segment running trials in gait cycles, identification of contact phase, foot strike and toe off within each cycle, ground reaction force systematic check and segment and joint kinematics visual check.
      - Sensitivity_Analysis.m. Script to run the sensitivity analysis of hip, knee and ankle sagittal plane angles to error in the detection of foot strike and toe off.
      - TestResults_Analysis.m. Script to run Bland-Altman agreement analysis between FootNet and the gold standard method and correlation analysis between FootNet error and speed, foot angle at contact and ground gradient.
      - Dataset_Sorter.py. Script to calculate final input features for model development and to sort each datasets (individual .mat files for each trial) in a single "Python-friendly" .npy file containing a dictionary with the input features and target labels.
      
## Data

The datasets used in this study include ground reaction forces collected on an instrumented treadmill and three-dimensional marker trajectories collected using an optoelectronic motion capture system and have been gathered from previosly published running biomechanics research. The datasets have been named after the characteristics of the data collected as:

FootStrikes dataset: LINK
Inclines dataset: LINK
Speed dataset: LINK
Footwear: LINK
Prolonged dataset: LINK

Please note that FootStrikes and Inclines were already open access datasets retrieved from [here](link) and [here](link), and credit should go to the researchers leading the original projects. We just reshare their work organised conveniently for our study.

## Data processing

Biomechanical basic data processing steps including marker trajecotry filtering, rigid body segment model scaling, calculation of segment position and orientation, calculation of joint kinematics, ground reaction force baseline noise removal and filtering were performed in Visual3D. Visual3D pipelines for each individual to perform these steps are included. These subject-specific pipelines were automatically created based on a template and executed in Visual3D through Matlab using NameOfScript in Matlab. 

Following data processing steps including segmentation of running trials in gait cycles using the highest position of the foot centre of mass, ground reaction force and kinematics data quality assessment, identification of the contact phase using the vertical ground reaction force within each cycle and subsequent identification of foot strike and toe off were performed in Matlab using NameOfScript.

FootNet's architectue and development was completed in Python. NameOfScript Python script was used to gather the output files produced in the previous data processing steps, calculate segment linear velocities and save the input features, target labels, trial names and vertical ground reaction force vectors in a more "Python-friendly" format for FootNet development.

## FootNet development

FootNet cross validation and testing can be replicated on Google Colab. Firstly, you need to download the data and notebooks from [here](https://drive.google.com/drive/folders/1MMpsXvz8-rDjTwwfOrp_k7zS_Om1gqLy?usp=sharing) and add them to your Google drive. The root directory has the following structure:

  - StepDetectionStudy
    - Data
      - OriginalDatasets. Folder containing the entire datasets (.npy) files as Python dictionaries.
      - DataFolds.npy File containing the training data grouped in 5 folds.
      - TestingSet.npy File containing the testing set.
    - CrossValidation
      - Models. Folder containing the five models developed during cross validation.
      - Results. Folder containing the summary performance metrics for each model on its corresponding validation set and Bland-Altman plots comparing foot strike, toe off and contact times as predicted by FootNet vs gold standard method.
    - FinalTest
      - FootNet_bestCandidate. Best set of parameters resulting from cross validation
      - Summary performance metrics on testing set and Bland-Altman plots comparing foot strike, toe off and ocntact times as predicted by FootNet vs gold standard method.
      - y_and_yhat.mat File containing testing predictions, target labels and metadata from testing stride cycles for posterior analyses in Matlab presented in the paper.
    - TrainTest_Split.ipynb. This notebook demonstrates how the dataset splitting was performed, including training and testing (70/30) and further folding of training dataset in 5 folds.
    - CrossValidation.ipnyb. This notebook performs cross 5-fold cross validation.
    - FinalTest.ipnyb. This notebook updates the best candidate model resulting from cross validation with the 5 folds as training set and performs the final test on the testing set.

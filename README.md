# Overview

Motion capture running analyses are oftentimes performed on convetional (non-instrumented) treadmills. The absence of force plates can be problematic for the detection of foot strike and toe off, which are critical for the comprehensive biomechanical analysis of running kinematics. In this study, we developed FootNet an algorithm for the detection of foot strike and toe off events on non-instrumented treadmills using segment and joint kinematics as input. The algorithm is based on an LSTM neural network architecture that has been trained, validated and tested using five datasets collected in three different labs using different motion capture and treadmill systems. The datasets include athletes of different abilities and foot strikes running at a wide range of speeds, and under different gradient, fatigue, and shoe conditions. running conditions and foot tracking models.

This repository contains all the software developed for the data processing, cross validation and testing of FootNet as well as links to download the datasets used.

The pubication associated with this study can be found [here](link2pub).

The data and software needed to replicate our results can be accessed [here](link2datasoftwareetc).

The following sections provide further details about the data and sofware developed and how to use them.

## Data

The datasets used in this study include ground reaction forces collected on an instrumented treadmill and three-dimensional marker trajectories collected using an optoelectronic motion capture system and have been gathered from previosly published running biomechanics research. The datasets have been named after the characteristics of the data collected as:

FootStrikes dataset: LINK
Inclines dataset: LINK
Speed dataset: LINK
Footwear: LINK
Prolonged dataset: LINK

Please note that FootStrikes and Inclines were already open access datasets retrieved from here and here, and credit should go to the researchers leading the original projects. We just reshare their work organised conveniently for our study.

## Data processing

Biomechanical basic data processing steps including marker trajecotry filtering, rigid body segment model scaling, calculation of segment position and orientation, calculation of joint kinematics, ground reaction force baseline noise removal and filtering were performed in Visual3D. Visual3D pipelines for each individual to perform these steps are included and the way those individual pipelines were created based on pipeline templates can be replicated using NameOfScript in Matlab. 

Following data processing steps including segmentation of running trials in gait cycles using the highest position of the foot centre of mass, ground reaction force and kinematics data quality assessment, identification of the contact phase using the vertical ground reaction force within each cycle and subsequent identification of foot strike and toe off were performed in Matlab using NameOfScript.

FootNet's architectue and development was completed in Python. Hence, the Python script NameOfScript was used to gather the output files produced in the previous data processing steps, calculate segment linear velocities and save the input features, target labels, trial names and vertical ground reaction force vectors in a more "Python-friendly" format for FootNet development.

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

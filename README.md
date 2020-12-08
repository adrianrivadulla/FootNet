# FootNet_Development

Motion capture running analyses are oftentimes performed on convetional treadmills. The absence of force plates can be problematic for the detection for foot strike and toe off, which are critical for the comprehensive biomechanical analysis of running kinematics. FootNet is an algorithm for the detection of foot strike and toe off events on non-instrumented treadmills using segment and joint kinematics as input. The algorithm is based on an LSTM neural network architecture that has been trained, validated and tested using data from different labs, motion capture and treadmill systems, running speeds, running conditions and foot tracking models. Further details about FootNet development can be found in [REFTOSTUDY]. This repository includes all the software used for the study.

## Data

In this study we used five datasets including running kinematics and ground reaction forces collected on an instrumented treadmill. Two of those datasets are publicly available and will be used to demonstrate the processing steps followed for every dataset. The publicly available datasets can be downloaded from here:

Foot-strikes dataset: LINK

Inclines dataset: LINK

## Data processing

A Visual3D pipeline template is included for each dataset. This pipeline includes the GRF processing steps (e.g. baseline noise removal, down-sampling to motion capture sampling frequency), segment modeling and joint kinematics calculations and data export to .mat files. The pipeline template is modified to be participant-specific using a Matlab script that also runs each pipeline automatically.

SCRIPTNAME uses the exported files to 1) chop the GRF and kinematics variables into gait cycles using the highest point reached by the foot centre of mass, 2) detect gold standard foot strike (vertical GRF > 50 N) and toe off (vertical GRF < 50 N) within each cycle and 3) produce a one-hot encoded vector of labels (0 = non-contact, 1 = contact). The GRF and kinematics variables can be visualised in an interactive plot that allows for manual flagging of noisy/outlier cycles by clicking directly on the plotted signal. The data are stored in cycles and those cycles that have been flagged up are excluded.

## FootNet development

FootNet cross validation and testing can be replicated on Google Colab. Firstly, you need to download the data and notebooks from [here](https://drive.google.com/drive/folders/1MMpsXvz8-rDjTwwfOrp_k7zS_Om1gqLy?usp=sharing) and add them to your Google drive. The root directory has the following structure:

  - StepDetectionStudy
    - Data
      - OriginalDatasets. Folder containing the entire datasets (.npy) files as Python dictionaries.
      - DataFolds.npy File containing the training data grouped in 5 folds.
      - TestingSet.npy File containing the testing set.
    - CrossValidation.
      - Models. Folder containing the five models developed during cross validation.
      - Results. Folder containing the summary performance metrics for each model on its corresponding validation set and Bland-Altman plots comparing foot strike, toe off and contact times as predicted by FootNet vs gold standard method.

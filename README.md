# Overview

Motion capture running analyses are oftentimes performed on convetional (non-instrumented) treadmills. The absence of force plates can be problematic for the detection of foot strike and toe off, which are critical for the comprehensive biomechanical analysis of running kinematics. In this study, we introduce FootNet an algorithm for the detection of foot strike and toe off events on non-instrumented treadmills using segment and joint kinematics as input. The algorithm is based on an LSTM neural network architecture that has been trained, validated and tested using five datasets collected in three different labs using different motion capture and treadmill systems. The datasets include athletes of different abilities and foot strikes running at a wide range of speeds, and under different gradient, fatigue, and shoe conditions. running conditions and foot tracking models.

This repository contains all the software developed for the data processing, cross-validation and testing of FootNet as well as links to download the datasets used.

The pubication associated with this study can be found [here](link2pub).

# FootNet model

The model has been developed using Tensorflow 2.3.0 on Python 3.6.9 and can be downloaded from [here](https://drive.google.com/uc?export=download&id=18y8RhQTH3d1Nqp-CWiM415suUZxqjj-9). Clicking on the link will automatically start the dowload of a .zip folder containing the model as a SavedModel (Tensorflow saving format) directory (FootNetFinalModel), a data example file (Data_example.mat), an implementation example (FootNet_implementation.py) and a requirements.txt indicating the libraries and library versions needed to run the implementation example.

# Study replication

Complete replication of the study requires access to Visual3D (v6), Matlab (2018b) and Python (3.7). Nevertheless, all the files output by each script are also provided, so users can focus on a specific part of their interest or replicate the parts their software allows. Raw motion capture data and code for full data processing from raw marker trajectories and ground reaction forces to kinematic input features and corresponding desired labels can be found in the DataProcessing directory within this repository.

## FootNet development

FootNet cross-validation and testing can be replicated on Google Colab and *does not require the raw data and code mentioned in the previous section*. The final output of the previous processing steps can be dowloaded straight away from [here](https://drive.google.com/drive/folders/1MMpsXvz8-rDjTwwfOrp_k7zS_Om1gqLy?usp=sharing) and the Google Colab notebooks to replicate the development of Footnet can be found in this repository.

Before you begin, you need to download the project folder containing the data (should start automatically when clicking in the link provided in the previous paragraph)
and upload it to your Google Drive. The project directory StepDetectionStudy is organised as follows:

  - StepDetectionStudy
    - Data
      - OriginalDatasets. Folder containing the entire datasets (*_dataset.npy files).
      - DataFolds.npy File containing the training data grouped in 5 folds.
      - TestingSet.npy File containing the testing set.
      
      Data are organised as Python dictionaries containing the kinematic input features ['X'], label vectors ['Y'], metadata about the trials ['meta'] and vertical GRF ['GRFv']. Each of those dictionary keys contains a list with nested lists with the structure participant > trial > stride. For instance, dataset['X'][0][0][0] accesses the kinematic input features characterising the first stride recorded in the first trial of the first participant in dataset.
      
    - CrossValidation
      - Models. Folder containing the five models developed during cross validation.
      - Results. Folder containing the summary performance metrics for each model on its corresponding validation set and Bland-Altman plots comparing foot strike, toe off and contact times as predicted by FootNet vs gold standard method.
    - FinalTest
      - FootNet_best_candidate. Best set of parameters resulting from cross validation.
      - Summary performance metrics on testing set and Bland-Altman plots comparing foot strike, toe off and ocntact times as predicted by FootNet vs gold standard method.
      - y_and_yhat.mat File containing testing predictions, target labels and metadata from testing stride cycles for posterior analyses in Matlab presented in the paper.
    - FinalModel. Folder containing the final updated model resulting from FinalTest as a SavedModel directory (Tensorflow model format) and as .h5.

Once the project folder is in your Google Drive, you can use the Google Colab notebooks provided in this repository to replicate the data splitting, cross-validation and model testing. You can preview the notebook on Github however I would recommend opening the notebook in Google Colab to have full control over it. This option should appear at the top of your screen when you click on a given Google Colab notebook. For CrossValidation.ipynb and FinalTest.ipynb, make sure you are running on GPU by clicking on Runtime > Change Runtime type and selecting GPU.

- TrainTest_Split.ipynb. This notebook demonstrates how the dataset splitting was performed, including training and testing (70/30) and further folding of training dataset in 5 folds.
    - CrossValidation.ipnyb. This notebook performs 5-fold cross-validation and slected the best set of weights as best candidate for the final test.
    - FinalTest.ipnyb. This notebook updates the best candidate model resulting from cross-validation with the 5 folds as training set and performs the final test on the testing set.

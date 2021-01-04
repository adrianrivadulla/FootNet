## Data

The datasets used in this study include ground reaction forces collected on an instrumented treadmill and three-dimensional marker trajectories collected using an optoelectronic motion capture system. These datasets have been gathered from previosly published running biomechanics studies and have been named as:

FootStrikes dataset: LINK
Inclines dataset: LINK
Speed dataset: LINK
Footwear: LINK
Prolonged dataset: LINK

Please note that FootStrikes and Inclines were already open access datasets retrieved from [here](link) and [here](link), and credit should go to the researchers leading the original projects. We just reshare their work organised conveniently for our study.

The raw data and software needed to replicate our results can be accessed [here](link2datasoftwareetc). The project directory is organised as follows:

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
    - Figures. Folder containing all the figures in the paper and where the figures produced by the different scripts will be saved.
    - TestResults.

## Data processing

Biomechanical basic data processing steps including marker trajecotry filtering, rigid body segment model scaling, calculation of segment position and orientation, calculation of joint kinematics, ground reaction force baseline noise removal and filtering were performed in Visual3D. Visual3D pipelines for each individual to perform these steps are included. These subject-specific pipelines were automatically created based on a template and executed in Visual3D through Matlab using NameOfScript in Matlab. 

Following data processing steps including segmentation of running trials in gait cycles using the highest position of the foot centre of mass, ground reaction force and kinematics data quality assessment, identification of the contact phase using the vertical ground reaction force within each cycle and subsequent identification of foot strike and toe off were performed in Matlab using NameOfScript.

FootNet's architectue and development was completed in Python. NameOfScript Python script was used to gather the output files produced in the previous data processing steps, calculate segment linear velocities and save the input features, target labels, trial names and vertical ground reaction force vectors in a more "Python-friendly" format for FootNet development.


# FootNetDevelopmentStudy

This repository includes all the software used to process and analyse the data relating to the development of the FootNet step detection algorithm as implemented for the study [REFTOTHESTUDY].

## Data

In this study we used five datasets including running kinematics and ground reaction forces collected on an instrumented treadmill. Two of those datasets are publicly available and will be used to demonstrate the processing steps followed for every dataset. 

The publicly available datasets can be downloaded from here:

Foot-strikes dataset: LINK

Inclines dataset: LINK

## Data processing

A Visual3D pipeline template is included for each dataset. This pipeline includes the GRF processing steps (e.g. baseline noise removal, down-sampling to motion capture sampling frequency), segment modeling and joint kinematics calculations and data export to .mat files. The pipeline template is modified to be participant-specific using a Matlab script that also runs each pipeline automatically.

SCRIPTNAME uses the exported files to 1) chop the GRF and kinematics variables into gait cycles using the highest point reached by the foot centre of mass, 2) detect gold standard foot strike (vertical GRF > 50 N) and toe off (vertical GRF < 50 N) within each cycle and 3) produce a one-hot encoded vector of labels (0 = non-contact, 1 = contact). The GRF and kinematics variables can be visualised in an interactive plot that allows for manual flagging of noisy/outlier cycles by clicking directly on the plotted signal. The data are stored in cycles and those cycles that have been flagged up are excluded.

## FootNet development

FootNet development can be replicated running this GOOGLECOLAB notebook.

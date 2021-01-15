# FootNet

Motion capture running analyses are often performed on conventional (non-instrumented) treadmills. The absence of force plates can be problematic for the detection of foot strike and toe off, which are critical for the comprehensive biomechanical analysis of running kinematics. We introduce FootNet an algorithm for the detection of foot strike and toe off events on non-instrumented treadmills using segment and joint kinematics as input. The algorithm is based on an LSTM neural network architecture that has been trained, validated and tested using five datasets collected in three independent motion capture labs.

The publication associated with this study can be found [here](link2pub) (not available yet).

## Getting Started

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Pre-requisites

- Python 3.7

### Installing

- Clone this repository and enter it:

```Shell
   git clone https://github.com/adrianrivadulla/FootNet.git
   cd FootNet
   ```
-  Create models and output directories and download [model:](https://drive.google.com/uc?export=download&id=18y8RhQTH3d1Nqp-CWiM415suUZxqjj-9) (this only works manually by clicking on the link for now)

    ```Shell
    mkdir models
    mkdir output
    cd models
    command to download model
    cd ..
    ```

This same process can be replicated manually by downloading and unzipping this repository, creating the "models" and "output" folders in FootNet and downloading the model into the models folder.

- Set up the environment using one of the following methods:

    - Using [Anaconda:](https://www.anaconda.com/distribution/)

     ```Shell
     conda env create -f environment.yml
     ```

    - Using [pip:](https://pip.pypa.io/en/stable/installing/)

    ```Shell
    pip install venv
    python -m virtualenv env
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### Usage

Ensure that the model is downloaded into ```FootNet/models/``` and that data files are stored in ```FootNet/data/```. All files in this directory will be processed. Results are saved by default to the same folder with the same file name and the extension _contact_events.mat.

To run, navigate to the FootNet directory and use:

```Shell
    python FootNet_inference.py --samplingfreq 200 --output path/to/outputdirectory
```

FootNet_inference takes the sampling frequency to calculate linear velocities as required input and three optional inputs: the directory where data can be found or a path to a specific file, the model directory and the output directory where files should be saved. These are set by default to ./data/, ./models/ and ./data/ respectively so they are not needed for demonstration purposes but something to bear in mind when implementing the method in your own data.

## License

Copyright (c) 2021 Adrian R Rivadulla

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this program (see gpl.txt and lgpl.txt). If not, see <https://www.gnu.org/licenses/>.


# Citation
If you use FootNet or this code base in your work, please cite

```
@inproceedings{FootNet...,
  author    = {Adrian R. et al.},
  title     = {},
  booktitle = {},
  year      = {},
}
```
# FootNet development replication

FootNet development can be replicated on Google Colab. More details on FootNet cross-validation and model testing, how to download the data and run the notebooks can be found in the [notebooks folder] NEED A RELATIVE LINK THAT I CAN'T CREATE.

# Contact
For questions about our paper or code, please contact [Adrian R](mailto:arr43@bath.ac.uk).

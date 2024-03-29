# FootNet

[![DOI](https://zenodo.org/badge/302002826.svg)](https://zenodo.org/badge/latestdoi/302002826)

Motion capture running analyses are often performed on conventional (non-instrumented) treadmills. The absence of force plates can be problematic for the detection of foot strike and toe off, which are critical for the comprehensive biomechanical analysis of running kinematics. We introduce FootNet an algorithm for the detection of foot strike and toe off events on non-instrumented treadmills using segment and joint kinematics as input. The algorithm is based on an LSTM neural network architecture that has been trained, validated and tested using five datasets collected in three independent motion capture labs.

The publication associated with this study can be found [here](https://doi.org/10.1371/journal.pone.0248608).

## Getting Started

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Pre-requisites

- Python 3.7
- venv >= 19.0 (if using pip)

### Installing

- Clone this repository and enter it:

```Shell
   git clone https://github.com/adrianrivadulla/FootNet.git
   cd FootNet
   ```

- Create output directory where ouput data will be saved for the demo:

```Shell
mkdir output
```

This same process can be replicated manually by downloading and unzipping this repository, then creating the "output" folder in FootNet.

- Set up the environment using one of the following methods:

- Using [Anaconda](https://www.anaconda.com/distribution/), navigate to the FootNet directory and create a version environment with the environment.yml file provided:

     ```Shell
     cd /path/to/FootNet
     conda env create -f environment.yml
     ```

- Using [pip](https://pip.pypa.io/en/stable/installing/) on Windows:

    ```Shell
    python -m venv --system-site-packages .\venv
    .\venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

- Using [pip](https://pip.pypa.io/en/stable/installing/) on Ubuntu/macOS:

    ```Shell
    python3 -m venv --system-site-packages ./venv
    source ./venv/bin/activate  # sh, bash, or zsh
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

- Finally, verify the tensorflow install:

    ```Shell
    python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random normal([1000, 1000])))"
    ```

    If a tensor is returned, you've installed TensorFlow successfully. If an error is returned see [tensorflow website](https://www.tensorflow.org/install/).

### Usage

FootNet_v1 is deployed in [FootNet_inference.py](https://github.com/adrianrivadulla/FootNet/blob/main/FootNet_inference.py), navigate to the FootNet directory and use:

- Using default args (note that sampling frequency -sf must be added):

```Shell
    python FootNet_inference.py -sf 200
```

- To view all args:

```Shell
    python FootNet_inference.py --help
```

See docstring in [FootNet_inference.py](./FootNet_inference.py) for detailed information on each input argument and output argument.

A further [example](./FootNet_compare_to_FP.py) is provided to demonstrate the results of FootNet against force plates. To run use:

```Shell
    python FootNet_compare_to_FP.py
```

#### Matlab workaround through batch file (Windows OS)

Although Matlab has a new function called importKerasNetwork, as of January 2021, this function does not work as one would expect. A workaround to use FootNet through Matlab is included in the [CMD-Matlab folder](./CMD-Matlab).


## License

Copyright (c) 2021 Adrian R Rivadulla

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this program (see gpl.txt and lgpl.txt). If not, see <https://www.gnu.org/licenses/>.


# Citation
If you use FootNet or this code base in your work, please cite:

Rivadulla A, Chen X, Weir G, Cazzola D, Trewartha G, Hamill J, et al. (2021) Development and validation of FootNet; a new kinematic algorithm to improve foot-strike and toe-off detection in treadmill running. PLoS ONE 16(8): e0248608. [https://doi.org/10.1371/journal.pone.0248608](https://doi.org/10.1371/journal.pone.0248608)


# FootNet Training Replication

FootNet training can be replicated on Google Colab. More details on FootNet cross-validation and model testing, how to download the data and run the notebooks can be found in the [notebooks folder](./notebooks).

# Contact
For questions about our paper or code, please contact [Adrian R](mailto:arr43@bath.ac.uk).

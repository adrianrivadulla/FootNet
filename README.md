# FootNet

An LSTM model for predicting foot-strike and toe-off events during treadmill running using lower limb kinematic data.

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

- Download [model:](https://drive.google.com/uc?export=download&id=1pw37mEnt1xdn6EQvulYimjdGGxqu0C1u)

    ```Shell
    mkdir models
    cd models
    command to download model
    cd ..
    ```

### Usage

Ensure that the model is downloaded into ```FootNet/models/``` and that data files are stored in ```FootNet/data/```. All files in this directory will be processed. Results are saved to ```FootNet/output/```.

To run use:

```Shell
    python Footnet_inference.py
```

## License


Copyright (c) <2020> <Adrian R Rivadulla>

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


# Contact
For questions about our paper or code, please contact [Adrian R](mailto:arr43@bath.ac.uk).

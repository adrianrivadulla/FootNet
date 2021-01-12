# FootNet

An LSTM model for predciting foot-strike and toe-off events during treadmill running using lower limb kinematic data.

The pubication associated with this study can be found [here](link2pub) (not available yet).

## Getting Started

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Pre-requisites

- Python 3.6

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

- Download [model:](https://drive.google.com/uc?export=download&id=18y8RhQTH3d1Nqp-CWiM415suUZxqjj-9)

    ```Shell
    mkdir models
    cd models
    command to download model
    cd ..
    ```

### Usage

Ensure that the model is downloaded into ```FootNet/model/``` and that data files are stored in ```FootNet/data/```. All files in this directory will be processed. Results are saved to ```FootNet/ouput/```.

To run use:

```Shell
    python Footnet_inference.py
```

## License

tbc

# Citation
If you use FootNet or this code base in your work, please cite

```
@inproceedings{FootNet...,
  author    = {Adrian R. et al.},
  title     = {},
  booktitle = {,
  year      = {},
}
```


# Contact
For questions about our paper or code, please contact [Adrian R](mailto:arr43@bath.ac.uk).
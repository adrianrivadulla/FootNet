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

- Download [model:](https://drive.google.com/uc?export=download&id=18y8RhQTH3d1Nqp-CWiM415suUZxqjj-9) (this only works manually by clicking on the link for now)

    ```Shell
    mkdir models
    cd models
    command to download model
    cd ..
    ```

### Usage

Ensure that the model is downloaded into ```FootNet/models/``` and that data files are stored in ```FootNet/data/```. All files in this directory will be processed. Results are saved to the same folder with the same file name and the extension _contact_events.mat.

To run use:

```Shell
    python FootNet_inference.py --samplingfreq 200
```

FootNet_inference takes two optional inputs: the directory where data can be found or a path to a specific file and the model directory. These are set by default to ./data/ and ./models/ respectively so they are not needed for demonstration purposes but something to bear in mind when implementing the method in the real world.

## License

tbc

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

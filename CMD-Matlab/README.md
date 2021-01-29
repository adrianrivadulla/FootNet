Most of my PhD data processing scripts were written in Matlab (using Windows OS) so I had to find a workaround to integrate FootNet. This can be achieved by using [FootNet_call_CMD.bat](./FootNet_call_CMD.bat). This batch file executes FootNet_infernece.py through the command prompt, and can be called through Matlab.

Note that this still requires all the dependencies outlined in the Requirements section and that you have created your virtual environment to use FootNet through Anaconda. All you will be doing is telling Matlab to tell your computer to run a script in Python within this virual environment.

Before you can use the batch file, you will have to set the path to Anaconda, your environment name and the path to FootNet. Open the file with a text editor in your machine for more details.

Once your paths have been set, you can call it in Matlab using the command system() such as:

system('FootNet_call_CMD.bat "datapath=path\to\data" "output=path\to\output" "samplingfreq=200"')

Note that the input you pass to the batch file between "" is defined as a variable so it is important that it has the right names: datapath, output, samplingfreq.
Not all of them are needed as FootNet_inference.py has some default paths (see [FootNet_inference.py](../FootNet_inference.py) docu). In fact, the batch file can be run with no input and it won't crash but FootNet_inference.py will crash if samplingfreq is not provided.

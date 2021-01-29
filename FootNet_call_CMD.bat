:: This Batch file executes FootNet_inference.py. in its right virtual environment.
:: The same input FootNet_inference.py takes can be passed to the batch file.
:: E.g.
::
:: FootNet_call_CMD.bat "datapath=path\to\data" "output=path\to\output" "samplingfreq=200"
::
:: Note that the input you pass to the batch file between "" is defined as a variable so it is important
:: that it has the right names: datapath, output, samplingfreq.
:: Not all of them are needed as FootNet_inference.py has some default paths (see FootNet_inference.py docu).
:: In fact, the batch file can be run with no input and it won't crash but FootNet_inference.py will crash if 
:: samplingfreq is not provided.

:: Written by Adrian R Rivadulla, Jan 2021

:: Before you can use this file, you need to define a few paths in your local machine

:: Path to Anaconda e.g. C:\path\to\Anaconda3
set CONDAPATH=C:\Users\arr43\Anaconda3

:: Name of your virtual environment. This should be FootNetEnv if not changed when you installed FootNet
set ENVNAME=FootNetEnv

:: FootNet directory e.g. C:\path\to\FootNet
set FOOTNETDIR=H:\FootNet

:: MAIN

:: Parse input

if not %1.==. set %1
if not %2.==. set %2
if not %3.==. set %3

:: Create path to virtual environment
set ENVPATH=%CONDAPATH%\envs\%ENVNAME%

:: Activate conda environment
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

:: Navigate to FOOTNET drive
set FOOTNETDRIVE=%FOOTNETDIR:~0,2%
%FOOTNETDRIVE%

:: Navigate to FOOTNET dir
cd %FOOTNETDIR%

:: Initiate FOOTNETCALL
set FOOTNETCALL=FootNet_inference.py

:: Add input to FOOTNETCALL string
if defined samplingfreq set FOOTNETCALL= %FOOTNETCALL% --samplingfreq %samplingfreq%
if defined datapath set FOOTNETCALL= %FOOTNETCALL% --datapath %datapath%
if defined output set FOOTNETCALL= %FOOTNETCALL% --output %output%

:: Run it
python %FOOTNETCALL%

@echo off

:: Set the path to the conda executable
set CONDA_PATH=C:\Path\To\anaconda3\Scripts\activate.bat

:: Activate the NSIenv environment
call "%CONDA_PATH%" activate NSIenv

:: Run the python script
python "C:\Path\To\libraries\sysmlGPTUI.py"

:: Deactivate the environment
: : call "%CONDA_PATH%" deactivate

pause

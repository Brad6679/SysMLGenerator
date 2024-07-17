:: %windir%\System32\cmd.exe "/K" C:\Users\brady\anaconda3\Scripts\activate.bat C:\Users\brady\anaconda3
:: activate NSIEnv
:: python sysmlGPTUI.py

@echo off

:: Set the path to the conda executable
set CONDA_PATH=C:\Users\<User>\anaconda3\Scripts\activate.bat

:: Activate the NSIenv environment
call "%CONDA_PATH%" activate NSIenv

:: Run the python script
python "sysmlGPTUI.py"

:: Deactivate the environment
: : call "%CONDA_PATH%" deactivate

pause

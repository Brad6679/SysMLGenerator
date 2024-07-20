# SysMLGenerator
Windows/Linux software to use GPT to generate SysMLv2 code using fine tuned assistant.


# sysmlGPT.py
OpenAI wrapper to query assistant for a SysMLv2 diagram using textual or image input, create object using obj = sysmlGPT('Default')
Current version does not support other arguments to constructor.
Handles both GPT code output, and text output parsing to isolate code snippet using regex.
Fill <OpenAI Key> with your key.
Replace asst_id with you assistant's ID.

# sysmlGPTUI.py
PyQt5 class to interface with user, sysmlGPT object, and JupyterSandbox CLI.

![Screenshot (200)](https://github.com/user-attachments/assets/dd7e2dac-3d7b-44e8-8735-b16c9b5c1372)

# JupyterBook.py
Jupyter CLI wrapper to run sysml kernel and get error dump/visualization of sysml diagram.

# startCode.bat
Batch file to run software on windows, calls anaconda environment then sysmlGPTUI to output code/errors to terminal and save diagram image to working directory with given name from GPT.
Fill 'User' with your user and 'Env' with conda environment.

# startCode.sh
Bash file to run software on linux, calls anaconda environment then sysmlGPTUI to output code/errors to terminal and save diagram image to working directory with given name from GPT.
Fill 'Env' with your environment name.

Code is currently relatively buggy, but works for one off text/image prompts fed to UI (may run multiple times for one prompt, working on debugging).

# sysmlgen.yaml
Anaconda environment config file to install environment.

# Dependencies
- Python 3.10
- PyQt5
- openai
- cairosvg
- nbformat

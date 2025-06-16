@echo off
setlocal enabledelayedexpansion

set "SCRIPT=MainGUI.py"
set "REQUIREMENTS=requirements.txt"

python -m pip install --upgrade pip
python -m pip install -r "%REQUIREMENTS%"

python "%SCRIPT%"

pause


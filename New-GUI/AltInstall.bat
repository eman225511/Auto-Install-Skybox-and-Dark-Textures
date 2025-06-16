@echo off
setlocal enabledelayedexpansion

set "PYTHON_INSTALLER=python-3.12.1-amd64.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.1/%PYTHON_INSTALLER%"

REM Check if python 3.12 is already installed
where python >nul 2>nul
if %errorlevel%==0 (
    python --version 2>nul | find "3.12." >nul
    if %errorlevel%==0 (
        echo Python 3.12 is already installed.
        pause
        goto :eof
    )
)

REM Download Python installer if not present
if not exist "%PYTHON_INSTALLER%" (
    echo Downloading Python 3.12.1 installer...
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"
)

REM Install Python 3.12.1 silently and add to PATH
echo Installing Python 3.12.1...
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Wait for install to finish
timeout /t 10 >nul

REM Verify installation
where python >nul 2>nul
if %errorlevel%==0 (
    python --version
    echo Python 3.12 installation complete.
) else (
    echo Python installation failed.
)

pause
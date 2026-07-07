@echo off
REM Timeseek Lifecycle Script (Windows)
REM Philosophy: Offline, Portable, 1-Click

if "%1"=="check-prereqs" goto check-prereqs
if "%1"=="install" goto install
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="uninstall" goto uninstall
if "%1"=="help" goto help

:help
echo Usage: %0 {check-prereqs^|install^|start^|stop^|uninstall^|help}
goto :eof

:check-prereqs
echo Checking prerequisites...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: python is not installed.
)
echo Prerequisites met.
goto :eof

:install
call :check-prereqs
echo Installing Timeseek...
python -m pip install .
goto :eof

:start
echo Starting Timeseek...
python -m timeseek.app
goto :eof

:stop
echo Stopping Timeseek...
taskkill /F /FI "COMMANDLINE eq python.exe -m timeseek.app"
goto :eof

:uninstall
echo Uninstalling Timeseek...
python -m pip uninstall timeseek -y
goto :eof

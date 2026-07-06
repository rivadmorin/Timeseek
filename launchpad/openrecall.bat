@echo off
REM OpenRecall Lifecycle Script (Windows)
REM Philosophy: Offline, Portable, 1-Click

if "%1"=="install" goto install
if "%1"=="run" goto run
if "%1"=="stop" goto stop
if "%1"=="uninstall" goto uninstall

echo Usage: %0 {install^|run^|stop^|uninstall}
goto :eof

:install
echo Installing OpenRecall...
python -m pip install .
goto :eof

:run
echo Starting OpenRecall...
python -m openrecall.app
goto :eof

:stop
echo Stopping OpenRecall...
taskkill /F /FI "COMMANDLINE eq python.exe -m openrecall.app"
goto :eof

:uninstall
echo Uninstalling OpenRecall...
python -m pip uninstall openrecall -y
goto :eof

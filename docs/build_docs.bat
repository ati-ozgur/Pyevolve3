@echo off
set "PYTHONPATH=%~dp0..;%PYTHONPATH%"
pushd "%~dp0source"
quartodoc build
if errorlevel 1 exit /b %errorlevel%
quarto render
set result=%errorlevel%
popd
exit /b %result%
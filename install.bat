@echo off
echo [Creating virtual env]
py -m venv venv
cd venv\Scripts
echo [Activating virtual env]
call activate
cd ..
cd ..
echo [Installing requirement.txt]
pip install -r requirement.txt
echo.
echo.
echo =================================================================
echo                          All done :)
echo =================================================================
pause
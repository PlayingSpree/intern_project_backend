@echo off
cd venv\Scripts
echo [Activating virtual env]
call activate
echo Done
cd ..
cd ..
echo.
echo [Running Create Superuser Command]
echo Enter user data...
echo.
py manage.py createsuperuser
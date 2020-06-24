@echo off
cd venv\Scripts
echo [Activating virtual venv]
call activate
echo.
echo Done
cd ..
cd ..
echo.
echo [Migating Databases]
echo.
py manage.py makemigrations
py manage.py migrate
echo.
echo [Running Server]
echo.
py manage.py runserver
pause
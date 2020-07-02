del "db.sqlite3" /f /q
del "authapp\migrations\0*" /f /q
del "authapp\migrations\__pycache__" /f /q
del "grouplearning\migrations\0*" /f /q
del "grouplearning\migrations\__pycache__" /f /q
del "sop\migrations\0*" /f /q
del "sop\migrations\__pycache__" /f /q

@echo off
echo.
echo Database deleted. RIP.
pause
@echo off
REM ============================================================
REM  Al-Kawthar ERP — START SERVER (run every time)
REM  Double-click to start. Keep this window open.
REM ============================================================
cd /d "%~dp0.."
call venv\Scripts\activate.bat
cd ERP

echo.
echo ============================================================
echo  Al-Kawthar ERP chal raha hai
echo  Is server par     : http://localhost:8000
echo  LAN ke doosre PC se: http://%COMPUTERNAME%:8000  (ya server-IP:8000)
echo  Band karne ke liye : is window me Ctrl+C ya window close
echo ============================================================
echo.

waitress-serve --host=0.0.0.0 --port=8000 ERP.wsgi:application
pause

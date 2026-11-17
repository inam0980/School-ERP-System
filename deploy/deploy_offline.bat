@echo off
REM ============================================================
REM  Al-Kawthar ERP — OFFLINE INSTALL (run ONCE on the server)
REM  Requirement: Python 3.14.x already installed (Add to PATH).
REM  Just double-click this file.
REM ============================================================
REM  This file lives in DEPLOY\ ; jump to the project root.
cd /d "%~dp0.."

echo.
echo === [1/4] Creating virtual environment ===
python -m venv venv
if errorlevel 1 ( echo Python not found. Install Python 3.14 first. & pause & exit /b 1 )

call venv\Scripts\activate.bat

echo.
echo === [2/4] Installing packages (offline) ===
python -m pip install --no-index --find-links="%CD%\offline_packages" -r requirements.txt
if errorlevel 1 ( echo Package install failed. & pause & exit /b 1 )

echo.
echo === [3/4] Applying database migrations ===
cd ERP
python manage.py migrate

echo.
echo === [4/4] Collecting static files ===
python manage.py collectstatic --noinput

echo.
echo ============================================================
echo  DONE!  Ab DEPLOY\start_server.bat (ya install_service.bat) chalao.
echo ============================================================
pause

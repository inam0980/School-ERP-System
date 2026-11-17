@echo off
cd /d "%~dp0..\.."
set ROOT=%CD%
echo Project root: %ROOT%

echo === Copying files ===
copy /Y "%~dp0urls.py"       "%ROOT%\ERP\ERP\urls.py"
copy /Y "%~dp0settings.py"   "%ROOT%\ERP\ERP\settings.py"
copy /Y "%~dp0base.html"     "%ROOT%\ERP\templates\base.html"
if not exist "%ROOT%\ERP\static\js"  mkdir "%ROOT%\ERP\static\js"
if not exist "%ROOT%\ERP\static\css" mkdir "%ROOT%\ERP\static\css"
copy /Y "%~dp0tailwind.css"  "%ROOT%\ERP\static\css\tailwind.css"

echo === Collecting static files ===
call "%ROOT%\venv\Scripts\activate.bat"
cd ERP
python manage.py collectstatic --noinput

echo === Restarting service ===
net stop AlKawtharERP
net start AlKawtharERP

echo ============================================================
echo  DONE! Browser me Ctrl+F5 karo.
echo ============================================================
pause

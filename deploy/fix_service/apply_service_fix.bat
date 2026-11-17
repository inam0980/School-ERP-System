@echo off
REM ============================================================
REM  SERVICE FIX — purani service hata ke nayi (python serve.py)
REM  RIGHT-CLICK -> "Run as administrator"
REM  Ye file C:\erp\DEPLOY\fix_service\ me honi chahiye.
REM ============================================================
cd /d "%~dp0..\.."
set ROOT=%CD%

net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo  !! Administrator ke roop me chalao !!
    echo  right-click -^> "Run as administrator"
    echo.
    pause
    exit /b 1
)

set SVC=AlKawtharERP
set NSSM="%ROOT%\nssm\nssm.exe"

echo === Copying serve.py ===
copy /Y "%~dp0serve.py" "%ROOT%\ERP\serve.py"

echo === Removing old service ===
%NSSM% stop %SVC% >nul 2>&1
%NSSM% remove %SVC% confirm >nul 2>&1

echo === Installing service (python.exe + serve.py) ===
%NSSM% install %SVC% "%ROOT%\venv\Scripts\python.exe" "%ROOT%\ERP\serve.py"
%NSSM% set %SVC% AppDirectory "%ROOT%\ERP"
%NSSM% set %SVC% DisplayName "Al-Kawthar ERP"
%NSSM% set %SVC% Description "Al-Kawthar School ERP (Django + Waitress)"
%NSSM% set %SVC% AppEnvironmentExtra PYTHONUTF8=1
%NSSM% set %SVC% Start SERVICE_AUTO_START
%NSSM% set %SVC% AppStdout "%ROOT%\ERP\logs_service.txt"
%NSSM% set %SVC% AppStderr "%ROOT%\ERP\logs_service.txt"

echo === Starting service ===
%NSSM% start %SVC%
%NSSM% status %SVC%

echo.
echo ============================================================
echo  Ho gaya. 5 second ruk ke browser me localhost:8000 test karo.
echo  "SERVICE_RUNNING" upar dikhe to service chalu hai.
echo ============================================================
pause

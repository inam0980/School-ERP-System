@echo off
REM ============================================================
REM  Al-Kawthar ERP — INSTALL AS WINDOWS SERVICE (auto-start)
REM  RIGHT-CLICK this file  ->  "Run as administrator"
REM  After this, ERP boot par apne aap chalu rahega.
REM ============================================================
cd /d "%~dp0.."
set ROOT=%CD%

net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo  !! Administrator ke roop me chalao !!
    echo  Is file par right-click -^> "Run as administrator"
    echo.
    pause
    exit /b 1
)

set SVC=AlKawtharERP
set NSSM="%ROOT%\nssm\nssm.exe"

echo === Removing old service (if any) ===
%NSSM% stop %SVC% >nul 2>&1
%NSSM% remove %SVC% confirm >nul 2>&1

echo === Installing service ===
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

echo.
echo ============================================================
echo  DONE!  Service "Al-Kawthar ERP" chalu aur auto-start ON.
echo  Browser: http://%COMPUTERNAME%:8000  (ya server-IP:8000)
echo  Server reboot hone par bhi apne aap chalega.
echo ============================================================
pause

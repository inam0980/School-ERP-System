@echo off
REM ============================================================
REM  Al-Kawthar ERP — REMOVE WINDOWS SERVICE
REM  RIGHT-CLICK  ->  "Run as administrator"
REM ============================================================
cd /d "%~dp0.."
set ROOT=%CD%

net session >nul 2>&1
if errorlevel 1 (
    echo  !! Administrator ke roop me chalao (right-click -^> Run as administrator) !!
    pause
    exit /b 1
)

set SVC=AlKawtharERP
set NSSM="%ROOT%\nssm\nssm.exe"

%NSSM% stop %SVC%
%NSSM% remove %SVC% confirm

echo.
echo  Service hata diya gaya.  (Project aur data waise hi safe hai.)
pause

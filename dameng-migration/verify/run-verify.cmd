@echo off
chcp 65001 >nul
setlocal
set "VENV=C:\Users\AIGC\.workbuddy\binaries\python\envs\default"
set "PY=%VENV%\Scripts\python.exe"

if not exist "%PY%" (
  echo [ERROR] Python venv not found: %PY%
  echo Please reinstall jaydebeapi and JPype1 in the networked window.
  pause
  exit /b 1
)

if "%~1"=="" goto usage

"%PY%" "%~dp0dm8check.py" %*
echo.
pause
exit /b 0

:usage
echo Usage: run-verify.cmd ^<mode^> [options]
echo.
echo   selftest   check toolchain and database reachability, no DB login
echo   list       offline inventory of statements, no DB login
echo   probe      run DUAL probes in probes\probe-*.sql        [needs DB]
echo   diff       run equivalence diff in probes\diff-*.sql   [needs DB]
echo   e2         run ..\e2-verify-*.sql                       [needs DB]
echo.
echo Options:
echo   --files a.sql b.sql    specify input files
echo   --user NAME            database user
echo   --out path.csv         output csv path
echo.
echo Password: set environment variable DM8_PASSWORD, otherwise prompted.
echo.
pause
exit /b 0

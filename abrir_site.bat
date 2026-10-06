@echo off
setlocal
cd /d "%~dp0"

rem Reuse an existing local server or start one with an available Python runtime.
netstat -ano | findstr /R /C:":8000 .*LISTENING" >nul
if errorlevel 1 (
  where py >nul 2>nul
  if not errorlevel 1 (
    start "Forno & Afeto - servidor" /min py -3 server.py
    goto wait_for_server
  )
  where python >nul 2>nul
  if not errorlevel 1 (
    start "Forno & Afeto - servidor" /min python server.py
    goto wait_for_server
  )
  if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    start "Forno & Afeto - servidor" /min "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" server.py
    goto wait_for_server
  )
  echo Nao encontrei o Python. Instale Python 3 e tente novamente.
  pause
  exit /b 1
)
goto open_browser

:wait_for_server
timeout /t 2 /nobreak >nul

:open_browser
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8000/
  exit /b 0
)
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8000/
  exit /b 0
)
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
  start "" "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8000/
  exit /b 0
)
start "" http://127.0.0.1:8000/

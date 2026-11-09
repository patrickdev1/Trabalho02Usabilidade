@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto local
if exist "..\.venv\Scripts\python.exe" goto workspace
where py >nul 2>nul
if not errorlevel 1 (
  py -3 -m venv .venv
) else (
  python -m venv .venv
)
if not exist ".venv\Scripts\python.exe" goto missing
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
:local
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto failed
exit /b 0
:workspace
"..\.venv\Scripts\python.exe" main.py
if errorlevel 1 goto failed
exit /b 0
:missing
echo Instale Python 3.12 de https://www.python.org/downloads/ e marque Add Python to PATH.
:failed
echo Nao foi possivel iniciar. Consulte o erro acima e o README.md.
pause
exit /b 1

@echo off
title Frontend Store

echo Iniciando Frontend Store...
call "%~dp0.venv\Scripts\activate.bat"

start "" http://127.0.0.1:5000

python "%~dp0app.py"

pause

@echo off
REM Define o caminho do interpretador Python
set PYTHON_PATH=C:\Users\mathr\AppData\Local\Programs\Python\Python310\python.exe

REM Caminho para o script Python
set SCRIPT_PATH=%~dp0add_text_to_videos_opencv.py

REM Executa o script Python
%PYTHON_PATH% %SCRIPT_PATH%

pause
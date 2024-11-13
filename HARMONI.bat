@echo off

REM Cambia al directorio del archivo .bat
cd /d %~dp0

REM Usa pushd para manejar correctamente la ruta UNC
pushd \\192.168.5.44\harmoni\database\gui

REM Activa el entorno virtual
call myenv\Scripts\activate.bat

REM Ejecuta el script
python src\main_gui.py

REM Regresa al directorio original
popd
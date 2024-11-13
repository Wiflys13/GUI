@echo off

REM Cambia al directorio del archivo .bat
cd /d %~dp0

REM Activa el entorno virtual
call .\myenv\Scripts\activate

REM Ejecuta el script
python src\main_gui.py
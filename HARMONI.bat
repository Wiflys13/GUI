@echo off
REM Cambia al directorio donde está el entorno virtual
cd /d "C:\Users\HARMONI\Documents\HARMONI\GUI"

REM Activa el entorno virtual
call .\myenv\Scripts\activate

REM Ejecuta el script
python src\main_gui.py

REM Espera a que el usuario presione una tecla antes de cerrar la ventana
pause
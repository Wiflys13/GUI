@echo off

REM Activa el entorno virtual
call .\myenv\Scripts\activate

REM Ejecuta el script
python src\main_gui.py

REM Espera a que el usuario presione una tecla antes de cerrar la ventana
pause
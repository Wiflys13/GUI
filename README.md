# Graphical User Interface for Harmoni APP

## Instalacion de la APP

**1) Instalar Python desde el sitio oficial:**

* Ve al sitio web de [Python](https://www.python.org/downloads/)
* Descarga la versión adecuada para tu sistema operativo.
* Asegúrate de seleccionar la opción "Add Python to PATH" durante la instalación.

**2) En el directorio ./GUI activar el entorno virtual de Python**
```
python -m venv myenv
```

**3) Habilitar entorno virtual**
En windows:
Configuracion/Sistema/Para programadores/PowerShell --> Activado

**4) Activar entorno virtual**
```
.\myenv\Scripts\Activate
```

**5) Instalar las dependencias**
```
pip install -r requirements.txt
```

**6) Crear y configurar .env
* Crea un archivo llamado .env en la raiz del directorio
* Añade la siguiente linea ajustando la IP de la API

```
API_IP = 000.000.0.000 # Reemplazar por la IP real de la API 
```

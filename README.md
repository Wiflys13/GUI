# Graphical User Interface for Harmoni (HRM-GUI)

## Installation of the APP

**1) Install Python from the official website:**

* Go to the [Python](https://www.python.org/downloads/) website.
* Download the appropriate version for your operating system.
> [!NOTE]
> Recommended version: 3.12
* Make sure to select the "Add Python to PATH" option during installation.

**2) Activate the Python virtual environment**  
> [!IMPORTANT]  
> In the `./GUI` directory:
```
python -m venv myenv
cd .\myenv\Scripts
python.exe -m pip install --upgrade pip
```

**3) Enable the virtual environment**

* On Windows: Settings/System/For Developers/PowerShell --> Enabled
* On Mac: Open Terminal and ensure you're using the correct shell (bash, zsh, etc.).


**4) Activate the virtual environment**
* On Windows
```
.\myenv\Scripts\Activate 
```
* On MacOS:
```
source ./myenv/bin/activate
```

**5) Install the dependencies**

```
pip install -r requirements.txt
```

**6) Create and configure the `.env` file**
* Create a file named `.env` in the root directory.
* Add the following line, adjusting the API IP address:

```
API_IP = 000.000.0.000 # Reemplazar por la IP real de la API 
```

**7) Create ejecutable - Pyinstaller

> [!Note]
> Tengo que añadir a mano los paths.
> Si se corrige: pyinstaller --onefile --noconsole main_gui.py

```
pyinstaller --onefile --noconsole --paths=C:/local_project/src main_gui.py
```
#config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer la IP de la API desde las variables de entorno
API_IP = os.getenv("API_IP")
URL_VPN = f'http://{API_IP}'
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Cargar .env variables
load_dotenv()

# Variables generales
LOG_PATH = os.getenv("LOG_PATH")
DB_PATH = os.getenv("DB_PATH")
RUTA_EXCEL = os.getenv("PRODUCTS_PATH")
RUTA_RESUMEN = os.getenv("RESULT_PATH")
LIMITE_PRODUCTOS = int(os.getenv("LIMITE_PRODUCTOS"))


# Gmail
GMAIL_USUARIO = os.getenv("GMAIL_USUARIO")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
GMAIL_CLAVE_ENCRYPTED = os.getenv("GMAIL_CLAVE_ENCRYPTED")



# Validación y descifrado
try:
    if ENCRYPTION_KEY and GMAIL_CLAVE_ENCRYPTED:
        fernet = Fernet(ENCRYPTION_KEY.encode())
        GMAIL_CLAVE = fernet.decrypt(GMAIL_CLAVE_ENCRYPTED.encode()).decode()
    else:
        raise ValueError("Faltan ENCRYPTION_KEY o GMAIL_CLAVE_ENCRYPTED en .env")
except Exception as e:
    print(" Error al descifrar la clave:", e)
    GMAIL_CLAVE = None
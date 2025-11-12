from cryptography.fernet import Fernet
import getpass
import os

def generar_clave():
    return Fernet.generate_key()

def cifrar_clave(clave, key):
    fernet = Fernet(key)
    return fernet.encrypt(clave.encode())

def main():
    print("🔐 Configuración inicial del bot Amazon")
    log_path = input("Ruta para el log (ej: F:/.../bot.log): ")
    db_path = input("Ruta para la base de datos (ej: F:/.../AmazonProductos.db): ")
    limite = input("Cantidad de productos a buscar (ej: 40): ")
    product_path = input("Ruta ubicacaion del archico Productos (ej: F:/.../Producto.xlsx): ")
    result_path = input("Ruta ubicacion del archivo Resultados (ej: F:/.../Resultados.xlsx): ")

    gmail_usuario = input("Correo Gmail: ")
    gmail_clave = getpass.getpass("Clave Gmail (no se mostrará): ")

    key = generar_clave()
    clave_cifrada = cifrar_clave(gmail_clave, key)

    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"LOG_PATH={log_path}\n")
        f.write(f"DB_PATH={db_path}\n")
        f.write(f"LIMITE_PRODUCTOS={limite}\n")
        f.write(f"PRODUCTS_PATH={product_path}\n")
        f.write(f"RESULT_PATH={result_path}\n")
        f.write(f"GMAIL_USUARIO={gmail_usuario}\n")
        f.write(f"GMAIL_CLAVE_ENCRYPTED={clave_cifrada.decode()}\n")
        f.write(f"ENCRYPTION_KEY={key.decode()}\n")

    print("\n Archivo .env generado con éxito.")

if __name__ == "__main__":
    main()
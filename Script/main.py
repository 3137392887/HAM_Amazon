import pandas as pd
from scraper import iniciar_driver, buscar_productos_amazon
from database import guardar_en_db, obtener_mas_baratos
from emailer import enviar_resumen_por_correo
from utils import convertir_usd_a_cop
from database import limpiar_tabla_productos
from config import GMAIL_USUARIO, RUTA_EXCEL, RUTA_RESUMEN
import os
import logging

# Ruta del archivo de entrada

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RUTA_EXCEL = RUTA_EXCEL
RUTA_RESUMEN = RUTA_RESUMEN
EMAIL_DESTINO = GMAIL_USUARIO

def main():
    limpiar_tabla_productos() 
    driver = iniciar_driver()

    # 1. Leer productos desde Excel
    try:
        productos = pd.read_excel(RUTA_EXCEL)['PRODUCTO'].dropna().tolist()
    except Exception as e:
        print(f"Error leyendo archivo Excel: {e}")
        return

    # 2. Buscar productos en Amazon y guardar en DB
    for producto in productos:
        print(f"Buscando: {producto}")
        resultados = buscar_productos_amazon(producto, driver)
        guardar_en_db(resultados, producto)

    # 3. Obtener el más barato por producto
    resumen = obtener_mas_baratos()

    # 4. Convertir precios a COP
    for item in resumen:
        try:
            precio_usd = float(item['precio_usd'])
            item['precio_cop'] = convertir_usd_a_cop(precio_usd)
        except (TypeError, ValueError):
            item['precio_cop'] = None

    # 5. Guardar resumen en Excel
    df_resumen = pd.DataFrame(resumen)
    df_resumen.to_excel(RUTA_RESUMEN, index=False)

    # 6. Enviar resumen por correo
    enviar_resumen_por_correo(EMAIL_DESTINO, RUTA_RESUMEN)

    print("Proceso completado exitosamente.")
    logging.info("Proceso completado exitosamente.")

if __name__ == "__main__":
    main()
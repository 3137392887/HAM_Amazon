import os
import sqlite3
from config import DB_PATH

DB_PATH = DB_PATH

def limpiar_tabla_productos():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos")  
        conn.commit()
        conn.close()
        print(" Tabla de productos limpiada correctamente.")
    except Exception as e:
        print(f" Error al limpiar la tabla: {e}")


def guardar_en_db(lista_productos, producto_busqueda):
    """
    Inserta una lista de productos en la tabla Productos.
    Cada producto es un dict con nombre, precio_usd y entrega.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for item in lista_productos:
        nombre = item.get("nombre", "No disponible")
        precio = item.get("precio_usd", None)
        entrega = item.get("entrega", "No disponible")

        cursor.execute("""
            INSERT INTO Productos (Nombre, Precio, TipoEntrega)
            VALUES (?, ?, ?)
        """, (nombre, precio, entrega))

    conn.commit()
    conn.close()


def obtener_mas_baratos():
    """
    Devuelve el producto más barato por nombre (asumiendo que cada búsqueda genera múltiples registros).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT idProducto, Nombre, MIN(Precio) as Precio, TipoEntrega
        FROM Productos
        WHERE Precio IS NOT NULL
        GROUP BY Nombre
    """)

    resultados = []
    for row in cursor.fetchall():
        resultados.append({

            "idProducto": row[0],
            "nombre": row[1],
            "precio_usd": row[2],
            "entrega": row[3]
            
        })

    conn.close()
    return resultados
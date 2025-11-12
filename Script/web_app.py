from flask import Flask, render_template, request
from config import DB_PATH
import sqlite3
import os


app = Flask(__name__)

# Cargar .env desde la raíz del proyecto
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_PATH = os.getenv("DB_PATH")

if not DB_PATH:
    raise ValueError("No se encontró DB_PATH en el archivo .env")


def obtener_productos(nombre_filtro=None, precio_min=None, precio_max=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT Nombre, Precio, TipoEntrega FROM Productos WHERE 1=1"
    params = []

    if nombre_filtro:
        query += " AND Nombre LIKE ?"
        params.append(f"%{nombre_filtro}%")
    if precio_min:
        query += " AND Precio >= ?"
        params.append(precio_min)
    if precio_max:
        query += " AND Precio <= ?"
        params.append(precio_max)

    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()

    return resultados

@app.route('/', methods=['GET', 'POST'])
def index():
    nombre = request.form.get('nombre')
    precio_min = request.form.get('precio_min')
    precio_max = request.form.get('precio_max')

    # Convertir precios a float si están presentes
    precio_min = float(precio_min) if precio_min else None
    precio_max = float(precio_max) if precio_max else None

    productos = obtener_productos(nombre, precio_min, precio_max)
    return render_template('index.html', productos=productos)


if __name__ == '__main__':
    app.run(debug=True)
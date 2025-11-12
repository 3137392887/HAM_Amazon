from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Insumos', 'AmazonProductos.db'))

@app.route('/diagnostico', methods=['GET'])
def diagnostico():
    """Verifica si la BD existe y tiene datos"""
    if not os.path.exists(DB_PATH):
        return jsonify({"error": f"Base de datos no encontrada en: {DB_PATH}"}), 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        
        # Contar productos
        cursor.execute("SELECT COUNT(*) FROM Productos")
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            "db_path": DB_PATH,
            "existe": True,
            "tablas": [t[0] for t in tablas],
            "total_productos": total
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/producto/<int:id_producto>', methods=['GET'])
def obtener_producto(id_producto):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT idProducto, Nombre, Precio, TipoEntrega FROM Productos WHERE idProducto = ?", (id_producto,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "idProducto": row[0],
            "nombre": row[1],
            "precio_usd": row[2],
            "tipo_entrega": row[3]
        })
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, send_file
import sqlite3
import matplotlib.pyplot as plt
import io
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Conexión a la base de datos SQLite
def init_db():
    conn = sqlite3.connect('sensorWifi.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ldr_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor_ldr INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

# Ruta para recibir los datos del LDR
@app.route('/recibir_dato', methods=['POST'])
def recibir_dato():
    valor_ldr = request.form.get('valor_ldr')

    if valor_ldr:
        # Insertar los datos en la base de datos
        conn = sqlite3.connect('sensorWifi.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ldr_data (valor_ldr) VALUES (?)", (valor_ldr,))
        conn.commit()
        conn.close()
        return "Datos guardados correctamente", 200
    else:
        return "Error en los datos", 400

# Ruta para mostrar los datos guardados y graficarlos
@app.route('/mostrar_datos', methods=['GET'])
def mostrar_datos():
    conn = sqlite3.connect('sensorWifi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ldr_data ORDER BY fecha DESC")
    rows = cursor.fetchall()
    conn.close()

    # Procesar los datos para el gráfico
    timestamps = [row[2] for row in rows]
    ldr_values = [row[1] for row in rows]

    # Convertir fechas a formato datetime
    timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps]

    # Crear gráfico de la serie temporal
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, ldr_values, label="LDR Value", color='blue')
    plt.xlabel("Time")
    plt.ylabel("LDR Value")
    plt.title("Time Series of LDR Values")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar el gráfico en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Enviar el gráfico como respuesta
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    init_db()  # Crear la base de datos si no existe
    app.run(host='0.0.0.0', port=5000)

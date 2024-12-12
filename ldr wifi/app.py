from flask import Flask, request
import sqlite3
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


# Ruta para mostrar los datos guardados
@app.route('/mostrar_datos', methods=['GET'])
def mostrar_datos():
   conn = sqlite3.connect('sensorWifi.db')
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM ldr_data ORDER BY fecha DESC")
   rows = cursor.fetchall()
   conn.close()


   return {'data': rows}, 200


if __name__ == '__main__':
   init_db()  # Crear la base de datos si no existe
   app.run(host='0.0.0.0', port=5000)


 

import serial
import sqlite3
import time

# Configura el puerto serial donde tu Arduino está conectado (ajusta el puerto según tu sistema)
arduino = serial.Serial('/dev/ttyUSB0', 115200)  # Cambia '/dev/ttyUSB0' por el puerto correcto en tu sistema
time.sleep(2)  # Espera 2 segundos para asegurarse de que la conexión esté establecida

# Conectar a la base de datos (se creará automáticamente si no existe)
conn = (sqlite3.connect('sensores.db'))
cursor = conn.cursor()

# Crear la tabla si no existe (sin usar CREATE DATABASE ni USE)
cursor.execute("""
CREATE TABLE IF NOT EXISTS ldr_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_ldr INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

while True:
    # Leer el valor del LDR desde el puerto serial
    if arduino.in_waiting > 0:
        ldr_value = arduino.readline().decode('utf-8').strip()
        if ldr_value.startswith("Valor del LDR: "):
            # Obtener el valor numérico del LDR
            valor_ldr = int(ldr_value.split(": ")[1])
            
            # Insertar el valor en la base de datos
            cursor.execute("INSERT INTO ldr_data (valor_ldr) VALUES (?)", (valor_ldr,))
            conn.commit()
            print(f"Valor del LDR guardado: {valor_ldr}")
    
    time.sleep(1)

# Cerrar la conexión
conn.close()

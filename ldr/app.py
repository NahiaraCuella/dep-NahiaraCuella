from flask import Flask, render_template, jsonify
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Función para obtener datos desde la base de datos
def get_ldr_data():
    conn = sqlite3.connect('sensores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, valor_ldr FROM ldr_data ORDER BY fecha")
    data = cursor.fetchall()
    conn.close()
    return data

# Ruta para mostrar la gráfica
@app.route('/')
def index():
    # Obtener los datos
    data = get_ldr_data()

    if not data:
        return "No hay datos disponibles para graficar."

    # Separar las fechas y los valores LDR
    fechas = [row[0] for row in data]
    valores_ldr = [row[1] for row in data]

    # Crear la gráfica
    fig, ax = plt.subplots()
    ax.plot(fechas, valores_ldr, label='Valor del LDR', color='b')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valor LDR')
    ax.set_title('Serie Temporal de Valores LDR')
    ax.grid(True)
    plt.xticks(rotation=45)

    # Guardar la gráfica en un buffer de memoria
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    # Convertir la imagen a base64 para mostrarla en HTML
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('index.html', graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)


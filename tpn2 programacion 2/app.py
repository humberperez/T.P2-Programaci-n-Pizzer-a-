from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
app = Flask(__name__,static_url_path="/static/estilo.css")

def get_db_connection():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pedidos"
        )
        cursor = connection.cursor()
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection, cursor


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pedidos")
def pedidos():
    return render_template("pedidos.html")

@app.route("/guardar_pedido", methods=["POST"])
def guardar_pedido():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_pizza = request.form['tipo_pizza']
        bebidas = request.form['bebidas']
        contacto = request.form['contacto']
        direccion = request.form["direccion"]
        envio = request.form['envio']

        # establece la conexion con la base de datos
        db_connection, cursor = get_db_connection()
        if db_connection is not None and cursor is not None:
            try:
                # prepara la consulta SQL
                insert_query = "INSERT INTO pedidos (nombre, apellido, tipo_pizza, bebidas, contacto, direccion, envio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (nombre, apellido, tipo_pizza, bebidas, contacto, direccion, envio))
                db_connection.commit()
            finally:
                # termina la conexion
                cursor.close()
                db_connection.close()

        return redirect(url_for("index"))

@app.route("/historial_pedidos")
def historial_pedidos():
    db_connection, cursor = get_db_connection()
    pedidos = []
    if db_connection is not None and cursor is not None:
        try:
            cursor.execute("SELECT id, nombre, apellido, tipo_pizza, bebidas, contacto, direccion, envio FROM pedidos")
            pedidos = cursor.fetchall()
        finally:
            cursor.close()
            db_connection.close()

    return render_template("historial_pedidos.html", pedidos=pedidos)


@app.route("/editar_pedido/<int:pedido_id>", methods=["GET", "POST"])
def editar_pedido(pedido_id):
    db_connection, cursor = get_db_connection()
    pedido = None

    if db_connection is not None and cursor is not None:
        try:
            cursor.execute("SELECT id, nombre, apellido, tipo_pizza, bebidas, contacto, direccion, envio FROM pedidos WHERE id = %s", (pedido_id,))
            pedido_data = cursor.fetchone()
            pedido = {
                'id': pedido_data[0],
                'nombre': pedido_data[1],
                'apellido': pedido_data[2],
                'tipo_pizza': pedido_data[3],
                'bebidas': pedido_data[4],
                'contacto': pedido_data[5],
                'direccion': pedido_data[6],
                'envio': pedido_data[7]
            }
        finally:
            cursor.close()
            db_connection.close()

    if pedido:
        return render_template("editar_pedido.html", pedido=pedido)
    else:
        return "Pedido no encontrado", 404


@app.route("/guardar_edicion_pedido/<int:pedido_id>", methods=["POST"])
def guardar_edicion_pedido(pedido_id):
    if request.method == "POST":
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_pizza = request.form['tipo_pizza']
        bebidas = request.form['bebidas']
        contacto = request.form['contacto']
        direccion = request.form["direccion"]
        envio = request.form['envio']

        db_connection, cursor = get_db_connection()
        if db_connection is not None and cursor is not None:
            try:
                update_query = "UPDATE pedidos SET nombre=%s, apellido=%s, tipo_pizza=%s, bebidas=%s, contacto=%s, direccion=%s, envio=%s WHERE id=%s"
                cursor.execute(update_query, (nombre, apellido, tipo_pizza, bebidas, contacto, direccion, envio, pedido_id))
                db_connection.commit()
            finally:
                cursor.close()
                db_connection.close()

        return redirect(url_for("historial_pedidos"))

    
if __name__ == "__main__":
    app.run(debug=True)

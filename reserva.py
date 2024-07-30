from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config ={
    'user':'root',
    'password':'ironhack',
    'host':'localhost',
    'database':'el_churrete_reserva'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lista_reserva')
def listReserva():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vw_reservas_Activas")
            reserva = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('reserva_lista.html', reservas=reserva)
    except:
        return "Error al conectar a la base de datos"

@app.route('/reserva/agregar',methods=['POST'])
def addReserva():
    try:
        contacto = request.form['contacto']
        email = request.form['email']
        telefono= request.form['telefono']
        fechaPrevista= request.form['fechaPrevista']
        horaPrevista= request.form['horaPrevista']
        plazas= request.form['plazas']
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            query="INSERT INTO reserva (contacto, email, telefono, fechaPrevista, horaPrevista,plazas) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (contacto, email,telefono,fechaPrevista,horaPrevista,plazas))
            cursor.close()
            conn.close()
            return render_template('reserva_lista.html', reservas=reserva)
    except:
        return "Error al conectar a la base de datos"
    
@app.route('/reserva/editar<int:id>', methods=['POST'])
def editReserva(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            query='DELETE FROM reserva WHERE id = %s"'
            cursor.execute(query, (id,))
            reserva=cursor.fetchone
            cursor.close
            conn.close
            if reserva:
                return render_template('reserva_form.html', reserva=reserva)
            else:
                return "reserva no encontrada"
           
    except:
        return "Error al conectar base de datos"

@app.route('/reserva/cancelar<int:id>', methods=['POST'])
def cancelReserva(id):
    valor=2
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            print('conectada db id ',id, ' ',valor)
            query='UPDATE reserva SET id_reservaEstado =  %s  WHERE id = %s;'
            cursor.execute(query, (valor,id))
            print('ejecutado id ',id)
            conn.commit
            cursor.close
            conn.close
            return redirect(url_for('listaReserva'))
           
    except:
        return "Error al conectar base de datos"

if __name__ == '__main__':
    app.run(debug=True)
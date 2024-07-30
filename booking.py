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

@app.route('/booking/list')
def bookingList():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vw_booking_Active")
            reserva = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('booking_list.html', reservas=reserva)
    except:
        return "Error al conectar a la base de datos"

@app.route('/booking/add',methods=['POST'])
def addReserva():
    try:
        contact = request.form['contact']
        email = request.form['email']
        phone= request.form['phone']
        expectedDate= request.form['expectedDate']
        expectedHour= request.form['expectedHour']
        people= request.form['people']
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            query="INSERT INTO reserva (contact, email, phone, expectedDate, expectedHour,people) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (contact, email, phone, expectedDate, expectedHour, people))
            cursor.close()
            conn.close()
            return redirect(url_for('bookingList'))
    except:
        return "Error al conectar a la base de datos"
    
@app.route('/booking/edit<int:id>', methods=['POST'])
def editReserva(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            query='SELECT FROM booking WHERE id = %s"'
            cursor.execute(query, (id,))
            booking=cursor.fetchone
            cursor.close
            conn.close
            if booking:
                return render_template('booking_form.html', booking=booking)
            else:
                return "reserva no encontrada"
           
    except:
        return "Error al conectar base de datos"

@app.route('/booking/cancel/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def cancelReserva(id):
    valor=2
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            print('conectada db id ',id, ' ',valor)
            query='UPDATE booking SET id_bookingState =  2  WHERE id = %s;'
            cursor.execute(query, (id,))
            conn.commit
            cursor.close
            conn.close
            print('ejecutado id ',id)
            return redirect(url_for('listBooking'))
           
    except:
        return "Error al conectar base de datos"

if __name__ == '__main__':
    app.run(debug=True)
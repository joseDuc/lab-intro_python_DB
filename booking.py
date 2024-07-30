from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config ={
    'user':'root',
    'password':'ironhack',
    'host':'localhost',
    'database':'el_churrete_booking'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking/list/')
def bookingList():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vw_booking_Active")
            booking = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('booking_list.html', bookings=booking)
    except:
        return "Error al conectar a la base de datos"

@app.route('/booking/add/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def addBooking():
    try:
        contact = request.form['contact']
        email = request.form['email']
        phone= request.form['phone']
        expectedDate= request.form['expectedDate']
        expectedHour= request.form['expectedHour']
        people= request.form['people']
        print(contact,email,phone,expectedDate,expectedHour,people)   
        conn = mysql.connector.connect(**db_config)
        print('conexion abierta')   
        if conn.is_connected():
            cursor = conn.cursor()
            query="INSERT INTO booking (id_establishment, id_bookingState, contact, email, phone, expectedDate, expectedHour, people) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (1, 1, contact, email, phone, expectedDate, expectedHour, people))
            cursor.close()
            conn.close()
            return redirect(url_for('bookingList'))
    except:
        return "Error al conectar a la base de datos"
    
@app.route('/booking/edit/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def editBooking(id):
    try:
        print('entra id ',id)
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            print('cursor db id ',id)
            query='SELECT * FROM booking WHERE id = %s'
            cursor.execute(query, (id,))
            print('execute db id ',id)
            bookings=cursor.fetchone
            cursor.close
            conn.close
            if bookings:
                return render_template('booking_form.html', booking=bookings)
            else:
                return "reserva no encontrada"
           
    except:
        return "Error al conectar base de datos"

@app.route('/booking/edited/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def editedBooking(id):
    try:
        print('entra id ',id)
        contact = request.form['contact']
        email = request.form['email']
        phone= request.form['phone']
        expectedDate= request.form['expectedDate']
        expectedHour= request.form['expectedHour']
        people= request.form['people']
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            query='UPDATE booking SET name=%s,email=%s,phone=%s,expectedDate=%s,expectedHour=%s,people=%s WHERE id = %s'
            cursor.execute(query,(contact, email, phone, expectedDate, expectedHour, people, id))
            cursor.close
            conn.close
            return redirect(url_for('bookingList'))
           
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
            return redirect(url_for('bookingList'))
           
    except:
        return "Error al conectar base de datos"

if __name__ == '__main__':
    app.run(debug=True)
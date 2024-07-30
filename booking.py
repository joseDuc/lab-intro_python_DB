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
def booking_list():
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
        return "Error al conectar a la base de datos listando"

@app.route('/booking/addX/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_addX():
    try:
        conn = mysql.connector.connect(**db_config)
        print('conexion abierta')   
        if conn.is_connected():
            cursor = conn.cursor()
            query="INSERT INTO booking (id_establishment, id_bookingState, contact, email, phone, expectedDate, expectedHour, people) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (1, 1, 'manuel', 'amail@gmail.com', '', '2024-08-01', '14:00', 4))
            cursor.close()
            conn.close()
            return redirect(url_for('booking_list'))
    except:
        return "Error al conectar a la base de datos agregando"

@app.route('/booking/add/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_add():
    try:
        print('iniciando agregar')   
        contact = request.form['contact']
        email = request.form['email']
        phone = request.form['phone']
        expectedDate = request.form['expectedDate']
        expectedHour = request.form['expectedHour']
        people = request.form['people'] 
        conn = mysql.connector.connect(**db_config)
        print('conexion abierta')   
        if conn.is_connected():
            cursor = conn.cursor()
            query="INSERT INTO booking (id_establishment, id_bookingState, contact, email, phone, expectedDate, expectedHour, people) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (1, 1, contact, email, phone, expectedDate, expectedHour, people))
            cursor.close()
            conn.close()
            return redirect(url_for('booking_list'))
    except:
        return "Error al conectar a la base de datos agregando"
    
@app.route('/booking/edit/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_edit(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            query='SELECT * FROM booking WHERE id = %s'
            cursor.execute(query, (id,))
            bookings=cursor.fetchone()
            cursor.close()
            conn.close()
            if bookings:
                return render_template('booking_form.html', booking=bookings)
            else:
                return "reserva no encontrada editando"
           
    except:
        return "Error al conectar base de datos editando"

@app.route('/booking/edited/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_edited(id):
    try:
        contact = request.form['contact']
        email = request.form['email']
        phone= request.form['phone']
        expectedDate= request.form['expectedDate']
        expectedHour= request.form['expectedHour']
        people= request.form['people']  
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            query='UPDATE booking SET contact=%s,email=%s,phone=%s,expectedDate=%s,expectedHour=%s,people=%s WHERE id = %s'
            cursor.execute(query,(contact, email, phone, expectedDate, expectedHour, people, id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('booking_list'))
           
    except:
        return "Error al conectar base de datos guardando"


@app.route('/booking/cancel/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_cancel(id):
    valor=2
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            query='UPDATE booking SET id_bookingState =  2  WHERE id = %s;'
            cursor.execute(query, (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('booking_list'))
           
    except:
        return "Error al conectar base de datos cancelando"

if __name__ == '__main__':
    app.run(debug=True)
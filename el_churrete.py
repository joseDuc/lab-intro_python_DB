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
        return "Error al conectar a la base de datos listando reserva"


@app.route('/booking/add/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_add():
    try:
        contact = request.form['contact']
        email = request.form['email']
        phone = request.form['phone']
        expectedDate = request.form['expectedDate']
        expectedHour = request.form['expectedHour']
        people = request.form['people'] 
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            query="INSERT INTO booking (id_establishment, id_bookingState, contact, email, phone, expectedDate, expectedHour, people) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (1, 1, contact, email, phone, expectedDate, expectedHour, people))
            conn.commit()
            print (cursor.lastrowid)
            cursor.close()
            conn.close()
            return redirect(url_for('booking_list'))
    except:
        return "Error al conectar a la base de datos agregando reserva"
    
    
@app.route('/booking/edit/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_edit(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            query='SELECT * FROM booking WHERE id = %s'
            cursor.execute(query, (id,))
            booking=cursor.fetchone()
            cursor.close()
            conn.close()
            if booking:
                return render_template('booking_form.html', bookings=booking)
            else:
                return (f'No se ha encontrado la reserva {id} para editar')
           
    except:
        return 'Error al conectar base de datos preparando edición reserva'


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
        return f'Error al conectar base de datos guardando reserva {id}'


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
        return 'Error al conectar base de datos cancelando reserva'


@app.route('/account/list/')
def account_list():
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            cursor.execute('SELECT * FROM account')
            account=cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('account_list.html', accounts=account)

    except:
        return 'Error al conectar base de datos listando cuenta'


@app.route('/account/new/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_new():
    return render_template('account_form_new.html')
    
    
@app.route('/account/add/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_add():
    try:
        people = request.form['people']
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            query='INSERT INTO account (id_establishment, people) VALUES (%s,%s)'
            cursor=conn.cursor()
            cursor.execute(query,(1,people))
            conn.commit()
            lastId=cursor.lastrowid
            cursor.close()
            query='SELECT * FROM account WHERE id=%s'
            cursor=conn.cursor()
            cursor.execute(query,(lastId,))
            account=cursor.fetchone()
            cursor.close()
            conn.close()

            return render_template('account_form_edit.html',accounts=account)
    except:
        return 'Error al conectar base de datos agregando cuenta'
    

@app.route('/account/edit/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_edit(id):
    try:
        conn =mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            query='SELECT * FROM account WHERE id = %s'
            cursor.execute(query,(id,))
            accounts=cursor.fetchone()
            cursor.close()
            conn.close()
            if accounts:
                return (render_template('account_form_edit.html',account=accounts))
            else:
                return f'No se ha encontrado la cuenta {id} para editar'
            
    except:
        return 'Error al conectar base de datos preparando edición cuenta'

    
@app.route('/account/edited/<int:id>', methods=['POST'])
def account_edited(id):
    try:
        people = request.form['people']
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            query='UPDATE account SET people=%s WHERE id =%s'
            cursor.execute(query,(people,id))
            conn.commit()
            cursor.close()
            query='SELECT * FROM account WHERE id=%s'
            cursor=conn.cursor()
            cursor.execute(query,(id,))
            account=cursor.fetchone()
            cursor.close()
            conn.close()

            return render_template('account_form_edit.html',accounts=account)

    except:
        return f'Error al conectar base de datos en la edición de la cuenta {id}'
    

@app.route('/account/editByIdBooking/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_editByIdBooking(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            query='SELECT * FROM account WHERE id_booking=%s'
            cursor=conn.cursor()
            cursor.execute(query,(id,))
            account=cursor.fetchone()
            cursor.close()
            conn.close()
            if account:
               return render_template('account_form_edit', accounts=account)
            else:
                return (f'No se ha encontrado la cuenta para editar con id_reserva {id} ')
            
    except:
        return 'Error al conectar base de datos preparando edición cuenta por id_reserva'
    
    
@app.route('/account/confirmEntry/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_confirmEntry(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            arg=[id]
            cursor.callproc('insertEntryDateAccount',arg)
            conn.commit()
            cursor.close()
            query='SELECT * FROM account WHERE id=%s'
            cursor=conn.cursor()
            cursor.execute(query,(id,))
            account=cursor.fetchone()
            cursor.close()
            conn.close()

            return render_template('account_form_edit.html',accounts=account)
    except:
        return 'Error al conectar base de datos al confirmar cuenta_entrada'
    
    
@app.route('/account/confirmDeparture/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_confirmDeparture(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            arg=[id]
            cursor.callproc('insertDepartureDateAccount',arg)
            conn.commit()
            cursor.close()
            query='SELECT * FROM account WHERE id=%s'
            cursor=conn.cursor()
            cursor.execute(query,(id,))
            account=cursor.fetchone()
            cursor.close()
            conn.close()

            return render_template('account_form_edit.html',accounts=account)
    except:
        return 'Error al conectar base de datos al confirmar cuenta_salida'
    
    
    
    
    
    
if __name__ == '__main__':
    app.run(debug=True)
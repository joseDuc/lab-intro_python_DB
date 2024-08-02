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
            lastId= cursor.lastrowid
            cursor.close()
            conn.close()
            return redirect(url_for('account_editByIdBooking', id=lastId))
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

@app.route('/booking/edit/None', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_edit_none():
    try:
         return  redirect(url_for('booking_list'))
        
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
            # query='UPDATE booking SET id_bookingState =  2  WHERE id = %s;'
            # cursor.execute(query, (id,))
            cursor.callproc('cancelBooking',[id])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('booking_list'))
           
    except:
        return 'Error al conectar base de datos cancelando reserva'


    
@app.route('/booking/autoCancel/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def booking_autoCancel():
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            cursor.callproc('bookingCancelingFromNotPresented')
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('booking_list'))
    except:
        return 'Error al conectar base de datos para hacer cancelación automática'
    
    
@app.route('/account/list/')
def account_list():
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor=conn.cursor()
            cursor.execute('SELECT * FROM account  WHERE canceled IS NULL AND departureDate IS NULL')
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
            query ='SELECT IdAccountFromIdBooking(%s)'
            cursor.execute(query,(id,))
            i=account=cursor.fetchone()
            print ('idCta=',i)
            query='SELECT * FROM account WHERE id = %s'
            cursor.execute(query,(id,))
            account=cursor.fetchone()
            cursor.close()
            conn.close()
            if account:
                return (render_template('account_form_edit.html',accounts=account))
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
        print ('id=',id)
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            query='SELECT * FROM account WHERE id_booking=%s'
            cursor=conn.cursor()
            cursor.execute(query,(id,))
            account=cursor.fetchone()
            cursor.close()
            conn.close()
            print ('conexion cerrada')
            if account:
               return render_template('account_form_edit.html', accounts=account)
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
            return redirect(url_for('account_list'))            

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
            return redirect(url_for('account_list'))        

    except:
        return 'Error al conectar base de datos al confirmar cuenta_salida'
    
    
    

@app.route('/account/diningTableAssign/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_diningTableAssign(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            cursor.callproc('reservationDiningTableFromNextBooking')
            cursor.execute('SELECT * FROM vw_diningtable_free')
            freeDiningTable=cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('diningTable_list.html', freeDiningTables=freeDiningTable, account=id )
    except:
        return 'Error al conectar base de datos al listar mesa de la cuenta'
    
    
@app.route('/account/diningTableAdd/<int:id>/<int:idDiningTable>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_diningTableAdd(id,idDiningTable):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            args=(id,idDiningTable)
            cursor.callproc('addDiningTableAccount',args)
            conn.commit()
            cursor.close
            cursor=conn.cursor()
            cursor.execute('SELECT * FROM vw_diningtable_free')
            freeDiningTable=cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('diningTable_list.html', freeDiningTables=freeDiningTable, account=id )
    except:
        return 'Error al conectar base de datos al listar mesa de la cuenta'
    
@app.route('/account/diningTableDel/<int:id>/<int:idDiningTable>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_diningTableDel(id,idDiningTable):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            query ='DELETE FROM accountDiningTable WHERE id_account=%s AND id_diningTable=%s'
            cursor.execute(query,(id,idDiningTable)) # AND id_diningTable=%s',(id,diningTable))
            conn.commit()
            # cursor.execute('SELECT * FROM vw_diningtable_free')
            # freeDiningTable=cursor.fetchall()
            # cursor.close()
            # conn.close()
            # return redirect('account_diningTable',id=id)
            # return redirect(url_for('account_diningTable',id: id}) 
            # return render_template('diningTable_list.html', freeDiningTables=freeDiningTable, account=id )
            
            query='SELECT * FROM accountDiningTable WHERE id_account=%s'
            cursor.execute(query,(id,))
            accountDiningTable=cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('account_diningTable.html', accountDiningTables=accountDiningTable, account=id )
    except:
        return 'Error al conectar base de datos al listar mesa de la cuenta'
    
    
@app.route('/account/diningTable/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def account_diningTable(id):
    try:
        conn=mysql.connector.connect(**db_config)
        if conn.is_connected:
            cursor=conn.cursor()
            # query = '''
            #     'SELECT em.name as establishment ,dt.id as idTable ,f.name as planta, z.name as zona, dt.name as mesa, dt.people, e.name as state 
            #     FROM accountDiningTable at
            #     join diningTable dt on dt.id=at.id_diningTable
            #     join zone z on z.id=dt.id_zone
            #     join floor f on f.id=z.id_floor
            #     join establishment em on em.id=f.id_establishment
            #     join diningTableState e on e.id=dt.id_diningTableState
            #     WHERE id_account = %s
            #     order by em.name, f.value, z.name, dt.name, dt.people
            # '''
            query='SELECT * FROM accountDiningTable WHERE id_account=%s'
            cursor.execute(query,(id,))
            accountDiningTable=cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('account_diningTable.html', accountDiningTables=accountDiningTable, account=id )
    except:
        return 'Error al conectar base de datos al listar mesa de la cuenta'
    
    
if __name__ == '__main__':
    app.run(debug=True)
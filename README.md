# Gestión de reservas del restaurante El Churrete

### Sobre mí

        Tengo 61 años y he pasado los últimos veintipico de años programando primero en Visual Basic 6.0 y los últimos 4 años desarrollando en Visual Basic .NET. He trabajado normalmente con Sql Server para la gestión de bases de datos.

        Mi esperiencia en la web no es muy extensa. Creé un servicio de presupuestos en línea para la empresa donde trabajé 21 años y que desde el Mayo de este año canceló mi contrato por un severo ERE.

### Objetivo de la aplicación

    Este software permite acceder al entorno de datos de las reservas de un restaurante y gestionar sus movimientos.

    He preferido este tema, porque me llamó la atención la mecánica producida al sincronizar los datos de varias relaciones y por la necesidad de mantener una coherencia permanente de los datos, en este caso utilizando los triggers y procedimientos en mySql.

### Herramientas utilizadas

- ### MySql
        Ágil para convertir en esquema el modelo conceptual y relacional del proyecto.
- ### Python
        Lenguaje para establecer la lógica del tráfico de datos de ida y vuelta y conectar con las bases de datos.
- ### Flask
        En la inyección de datos desde back-end en los elementos HTML a través de listas y formularios antes de su salida.
- ### HTML.5 
        En la maquetación de los diferentes formularios y listas que se precisan para manipular los datos y navegar por todo su ámbito mediante el navegador que facilita cada página.
- ### CSS.3 
        Para conseguir un centrado visual de los objetos sin pretensión decorativa en este caso.
- ### ECMAScript 2023 de Node.js 'v20.14.0'
        Lenguaje para programar algunas de las acciones de ámbito local dentro del alcance de cada página.
- ### GitHub
        Para publicar el proyecto en repositorios compartidos que permiten el acceso periódico a otros colaboradores.

### Esquema del modelo relacional de datos del proyecto
        En esta imagen se aprecia el desarrollo del concepto de las reservas de un restaurante.

![imagen](/img/ER.png)

    Representa los modelos relacionales necesarios para establecer una reserva.
    En el instante de crear una reserva, se abre una nueva cuenta única para esa nueva reserva.

    Cuando se activa una reserva, los parámetros más relevantes, son la fecha y hora esperadas y las plazas que ocuparán.
    Se ha de preservar la existencia de esas plazas libres para el momento de la entrada de los clientes.

    Se han creado los procedimientos y funciones necesarias para que MySql mediante este esquema, sincronice esas modificaciones.
    
    Al ir aproximándose al momento de la reserva y con un tiempo de anticipación equivalente a una comida relajada, se han de reservar, mediante un procedimiento existente, las mesas asignadas a sus correspondientes cuentas según las horas de llegada que indiquen las reservas asociadas.

    Es común que algunas reservas puedan no haber sido consumadas por la no asistencia de sus clientes, pero hasta que no haya transcurrido un tiempo prudencial, no se deben auto-cancelar. Si traspasa esa tolerancia temporal y no asiste el cliente, serán canceladas.

    Para ello existe un procedimiento que resuelve las reservas sin asistencia y libera las mesas que hubieran sido reservas para su uso, bajo unos criterios de comparación en los intervalos de tiempo con las reservas. 

    Existe una vista de datos que selecciona las reservas activas y antepone la ejecución de este procedimiento comentado anteriormente, para asegurar que la nueva lectura de la vista, arrastre las reservas adecuadas, con las citas esperadas dentro del intervalo de tiempo actual, en este caso sólo las que no están canceladas. 

### Servicio ofrecido por el back-end

        La primera tarea del back es preparar la configuración de conexión a datos.

        El inicio de la aplicación es la página principal que se sirve en el primer contacto con el usuario, está preparada con un formulario de nueva reserva. Es el inicio del preceso, crear reservas.

![imagen](/img/Main.png)

        No es necesario crear siempre una reseva. Hay entrada de clientes de forma espontánea. En ese caso, el navegador nos permite saltar al formulario de nueva cuenta. Requiere el número de personas para incluirlas en la cuenta y poder asignar las mesas necesarias para cubrir esas plazas.

![imagen](/img/AccountNew.png)

        Para asignar las mesas de la cuenta, el formulario posee un enlace para acceder a la lista de mesas desocupadas. Desde esta lista se pueden ir asignando una a una las mesas precisas.
        Para ver las mesas asignadas a una cuenta determinada, desde el formulario de edición de cuenta se puede acceder mediante un enlace.

![imagen](/img/DiningTableFree.png)

        Al crear una reserva, se crea instantáneamente su cuenta correspondiente. Es desde la cuenta que se han de asignar las mesas. 
        Al llegar el cliente es importante que quede constancia informáticamente, por eso es necesario desde el formulario de editar cuenta, confirmar la llegada pulsando el botón que hay para su efecto.
        Lo mismo para la salida del cliente, se ha de confirmar pulsando un botón que hay para su efecto.

![imagen](/img/AccountEdit.png)

![imagen](/img/AccountDiningTable.png)

        La confirmación de entrada fuerza en caso de que exista una reserva relacionada, que esta pase al estado de consumada. Su función como reserva, a terminado.
        La confirmación de salida fuerza a liberar las mesas, pasando al estado de desocupadas.

        La vista de datos que muestra las reservas activas, se encarga de actualizar previamente el estado de las mesas asignadas mediante la aproximación en el tiempo, utilizando un intervalo constante de comparación que va pasando las mesas candidatas al estado de reservada.

        Cuando es necesario cancelar una reserva, se puede gestionar desde la lista de reservas. En esta lista cada reserva tiene su propio botón de cancelación.
        Esta operación cancelará seguidamente la cuenta correspondiente y liberará las mesas reservadas.

![imagen](/img/BookingList.png)

![imagen](/img/AccountList.png)

        Tanto las cuentas como las reservas cuentan con su formulario de edición.

![imagen](/img/BookingEdit.png)

        Aunque básicamente estas son las funciones que realiza el back-end actualmente, la forma en la que se ha desarrollado, permite ampliar el tipo de información y la forma de solicitarla para mejorar la experiencia del usuario.

#### Rutas habilitadas 

        El inicio
        @app.route('/')

        La lista de reservas
        @app.route('/booking/list/')
        
        Para agregar una reseva
        @app.route('/booking/add/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Para editar la reserva
        @app.route('/booking/edit/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Cuando no envía código de reserva, esta ruta reconduce al usuario
        @app.route('/booking/edit/None', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Cuando la reserva está editada, esta ruta se encarga de guardarla en la base de datos
        @app.route('/booking/edited/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Para cancelar una reserva
        @app.route('/booking/cancel/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        LLama a un procedimiento de la base de datos que cancela automáticamente según un criterio
        @app.route('/booking/autoCancel/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Lista de cuenta
        @app.route('/account/list/')

        Sirve nueva cuenta
        @app.route('/account/new/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Agrega la nueva cuenta en la basde de datos
        @app.route('/account/add/', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Poner en una cuenta edición 
        @app.route('/account/edit/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Se guarda la edición de la cuenta en la basde de datos
        @app.route('/account/edited/<int:id>', methods=['POST'])

        Poder encontrar una cuenta por el código de reserva para ponerla en edición
        @app.route('/account/editByIdBooking/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Confirma la entrada del cliente en la cuenta
        @app.route('/account/confirmEntry/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Conforma la salida del cliente en la cuenta
        @app.route('/account/confirmDeparture/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Lista de mesas desocupadas para seleccionar las que se asignarán a la cuenta del id
        @app.route('/account/diningTableAssign/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
        
        Agrega las mesas asignadas a la cuenta del id
        @app.route('/account/diningTableAdd/<int:id>/<int:idDiningTable>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

        Elimina la tabla asignada de la cuenta del id
        @app.route('/account/diningTableDel/<int:id>/<int:idDiningTable>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
        
        Lista las mesas asignadas a la cuenta del id
        @app.route('/account/diningTable/<int:id>', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])

### Mi impresión

        Esta actividad me ha dado una visión completa de las partes relevantes de los elementos de una web
        con servicio de back-end.
        Ejercitando la abstracción en la idea del proyecto, para ir construyendo por partes la estructura.

        Es tan solo un paso más para depurar los conceptos y afianzar los conocimientos fundamentales de la programación en general y en la web en particular.

        
        









# Gestión de reservas del restaurante El Churrete

### Objetivo de la aplicación

    Este software permite acceder al entorno de datos de las reservas de un restaurante.

    He preferido este tema, porque me llamó la atención la mecánica que se ha de producir para sincronizar los datos de varias relaciones, por la necesidad de mantener una coherencia permanente de los datos, en este caso mediante los triggers en mySql.

### Herramientas utilizadas

- ### MySql
        Para el desarrollo del modelo conceptual y relacional.
- ### Python
        Lenguaje para establecer una lógica de tráfico de datos de ida y vuelta.
- ### Flask
        Para inyectar datos en los elementos HTML mediante listas y formularios.
- ### HTML.5 
        En la maquetación de los diferentes formularios y listas que se precisan para manipular los datos y navegar a través del navegador, por el índice de la web.
- ### CSS.3 
        Conseguir un centrado de los objetos sin pretensión decorativa.
- ### ECMAScript 2023 de Node.js 'v20.14.0'
        Lenguaje para programar en este proyecto, las acciones de ámbito local dentro de las páginas.
- ### GitHub
        Para mantener el proyecto al alcance de otros colaboradores periódicamente.

### EL esquema del modelo relacional de datos del proyecto
![imagen](/img/esquemaRelacional.png)

    Representa los modelos relacionales necesarios para establecer una reserva.
    En ese instante, se abre una nueva cuenta única para esa nueva reserva.

    Cuando se activa una reserva, los parámetros más relevantes, son la fecha y hora esperadas y las plazas que ocuparán.
    Se ha de preservar la existencia de esas plazas libres para el momento de la entrada de los clientes.

    Se han creado los procedimientos y funciones necesarias para que MySql mediante este esquema, sincronice esas modificaciones.
    
    Al ir aproximándose el momento de la reserva y con un tiempo de anticipación equivalente a una comida lenta, se han de reservar mediante un procedimiento existente, las mesas asignadas a las cuenta relacionadas con sus reservas.

    Es común que algunas reservas puedan no haber sido consumadas por la ausencia de sus clientes, pero hasta que no haya transcurrido un tiempo prudencial, no se deben auto-cancelar.

    Para ello existe un procedimiento que resuelve las reservas no presentadas y libera las mesas que hubieran sido reservas para su uso bajo unos criterios en los intervalos de tiempo comparados en las reservas. 

    Existe una vista que selecciona las reservas activas y antepone este procedimiento anterior, para asegurar que la nueva lectura de la vista, arrastra las reservas adecuadas, con las citas esperadas dentro del intervalo de tiempo actual, en este caso no canceladas por el procedimiento previo de cancelación.
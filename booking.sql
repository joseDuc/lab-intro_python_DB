drop schema if exists el_churrete_booking;
create schema if not exists el_churrete_booking;

use el_churrete_booking;

-- one_to_many con establecimiento 
create table entity(
id smallint unsigned auto_increment,
cif varchar(15) not null,
name varchar(100) unique not null,
id_mainEstablishment smallint unsigned,
primary key(id)
);

-- one_to_many con planta y otras 
create table establishment(
id smallint unsigned auto_increment,
id_entity smallint unsigned not null,
name varchar(100) not null,
address varchar(255),
email varchar(100),
phone varchar(20),
constraint fk_id_entity_establishment foreign key(id_entity) references entity(id),
unique idx_id_entity_name_establishment (id_entity, name),
primary key(id)
);

alter table entity
add constraint fk_id_mainEstablishment_entity foreign key (id_mainEstablishment) references establishment(id);

-- one_to_many con zona 
create table floor(
id smallint unsigned auto_increment,
id_establishment smallint unsigned not null,
value tinyint unsigned not null,
name varchar(100) not null,
constraint fk_id_establishment_floor foreign key(id_establishment) references establishment(id),
primary key(id),
unique idx_establishment_value (id_establishment,value)
); 

-- one_to_many con mesa 
create table zone(
id smallint unsigned auto_increment,
id_floor smallint unsigned,
name varchar (100),
constraint fk_id_floor_zone foreign key(id_floor) references floor(id),
primary key(id),
unique idx_floor_name (id_floor,name)
);

create table diningTableState(
id tinyint unsigned auto_increment,
name varchar(20) not null unique,
primary key (id)
);

-- one_to_many con cuentamesa , la mesa puede aparecer en varias cuentaMesa
create table diningTable(
id smallint unsigned auto_increment,
id_zone smallint unsigned,
id_diningTableState tinyint unsigned,
name varchar(20),
people tinyint unsigned,
constraint fk_id_zone_diningTable foreign key(id_zone) references zone(id),
constraint fk_id_diningTableState_diningTable foreign key(id_diningTableState) references diningTableState(id),
primary key(id),
unique idx_zone_name (id_zone,name)
);

-- one_to_many con reserva , one_to_one con comensalObs bidireccional
create table diner(
id int unsigned auto_increment,
id_dinerObs int unsigned,
name varchar(100),
email varchar(100) unique,
phone varchar(20),
primary key(id)
);

-- one_to_one con comensal bidireccional, datos complementarios 
create table dinerObs(
id_diner int unsigned unique,
obs varchar(255),
primary key(id_diner)
);

-- agrego constraint bidireccional porque anteriormente no era posible al no existir aún la tabla comensalObs
alter table diner 
add constraint fk_id_diner_dinerObs foreign key(id_dinerObs) references dinerObs(id_diner);

-- one_to_many con reserva
create table bookingState(
id tinyint unsigned auto_increment,
name varchar(20) unique not null,
primary key(id)
);

-- one_to_one con cuenta
create table booking (
id int unsigned auto_increment,
id_establishment smallint unsigned not null,
id_bookingState tinyint unsigned not null,
contact varchar(100) not null,
email varchar(100) not null,
phone varchar(20),
contactDate datetime not null default now(),
expectedDate date not null,
expectedHour time not null,
people smallint not null,
canceledReason varchar(100),
primary key(id),
constraint fk_id_establishment_booking foreign key (id_establishment) references establishment(id),
constraint fk_id_bookingState_booking foreign key (id_bookingState) references bookingState(id)
);

-- one_to_one con reserva, one_to_many con mesas ocupadas por la cuenta
create table account(
id int unsigned auto_increment,
id_establishment smallint unsigned not null,
id_booking int unsigned unique,
entryDate datetime,
departureDate datetime,
people smallint not null,
primary key(id),
constraint fk_id_establishment_account foreign key (id_establishment) references establishment(id),
constraint fk_id_booking_account foreign key (id_booking) references booking(id),
index idx_id_booking_account (id_booking)
);

create table accountDiningTable(
id_account int unsigned,
id_diningTable smallint unsigned,
expectedDate date not null,
expectedHour time not null,
constraint fk_id_account_accountDiningTable foreign key(id_account) references account(id),
constraint fk_id_diningTable_accountDiningTable foreign key(id_diningTable) references diningTable(id),
primary key(id_account,id_diningTable)
);



delimiter //

-- al crear una reserva se ha de crear una cuenta
create procedure createAccountFromBooking (idEstablishment smallint, idBooking int, people tinyint)  
begin
	if idBooking>0 then
		insert into account (id_establishment, id_booking, people) values (idEstablishment, idBooking, people);
	end if;
end //
-- fin procedure

create procedure occupyDinnerTableFromAccountStarted (idAccount int)
begin
	-- select * from mesa where id_mesaEstado in(1,2) and id in(select id_mesa from cuentaMesa where id_cuenta=idCuenta) for update;
	update diningTable set id_diningTableState=3 where id_diningTableState in(1,2) and  id in(
	select id_diningTable from accountDiningTable where id_account=idAccount);
end //
-- fin procedure

create procedure freeDinnerTableFromAccountFinished(idAccount int)
begin
	-- select * from mesa where id_mesaEstado in(2,3) and id in(select id_mesa from cuentaMesa where id_cuenta=idCuenta)  for update;
	update diningTable set id_diningTableState=1 where id_diningTableState in(2,3) and id in(
	select id_diningTable from accountDiningTable where id_account=idAccount);
end //
-- fin procedure

create procedure freeDinnerTableFromBookingCancelled(idBooking int)
begin
	declare idAcc int;
	set idAcc=(select id from account where id_booking=idBooking);
	if idAcc>0 then
		call freeDinnerTableFromAccountFinished(idAcc);
	end if;
end //
-- fin procedure

create procedure bookingAccomplished(idBooking int)
begin
	update booking set id_bookingState=3
	where id_bookingState=1 and id = idBooking;
end //

create procedure bookingCancelingFromNotPresented()
begin
	update diningTable set id_diningTableState=1
	where id_diningTableState=2 and id in(
		select id_diningTable from accountDiningTable where id_account in(
		select account.id from booking, account where not id_bookingState=3 and booking.id=account.id_booking
		and expectedHour<date_add(current_time(), interval 20 minute ) and expectedDate<=current_date()
		and entrydate is null)
	);
	
	update booking, account set id_bookingState=2, canceledReason='autómatic'
	where id_bookingState=1 and booking.id =account.id_booking and expectedDate<=current_date()
	and expectedHour<date_add(current_time(), interval 20 minute )
	and entrydate is null;
end //

CREATE procedure reservationDinerTableFromNextBooking() 
 begin
 	update diningTable set id_diningTableState =2
	where id_diningTableState=1 and id in (select id_diningTable from accountDiningTable 
	where id_account in(select id from account 
	where id in (select id from booking where id_bookingState=1 
	and expectedDate=current_date()
	and (expectedHour>= date_add(current_time(),interval -120 minute) 
	and expectedHour < date_add(current_time(),interval 20 minute))
	)));
 end //
-- fin procedure
 

create trigger creatingBooking 
after insert on booking
FOR EACH row
begin 
	call createAccountFromBooking(new.id_establishment,new.id, new.people);
end //
-- fin trigger

create trigger modifyingBooking
after update on booking
for each row 
begin 
	if old.id_bookingState <> new.id_bookingState and new.id_bookingState=2 then  -- cancelada
		call freeDinnerTableFromBookingCancelled (new.id);
	end if;
end //
-- fin trigger

create trigger modifyingAccount
after update on account
FOR EACH row
begin
	if old.entrydate is null and new.entrydate>0 then 
		call occupyDinnerTableFromAccountStarted(new.id);
		call bookingAccomplished(new.id);
	end if;
	if old.departureDate is null and new.departureDate>0 then 
		call freeDinnerTableFromAccountFinished(new.id);
		
	end if;
end //
-- fin trigger


create function IdAccountFromIdBooking(idBooking int) returns int
READS SQL DATA
begin
	declare idAcc int;
	select id into idAcc from account where id_booking=idBooking;
	return idAcc;
end //
-- fin function

delimiter ;


create view vw_diningTable_free as
select m.id , z.name as zone ,m.people , m.name, e.name as state
from el_churrete_booking.diningTable m 
join el_churrete_booking.zone z on z.id=m.id_zone
join el_churrete_booking.diningTableState e on e.id=m.id_diningTableState
where id_diningTableState=1
order by z.id, m.people;


create view vw_booking_Active as 
select r.id, e.name as establishment, r.contactDate, r.expectedDate, r.expectedHour, r.people, re.name as state, r.contact, r.email
from el_churrete_booking.booking r 
join el_churrete_booking.establishment e on e.id=r.id_establishment
join el_churrete_booking.bookingState re on re.id=r.id_bookingState
where id_bookingState=1
order by r.expectedDate, r.expectedHour, r.contactDate;

create view vw_peopleUnoccupied as 
select z.name as zone, count(m.people)
from diningTable m 
join zone z on z.id=m.id_zone
where id_diningTableState=1
group by z.id;

create view vw_diningTableBusy as 
select z.name as zone, m.name as diningTable, m.people, c.entrydate, c.departureDate, cm.id_account as account, c.id_booking as booking, cm.expectedDate, cm.expectedHour
from diningTable m 
join accountDiningTable cm on cm.id_diningTable=m.id
join account c on c.id=cm.id_account
join zone z on z.id =m.id_zone
where id_diningTableState in (2,3)
order by z.id, m.people, m.name;

-- inicio una transacción al hacer una inyección de datos grande y multitabla y evitar inconsistencias de los datos
start transaction;

-- inserto entidades
insert into entity (name,cif) values
('El Churrete','B23412323');

-- inserto sus establecimientos o franquicias
insert into establishment (id_entity,name,address,email,phone) values
(1,'Pineda 1','cl/ Los Claveles, 15 14001 Córdoba','pineda1@el_churrete.com','957 471 577'),
(1,'Pineda 2','av/ Del Cortijo, 34 14002 Córdoba','pineda2@el_churrete.com','957 471 688');


-- despues de crear los establecimientos asigno el que es principal o sede de la entidad
update entity set id_mainEstablishment=1; 

-- inserto las plantas de los establecimientos
insert into floor (id_establishment,value, name) values
(1,0,'principal'),
(2,0,'principal');

-- inserto las zonas de cada planta
insert into zone (id_floor,name) values
(1,'central'),
(1,'discreta'),
(1,'terraza interior'),
(1,'terraza exterior'),
(2,'central'),
(2,'vista jardín'),
(2,'terraza');

-- inserto los posibles estados de la mesa
insert into diningTableState (name) values
('desocupada'),
('reservada'),
('ocupada'),
('deshabilitada');

-- inserto mesas por zona y establezco el estado en desocupada
insert into diningTable (id_zone,name,people,id_diningTableState) values
(1,'001',4,1),
(1,'002',4,1),
(1,'003',6,1),
(1,'004',6,1),
(1,'005',4,1),
(1,'006',4,1),
(1,'007',4,1),
(1,'008',6,1),
(1,'009',6,1),
(1,'010',4,1),
(2,'001',2,1),
(2,'002',4,1),
(2,'003',2,1),
(2,'004',2,1),
(3,'001',4,1),
(3,'002',4,1),
(3,'003',4,1),
(3,'004',4,1),
(4,'001',4,1),
(4,'002',4,1),
(4,'003',4,1),
(4,'004',2,1);

insert into bookingState (name) values
('activa'),
('cancelada'),
('consumada');

insert into booking (id_establishment, id_bookingState, expectedDate, expectedHour, people, contact, email) values
(1, 1, current_date(), '15:00', 6, 'Pérez','jperez@gmail.com'),
(1, 1, current_date(), '13:30', 3, 'Montilla','ricardoMontilla@gmail.com'),
(1, 1, current_date(), '14:00', 4, 'García','luisGarcia@gmail.com'),
(1, 1, current_date(), '14:30', 4, 'Benegas','ignacioBenega@gmail.com'),
(1, 1, current_date(), '15:20', 2, 'Sanchis','jperz@gmail.com'),
(1, 1, current_date(), '14:30', 4, 'Blanco','lorenzoBlanco@gmail.com'),
(1, 1, current_date(), '15:30', 2, 'Torres','angelTorres@gmail.com'),
(1, 1, current_date(), '13:30', 5, 'Flores','pedroTorres@gmail.com'),
(1, 1, current_date(), '16:00', 4, 'Reyes','manuelReyes@gmail.com'),
(1, 1, current_date(), '14:00', 4, 'Del Río','pabloDelRio@gmail.com');


insert into accountDiningTable (id_account,  id_diningTable, expectedDate, expectedHour) values
(1,21, current_date(), '15:00'),
(1,22, current_date(), '15:00'),
(2,1, current_date(), '13:30'),
(3,2, current_date(), '14:00'),
(4,5, current_date(), '14:30'),
(5,11, current_date(), '15:20'),
(6,4, current_date(), '14:30'),
(7,13, current_date(), '15:30'),
(8,8, current_date(), '13:30'),
(9,15, current_date(), '15:00'),
(10,16, current_date(), '14:00');


commit;

rollback;

use el_churrete_booking;
-- esto representa que entran los comensales y hace que se ocupen las mesas relacionadas a las cuentas 1,2 y 5
update account set entrydate=now() where id in(1,2,5);

call reservationDinerTableFromNextBooking; -- si la hora prevista es la de hoy +  horaActual - 120 minutos, reservará la mesas (2 horas por si acaso)
select * from vw_diningTable_free;
select * from vw_booking_Active;
select * from vw_peopleUnoccupied;
select * from vw_diningTableBusy;
select IdAccountFromIdBooking(6);
 -- call bookingCancelingFromNotPresented;

 -- cancela la reserva 8
update booking set id_bookingState=2 where id=8;
select * from el_churrete_booking.booking;

INSERT INTO booking (id_establishment, id_bookingState, contact, email, phone, expectedDate, expectedHour, people) VALUES
             (1, 1, 'manuel', 'amail@gmail.com', '', current_date(), '14:00', 4);
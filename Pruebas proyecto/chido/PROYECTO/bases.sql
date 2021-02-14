create database reloj;
create database base1;

use reloj;
create table hora_central (
    id INT unsigned primary key,
    h_prev VARCHAR(8),
    h_ref VARCHAR(8)
);
create table equipos(
	id int unsigned auto_increment primary key,
	ip varchar(15),
	nombre varchar(50),
	latencia int
);
insert into equipos(ip,nombre,latencia) values ('10.100.76.50','Usuario 1',5);
insert into equipos(ip,nombre,latencia) values ('127.0.0.1','Usuario 2',5);
insert into equipos(ip,nombre,latencia) values ('10.100.76.66','Usuario 3',5);

create table hora_equipos(
	id int unsigned auto_increment,
	id_h_sinc int unsigned,
	id_equipo int unsigned,
	h_equipo varchar(8),
	acelerar char(2),
	realentizar char(2),
    primary key (id),	
	FOREIGN KEY(id_h_sinc) REFERENCES hora_central (id),
	FOREIGN KEY(id_equipo) REFERENCES equipos (id)
);

use base1;
create table frecuencias (
	id          INT AUTO_INCREMENT,
	front_end   int ,
	numero      int ,
	frecuencia  int ,
	ip	        VARCHAR(15),
	puerto      VARCHAR(5),
	hora        VARCHAR(9),
	PRIMARY KEY(id,front_end,numero)
);

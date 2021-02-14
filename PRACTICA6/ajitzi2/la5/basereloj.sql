create database Reloj;
use reloj;
-- drop database Reloj;
CREATE TABLE HoraCentral
(id int unsigned auto_increment not null,
  hPrev varchar(9) not null,
  hRef varchar(9) not null,
PRIMARY KEY (id));
CREATE TABLE HoraEquipos
(idhe int unsigned auto_increment not null,
  idhsincr int unsigned not null,
  idequipo int unsigned not null,
  hEquipo varchar(9) not null,
  aEquipo varchar(9) not null,
  ralentizar int,
PRIMARY KEY (idhe));
CREATE TABLE Equipos
(ideq int unsigned auto_increment not null,
ip varchar(17) not null,
  nombre varchar(30) not null,
  latencia int,
PRIMARY KEY (ideq));
select * from Equipos;
ALTER TABLE HoraEquipos ADD FOREIGN KEY (idhsincr) REFERENCES HoraCentral(id);
ALTER TABLE HoraEquipos ADD FOREIGN KEY (idequipo) REFERENCES Equipos(ideq);


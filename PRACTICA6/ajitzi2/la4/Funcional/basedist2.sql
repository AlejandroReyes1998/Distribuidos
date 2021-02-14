-- drop database base1;
-- drop database base2;
create database base1;
create database base2;
use base1;
CREATE TABLE info
(id int unsigned auto_increment not null,
  ip varchar(17) not null,
  puerto varchar(7) not null,
  jugador int,
  hora varchar(9) not null, 
  resultado int,
PRIMARY KEY (id));
use base2;
CREATE TABLE info
(id int unsigned auto_increment not null,
  ip varchar(17) not null,
  puerto varchar(7) not null,
  jugador int,
  hora varchar(9) not null, 
  resultado int,
PRIMARY KEY (id));
select * from info;
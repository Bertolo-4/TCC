CREATE DATABASE simplecode;
USE  simplecode;


CREATE TABLE usuario (
id_usuario bigint not null auto_increment primary key, 
nome varchar(255) not null, 

email varchar(255) not null unique, 
senha varchar(255) not null
);

CREATE TABLE exercicio(
id_exercicio bigint not null auto_increment primary key, 
titulo varchar(255) not null, 
enunciado varchar(255) not null
); 

CREATE TABLE exercicioAdaptado(
id_exercicioAdap bigint not null auto_increment primary key, 
tituloAdap varchar(255) not null, 
enunciadoAdap varchar(255) not null
);

select * FROM usuario;
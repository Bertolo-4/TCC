CREATE DATABASE simplecode;
USE  simplecode;


CREATE TABLE usuario (
id_usuario bigint not null auto_increment primary key, 
nome varchar(255) not null, 
email varchar(255) not null unique, 
senha varchar(255) not null
);

select * FROM usuario;

CREATE TABLE perfil_aluno (
id_perfil bigint not null auto_increment primary key, 
id_usuario bigint not null, 
dificuldades text,
facilidades text,
foreign key (id_usuario) references usuario (id_usuario)
);


CREATE TABLE exercicio (
id_exercicio bigint not null auto_increment primary key,
titulo varchar(255) not null,
enunciado text not null, 
linguagem varchar(50) default 'Java'
);

CREATE TABLE exercicio_adaptado(
id_adaptado bigint not null auto_increment primary key,
id_usuario bigint not null,
id_exercicio bigint not null, 
enunciado_adaptado text not null,
foreign key (id_usuario) references usuario (id_usuario),
foreign key (id_exercicio) references exercicio (id_exercicio)
);

CREATE TABLE codigo_resposta (
id_resposta bigint not null auto_increment primary key,
id_usuario bigint not null,
id_exercicio bigint not null, 
codigo_submetido text not null,
codigo_corrigido text,
feedback text,
foreign key (id_usuario) references usuario (id_usuario),
foreign key (id_exercicio) references exercicio (id_exercicio)
);

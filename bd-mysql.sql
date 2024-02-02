CREATE DATABASE IF NOT EXISTS usuarios;
USE usuarios;

CREATE TABLE usuarios(
    id_usuario  int(255) auto_increment not null,
    usuario varchar(255),
    password_user varchar(500),
    CONSTRAINT pk_user PRIMARY KEY(id_usuario)

) ENGINE=InnoDb;
create database Panaderia;
use Panaderia;

create table Gerente(
id_gerente int primary key auto_increment,
correo_electronico varchar(50) not null,
nombre_gerente varchar(30) not null
);


CREATE TABLE materia_prima (
    id_materia_prima INT AUTO_INCREMENT PRIMARY KEY,
    nombre_mp VARCHAR(100) NOT NULL,
    distribuidor VARCHAR(100) NOT NULL,
);


CREATE TABLE producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL
);



CREATE TABLE producto_materia_prima (
    id_producto INT NOT NULL,
    id_materia_prima INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_producto, id_materia_prima),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_materia_prima) REFERENCES materia_prima(id_materia_prima)
);



CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nombre_pedido VARCHAR(100) NOT NULL,
    estado_pedido VARCHAR(50) NOT NULL,
    cliente VARCHAR(100) NOT NULL,
    fecha_pedido DATE NOT NULL,
    id_gerente INT,
    FOREIGN KEY (id_gerente) REFERENCES Gerente(id_gerente)
);


CREATE TABLE detalle_pedido (
    id_detalle_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

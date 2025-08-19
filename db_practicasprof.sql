create database Panaderia;
use Panaderia;

create table Gerente(
id_gerente int primary key auto_increment,
correo_electronico varchar(50) not null,
nombre_gerente varchar(30) not null
);

create table Pedido(
id_pedido int primary key auto_increment,
nombre_pedido varchar(40) not null,
estado_pedido varchar(30) not null,
precio int,
tipo_pedido varchar(50) not null,
cliente varchar(50) not null,
cantidad int,
fecha_pedido date,
id_gerente int
);

create table Detalle_pedido(
id_detalle_pedido int primary key auto_increment,
cantidad int,
id_pedido int,
id_producto int
);

create table Producto(
id_producto int primary key auto_increment,
nombre_producto varchar(40) not null,
cantidad int
);

create table MateriaPrima_Producto(
cantidad int,
unidad int,
id_producto int,
id_materia_prima int
);

create table MateriaPrima(
id_materia_prima int primary key auto_increment,
distribuidor varchar(40) not null,
nombre_materia_prima varchar(50) not null
);


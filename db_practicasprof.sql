
CREATE TABLE Gerente (
    id_gerente INT AUTO_INCREMENT PRIMARY KEY,
    correo_electronico VARCHAR(50) NOT NULL UNIQUE,
    nombre_gerente VARCHAR(60) NOT NULL
) ENGINE=InnoDB;


CREATE TABLE unidad (
    id_unidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;


CREATE TABLE MateriaPrima (
    id_materia_prima INT AUTO_INCREMENT PRIMARY KEY,
    nombre_mp VARCHAR(100) NOT NULL,
    distribuidor VARCHAR(100) NOT NULL,
    id_unidad INT NOT NULL,
    FOREIGN KEY (id_unidad) REFERENCES unidad(id_unidad)
) ENGINE=InnoDB;


CREATE TABLE Producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;


CREATE TABLE MateriaPrima_producto (
    id_producto INT NOT NULL,
    id_materia_prima INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_producto, id_materia_prima),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_materia_prima) REFERENCES MateriaPrima(id_materia_prima)
) ENGINE=InnoDB;


CREATE TABLE Pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nombre_pedido VARCHAR(100) NOT NULL,
    estado_pedido VARCHAR(50) NOT NULL,
    cliente VARCHAR(100) NOT NULL,
    fecha_pedido DATE NOT NULL,
    id_gerente INT,
    FOREIGN KEY (id_gerente) REFERENCES Gerente(id_gerente)
) ENGINE=InnoDB;


CREATE TABLE Detalle_pedido (
    id_detalle_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
) ENGINE=InnoDB;


-- Crear base de datos
CREATE DATABASE BTG;

-- Conectarse a la BD
\c BTG;

-- Crear schema
CREATE SCHEMA btg AUTHORIZATION postgres;

-- Tabla de clientes
CREATE TABLE btg.cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de sucursales
CREATE TABLE btg.sucursal (
    id_sucursal SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200)
);

-- Tabla de productos
CREATE TABLE btg.producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL
);

-- Relación: qué productos están disponibles en qué sucursales
CREATE TABLE btg.sucursal_producto (
    id_sucursal INT REFERENCES btg.sucursal(id_sucursal) ON DELETE CASCADE,
    id_producto INT REFERENCES btg.producto(id_producto) ON DELETE CASCADE,
    PRIMARY KEY (id_sucursal, id_producto)
);

-- Relación: qué sucursales visita un cliente
CREATE TABLE btg.cliente_sucursal (
    id_cliente INT REFERENCES btg.cliente(id_cliente) ON DELETE CASCADE,
    id_sucursal INT REFERENCES btg.sucursal(id_sucursal) ON DELETE CASCADE,
    PRIMARY KEY (id_cliente, id_sucursal)
);

-- Relación: qué productos tiene inscritos un cliente
CREATE TABLE btg.cliente_producto (
    id_cliente INT REFERENCES btg.cliente(id_cliente) ON DELETE CASCADE,
    id_producto INT REFERENCES btg.producto(id_producto) ON DELETE CASCADE,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_cliente, id_producto)
);

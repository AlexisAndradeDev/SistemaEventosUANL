CREATE DATABASE sistemaeventos
GO

USE sistemaeventos

CREATE TABLE Usuario (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) UNIQUE NOT NULL,
    apellido_paterno NVARCHAR(255) NOT NULL,
    apellido_materno NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL
);

CREATE TABLE Eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL,
    descripcion NVARCHAR(MAX) NOT NULL,
    lugar NVARCHAR(255) NOT NULL,
    fecha DATETIME NOT NULL
);

CREATE TABLE Asistentes (
    evento_id INT NOT NULL,
    usuario_id INT NOT NULL,
    PRIMARY KEY (evento_id, usuario_id),
    FOREIGN KEY (evento_id) REFERENCES Eventos (id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES Usuario (id) ON DELETE CASCADE
);
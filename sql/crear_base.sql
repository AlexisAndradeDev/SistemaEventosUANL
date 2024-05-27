CREATE TABLE Usuario (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) UNIQUE NOT NULL,
    nombre NVARCHAR(255) NOT NULL,
    apellido_paterno NVARCHAR(255) NOT NULL,
    apellido_materno NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL
);

CREATE TABLE Categoria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL
);

CREATE TABLE Eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL,
    descripcion NVARCHAR(MAX) NOT NULL,
    lugar NVARCHAR(255) NOT NULL,
    fecha DATETIME NOT NULL,
    creador_id INT NOT NULL,
    categoria_id INT NOT NULL,
    FOREIGN KEY (creador_id) REFERENCES Usuario (id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES Categoria (id) ON DELETE CASCADE
);

CREATE TABLE Asistentes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    evento_id INT NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (evento_id) REFERENCES Eventos (id) ON DELETE NO ACTION,
    FOREIGN KEY (usuario_id) REFERENCES Usuario (id) ON DELETE NO ACTION,
    UNIQUE (evento_id, usuario_id)
);
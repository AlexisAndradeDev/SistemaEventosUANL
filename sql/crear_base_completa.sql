CREATE TABLE MetodoPago (
    id INT IDENTITY(1,1) PRIMARY KEY,
    metodo NVARCHAR(255) NOT NULL
);

CREATE TABLE Roles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL
);

CREATE TABLE Dependencia (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL
);

CREATE TABLE Usuario (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) UNIQUE NOT NULL,
    nombre NVARCHAR(255) NOT NULL,
    apellido_paterno NVARCHAR(255) NOT NULL,
    apellido_materno NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    id_dependencia INT NOT NULL,
    FOREIGN KEY (rol_id) REFERENCES Roles (id),
    FOREIGN KEY (id_dependencia) REFERENCES Dependencia (id)
);

CREATE TABLE Categoria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL
);

CREATE TABLE Recinto (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL,
    direccion NVARCHAR(255) NOT NULL,
    capacidad INT NOT NULL
);

CREATE TABLE Butaca (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fila CHAR(1) NOT NULL,
    columna INT NOT NULL,
    recinto_id INT NOT NULL,
    FOREIGN KEY (recinto_id) REFERENCES Recinto (id)
);

CREATE TABLE Eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(255) NOT NULL,
    descripcion NVARCHAR(MAX) NOT NULL,
    fecha DATETIME NOT NULL,
    creador_id INT NOT NULL,
    categoria_id INT NOT NULL,
    recinto_id INT NOT NULL,
    FOREIGN KEY (creador_id) REFERENCES Usuario (id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES Categoria (id) ON DELETE CASCADE,
    FOREIGN KEY (recinto_id) REFERENCES Recinto (id)
);

CREATE TABLE Asistentes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    evento_id INT NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (evento_id) REFERENCES Eventos (id) ON DELETE NO ACTION,
    FOREIGN KEY (usuario_id) REFERENCES Usuario (id) ON DELETE NO ACTION,
    UNIQUE (evento_id, usuario_id)
);

CREATE TABLE Boleto (
    id INT IDENTITY(1,1) PRIMARY KEY,
    QR VARBINARY(MAX) NOT NULL,
    butaca_id INT NOT NULL,
    evento_id INT NOT NULL,
    FOREIGN KEY (butaca_id) REFERENCES Butaca (id),
    FOREIGN KEY (evento_id) REFERENCES Eventos (id)
);

CREATE TABLE Pago (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fecha DATETIME NOT NULL,
    descripcion NVARCHAR(MAX) NOT NULL,
    boleto_id INT NOT NULL,
    metodopago_id INT NOT NULL,
    FOREIGN KEY (boleto_id) REFERENCES Boleto (id),
    FOREIGN KEY (metodopago_id) REFERENCES MetodoPago (id)
);
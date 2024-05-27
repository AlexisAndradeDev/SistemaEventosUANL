USE sistemaeventos;

-- Primero, deshabilitar temporalmente las restricciones de claves for�neas

--ALTER TABLE Pago NOCHECK CONSTRAINT ALL;
--ALTER TABLE Boleto NOCHECK CONSTRAINT ALL;
--ALTER TABLE Asistentes NOCHECK CONSTRAINT ALL;
--ALTER TABLE Eventos NOCHECK CONSTRAINT ALL;
--ALTER TABLE Butaca NOCHECK CONSTRAINT ALL;
--ALTER TABLE Usuario NOCHECK CONSTRAINT ALL;

-- Luego, eliminar las tablas en el orden adecuado
DROP TABLE IF EXISTS Pago;
DROP TABLE IF EXISTS Boleto;
DROP TABLE IF EXISTS Asistentes;
DROP TABLE IF EXISTS Eventos;
DROP TABLE IF EXISTS Butaca;
DROP TABLE IF EXISTS Recinto;
DROP TABLE IF EXISTS Categoria;
DROP TABLE IF EXISTS Usuario;
DROP TABLE IF EXISTS Dependencia;
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS MetodoPago;
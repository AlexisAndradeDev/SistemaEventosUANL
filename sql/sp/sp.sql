USE sistemaeventos;

GO

ALTER PROCEDURE delete_user
    @user_id INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM Asistentes WHERE usuario_id = @user_id;
    DELETE FROM Asistentes WHERE evento_id IN (SELECT id
    FROM Eventos
    WHERE creador_id = @user_id);
    DELETE FROM Usuario WHERE id = @user_id;
END;

GO

ALTER PROCEDURE register_user
    @Email NVARCHAR(255),
    @Nombre NVARCHAR(255),
    @ApellidoPaterno NVARCHAR(255),
    @ApellidoMaterno NVARCHAR(255),
    @Password NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Usuario
        (email, nombre, apellido_paterno, apellido_materno, password)
    VALUES
        (@Email, @Nombre, @ApellidoPaterno, @ApellidoMaterno, @Password);
END

GO

ALTER PROCEDURE login_user
    @Email NVARCHAR(255),
    @Password NVARCHAR(255)
AS
BEGIN
    SELECT * FROM Usuario WHERE email = @Email AND password = @Password
END;

GO

CREATE PROCEDURE EliminarEvento
    @evento_id INT
AS
BEGIN
    DELETE FROM Asistentes
    WHERE evento_id = @evento_id;

    DELETE FROM Eventos
    WHERE id = @evento_id;
END;
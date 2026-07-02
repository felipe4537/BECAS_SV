-- ============================================
-- SCRIPT CREACION BDD BECAS_SV
-- El Salvador - 14 Departamentos
-- ============================================

-- Crear base de datos
CREATE DATABASE BECAS_SV;
GO

USE BECAS_SV;
GO

-- ============================================
-- TABLAS CATALOGO
-- ============================================

-- Departamento (14 de El Salvador)
CREATE TABLE Departamentos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL,
    codigo VARCHAR(5) NOT NULL UNIQUE
);

-- Universidad
CREATE TABLE Universidades (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(150) NOT NULL,
    departamento_id INT NOT NULL FOREIGN KEY REFERENCES Departamentos(id)
);

-- Carrera
CREATE TABLE Carreras (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(200) NOT NULL
);

-- Monitor / Gestor de becados
CREATE TABLE Monitores (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    activo BIT NOT NULL DEFAULT 1,
    fecha_registro DATETIME NOT NULL DEFAULT GETDATE()
);

-- Tipo de seguimiento
CREATE TABLE TiposSeguimiento (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL
);

-- ============================================
-- TABLAS DE NEGOCIO
-- ============================================

-- Becado
CREATE TABLE Becados (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dui CHAR(10) UNIQUE,
    direccion VARCHAR(300),
    telefono VARCHAR(20),
    email VARCHAR(150),
    departamento_id INT NOT NULL FOREIGN KEY REFERENCES Departamentos(id),
    universidad_id INT NOT NULL FOREIGN KEY REFERENCES Universidades(id),
    carrera_id INT NOT NULL FOREIGN KEY REFERENCES Carreras(id),
    anio_ingreso INT NOT NULL,
    anio_actual INT NOT NULL,
    monitor_id INT NOT NULL FOREIGN KEY REFERENCES Monitores(id),
    activo BIT NOT NULL DEFAULT 1,
    fecha_registro DATETIME NOT NULL DEFAULT GETDATE(),
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE()
);

-- Seguimiento
CREATE TABLE Seguimientos (
    id INT PRIMARY KEY IDENTITY(1,1),
    becado_id INT NOT NULL FOREIGN KEY REFERENCES Becados(id),
    monitor_id INT NOT NULL FOREIGN KEY REFERENCES Monitores(id),
    tipo_seguimiento_id INT NOT NULL FOREIGN KEY REFERENCES TiposSeguimiento(id),
    fecha DATETIME NOT NULL DEFAULT GETDATE(),
    comentario TEXT,
    nota DECIMAL(4,2),
    horas_voluntariado DECIMAL(5,2),
    presento_asistencia BIT,
    tiene_problemas BIT DEFAULT 0,
    descripcion_problema TEXT
);

-- Asistencia
CREATE TABLE Asistencia (
    id INT PRIMARY KEY IDENTITY(1,1),
    becado_id INT NOT NULL FOREIGN KEY REFERENCES Becados(id),
    fecha DATE NOT NULL,
    presente BIT NOT NULL,
    justificacion VARCHAR(300)
);

-- Voluntariado
CREATE TABLE Voluntariado (
    id INT PRIMARY KEY IDENTITY(1,1),
    becado_id INT NOT NULL FOREIGN KEY REFERENCES Becados(id),
    fecha DATE NOT NULL,
    actividad VARCHAR(300) NOT NULL,
    horas DECIMAL(5,2) NOT NULL,
    observaciones TEXT
);

-- Notas academicas
CREATE TABLE Notas (
    id INT PRIMARY KEY IDENTITY(1,1),
    becado_id INT NOT NULL FOREIGN KEY REFERENCES Becados(id),
    periodo VARCHAR(20) NOT NULL,
    materia VARCHAR(200) NOT NULL,
    nota DECIMAL(4,2) NOT NULL,
    aprobado BIT NOT NULL DEFAULT 1
);

-- Reportes generados
CREATE TABLE ReportesGenerados (
    id INT PRIMARY KEY IDENTITY(1,1),
    monitor_id INT FOREIGN KEY REFERENCES Monitores(id),
    tipo_reporte VARCHAR(50) NOT NULL,
    fecha_generacion DATETIME NOT NULL DEFAULT GETDATE(),
    parametros TEXT,
    archivo_nombre VARCHAR(200)
);

-- ============================================
-- INDICES
-- ============================================
CREATE INDEX IX_Becados_Departamento ON Becados(departamento_id);
CREATE INDEX IX_Becados_Monitor ON Becados(monitor_id);
CREATE INDEX IX_Becados_Activo ON Becados(activo);
CREATE INDEX IX_Seguimientos_Becado ON Seguimientos(becado_id);
CREATE INDEX IX_Seguimientos_Fecha ON Seguimientos(fecha);
CREATE INDEX IX_Asistencia_Becado ON Asistencia(becado_id, fecha);
CREATE INDEX IX_Notas_Becado ON Notas(becado_id, periodo);

-- ============================================
-- DATA: 14 DEPARTAMENTOS
-- ============================================
INSERT INTO Departamentos (nombre, codigo) VALUES
('San Salvador',     'SV-01'),
('Santa Ana',        'SV-02'),
('San Miguel',       'SV-03'),
('La Libertad',      'SV-04'),
('Usulutan',         'SV-05'),
('Sonsonate',        'SV-06'),
('La Union',         'SV-07'),
('Cuscatlan',        'SV-08'),
('Chalatenango',     'SV-09'),
('La Paz',           'SV-10'),
('Cabanas',          'SV-11'),
('San Vicente',      'SV-12'),
('Morazan',          'SV-13'),
('Ahuachapan',       'SV-14');

-- Tipos de seguimiento
INSERT INTO TiposSeguimiento (nombre) VALUES
('Llamada telefonica'),
('Visita presencial'),
('Videollamada'),
('Mensaje de texto'),
('Correo electronico'),
('Visita domiciliaria');

PRINT 'Base de datos BECAS_SV creada exitosamente.';
GO

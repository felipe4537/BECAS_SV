-- ============================================
-- TABLA: CARRERAS POR UNIVERSIDAD
-- ============================================
USE BECAS_SV;
GO

CREATE TABLE UniversidadCarreras (
    universidad_id INT NOT NULL FOREIGN KEY REFERENCES Universidades(id),
    carrera_id INT NOT NULL FOREIGN KEY REFERENCES Carreras(id),
    PRIMARY KEY (universidad_id, carrera_id)
);
GO

-- ============================================
-- MAPEO: Carreras por Universidad
-- Leyenda: uid = universidad_id, cid = carrera_id
-- ============================================

-- UES (uid=1) ofrece TODAS las carreras (prácticamente)
INSERT INTO UniversidadCarreras (universidad_id, carrera_id)
SELECT 1, id FROM Carreras;

-- ============================================
-- UJMD - Jose Matias Delgado (uid=2)
-- Derecho, Admin, Psicologia, Mercadeo, Comunicaciones, Diseño, Economia,
-- Finanzas, Relaciones Internacionales, Arquitectura, Letras
-- ============================================
INSERT INTO UniversidadCarreras VALUES
(2,2),(2,3),(2,4),(2,10),(2,16),(2,17),(2,23),(2,24),(2,26),
(2,11),(2,33),(2,37);

-- ============================================
-- UFG - Francisco Gavidia (uid=3)
-- Admin, Psicologia, Sistemas, Mercadeo, Comunicaciones, Diseño,
-- Economia, Finanzas, Hotelería, Ingenierias, Computacion
-- ============================================
INSERT INTO UniversidadCarreras VALUES
(3,3),(3,4),(3,5),(3,10),(3,16),(3,17),(3,23),(3,24),(3,25),
(3,12),(3,36),(3,37),(3,53);

-- ============================================
-- UCA - Centroamericana (uid=4)
-- Derecho, Admin, Psicologia, Sistemas, Contaduria, Ingles, Mercadeo,
-- Comunicaciones, Economia, Sociologia, Filosofia, Letras, Ing. Civil,
-- Ing. Industrial, Ing. Electrica, Ing. Mecanica, Computacion
-- ============================================
INSERT INTO UniversidadCarreras VALUES
(4,2),(4,3),(4,4),(4,5),(4,8),(4,9),(4,10),(4,16),(4,23),
(4,27),(4,31),(4,33),(4,12),(4,7),(4,13),(4,14),(4,37);

-- ============================================
-- UDB - Don Bosco (uid=12)
-- Sistemas, Ingles, Mercadeo, Ing. Industrial, Ing. Electrica,
-- Ing. Mecanica, Computacion, Telecomunicaciones, Biomedica,
-- Tec. Electronica, Tec. Mecanica Automotriz, Tec. Desarrollo Software
-- ============================================
INSERT INTO UniversidadCarreras VALUES
(12,5),(12,9),(12,10),(12,7),(12,13),(12,14),(12,36),(12,37),
(12,43),(12,44),(12,45),(12,54);

-- ============================================
-- UTEC - Tecnologica (uid=24)
-- Admin, Sistemas, Contaduria, Ingles, Mercadeo, Diseno, Economia,
-- Finanzas, Hotelería, Computacion, Tec. Marketing Digital, Gastronomia
-- ============================================
INSERT INTO UniversidadCarreras VALUES
(24,3),(24,5),(24,8),(24,9),(24,10),(24,17),(24,23),(24,24),(24,25),
(24,37),(24,57),(24,56);

-- ============================================
-- UES extension: solo carreras generales para regionales
-- ============================================

-- UNASA - Autonoma de Santa Ana (uid=6)
INSERT INTO UniversidadCarreras VALUES
(6,3),(6,4),(6,5),(6,8),(6,9),(6,10);

-- UNICAES - Catolica (uid=7)
INSERT INTO UniversidadCarreras VALUES
(7,3),(7,4),(7,8),(7,9),(7,10);

-- UNIVO - de Oriente (uid=10)
INSERT INTO UniversidadCarreras VALUES
(10,3),(10,5),(10,8),(10,9),(10,10),(10,7);

-- USO - de Sonsonate (uid=11)
INSERT INTO UniversidadCarreras VALUES
(11,3),(11,5),(11,8),(11,9),(11,10);

-- UGB - Gerardo Barrios (uid=15)
INSERT INTO UniversidadCarreras VALUES
(15,3),(15,4),(15,5),(15,8),(15,9),(15,10),(15,7);

-- UAB - Andres Bello (uid=13) - salud
INSERT INTO UniversidadCarreras VALUES
(13,3),(13,4),(13,6),(13,8),(13,9),(13,10),(13,34),(13,35);

-- UEES - Evangelica (uid=14) - salud
INSERT INTO UniversidadCarreras VALUES
(14,2),(14,3),(14,4),(14,6),(14,8),(14,9),(14,20);

-- UMOAR - Monseñor Romero (uid=18) - salud
INSERT INTO UniversidadCarreras VALUES
(18,3),(18,4),(18,6),(18,8),(18,9),(18,10);

-- ULS - Luterana (uid=16)
INSERT INTO UniversidadCarreras VALUES
(16,3),(16,5),(16,8),(16,9),(16,10);

-- UMA - Modular Abierta (uid=17)
INSERT INTO UniversidadCarreras VALUES
(17,3),(17,5),(17,8),(17,9),(17,10);

-- USAM - Alberto Masferrer (uid=22)
INSERT INTO UniversidadCarreras VALUES
(22,2),(22,3),(22,4),(22,8),(22,9),(22,10),(22,16);

-- UTLA - Tecnica Latinoamericana (uid=23)
INSERT INTO UniversidadCarreras VALUES
(23,3),(23,5),(23,8),(23,9),(23,10),(23,37);

-- UPAN - Panamericana (uid=19)
INSERT INTO UniversidadCarreras VALUES
(19,3),(19,4),(19,5),(19,8),(19,9),(19,10),(19,16);

-- Universidad Albert Einstein (uid=5)
INSERT INTO UniversidadCarreras VALUES
(5,5),(5,9),(5,10),(5,37);

-- Universidad Cristiana UCAD (uid=8)
INSERT INTO UniversidadCarreras VALUES
(8,3),(8,4),(8,8),(8,9),(8,10);

-- Universidad Nueva San Salvador UNSSA (uid=9)
INSERT INTO UniversidadCarreras VALUES
(9,3),(9,5),(9,8),(9,9),(9,10);

-- Universidad Pedagogica (uid=20)
INSERT INTO UniversidadCarreras VALUES
(20,9),(20,18),(20,19),(20,30),(20,51);

-- Universidad Politecnica (uid=21)
INSERT INTO UniversidadCarreras VALUES
(21,5),(21,7),(21,12),(21,13),(21,14),(21,36),(21,37),(21,43),(21,53);

-- ITCA-FEPADE (uid=25) - tecnica
INSERT INTO UniversidadCarreras VALUES
(25,5),(25,37),(25,39),(25,40),(25,43),(25,44),(25,45),(25,57);

-- ESEN (uid=26)
INSERT INTO UniversidadCarreras VALUES
(26,3),(26,23),(26,24),(26,26),(26,38);

-- ENA - Escuela Nacional de Agricultura (uid=27)
INSERT INTO UniversidadCarreras VALUES
(27,15),(27,28),(27,53);

-- Universidad Internacional Nehemias NIU (uid=28)
INSERT INTO UniversidadCarreras VALUES
(28,3),(28,5),(28,8),(28,9),(28,10);

PRINT 'Asignacion de carreras por universidad completada.';
GO

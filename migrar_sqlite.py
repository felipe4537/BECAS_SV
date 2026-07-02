"""
Migracion: SQL Server (pyodbc) -> SQLite
Ejecutar desde Windows: python migrar_sqlite.py
Requiere: pip install pyodbc
"""
import sqlite3, pyodbc

SRC = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,49742;"
    "DATABASE=BECAS_SV;"
    "UID=sa;PWD=Dust534lol+;"
)
DST = "BECAS_SV.db"

# ── Schema SQLite ──────────────────────────────────────────────
SCHEMA = """
PRAGMA foreign_keys = OFF;

CREATE TABLE Departamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    codigo TEXT NOT NULL UNIQUE
);

CREATE TABLE Universidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    departamento_id INTEGER NOT NULL REFERENCES Departamentos(id)
);

CREATE TABLE Carreras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE Monitores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT UNIQUE,
    telefono TEXT,
    activo INTEGER NOT NULL DEFAULT 1,
    fecha_registro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TiposSeguimiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE Becados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    dui TEXT UNIQUE,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    departamento_id INTEGER NOT NULL REFERENCES Departamentos(id),
    universidad_id INTEGER NOT NULL REFERENCES Universidades(id),
    carrera_id INTEGER NOT NULL REFERENCES Carreras(id),
    anio_ingreso INTEGER NOT NULL,
    anio_actual INTEGER NOT NULL,
    monitor_id INTEGER NOT NULL REFERENCES Monitores(id),
    activo INTEGER NOT NULL DEFAULT 1,
    fecha_registro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Seguimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    becado_id INTEGER NOT NULL REFERENCES Becados(id),
    monitor_id INTEGER NOT NULL REFERENCES Monitores(id),
    tipo_seguimiento_id INTEGER NOT NULL REFERENCES TiposSeguimiento(id),
    fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    nota REAL,
    horas_voluntariado REAL,
    presento_asistencia INTEGER,
    tiene_problemas INTEGER DEFAULT 0,
    descripcion_problema TEXT
);

CREATE TABLE Asistencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    becado_id INTEGER NOT NULL REFERENCES Becados(id),
    fecha TEXT NOT NULL,
    presente INTEGER NOT NULL,
    justificacion TEXT
);

CREATE TABLE Voluntariado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    becado_id INTEGER NOT NULL REFERENCES Becados(id),
    fecha TEXT NOT NULL,
    actividad TEXT NOT NULL,
    horas REAL NOT NULL,
    observaciones TEXT
);

CREATE TABLE Notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    becado_id INTEGER NOT NULL REFERENCES Becados(id),
    periodo TEXT NOT NULL,
    materia TEXT NOT NULL,
    nota REAL NOT NULL,
    aprobado INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE ReportesGenerados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monitor_id INTEGER REFERENCES Monitores(id),
    tipo_reporte TEXT NOT NULL,
    fecha_generacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    parametros TEXT,
    archivo_nombre TEXT
);

CREATE TABLE UniversidadCarreras (
    universidad_id INTEGER NOT NULL REFERENCES Universidades(id),
    carrera_id INTEGER NOT NULL REFERENCES Carreras(id),
    PRIMARY KEY (universidad_id, carrera_id)
);

CREATE INDEX IF NOT EXISTS IX_Becados_Departamento ON Becados(departamento_id);
CREATE INDEX IF NOT EXISTS IX_Becados_Monitor ON Becados(monitor_id);
CREATE INDEX IF NOT EXISTS IX_Becados_Activo ON Becados(activo);
CREATE INDEX IF NOT EXISTS IX_Seguimientos_Becado ON Seguimientos(becado_id);
CREATE INDEX IF NOT EXISTS IX_Seguimientos_Fecha ON Seguimientos(fecha);
CREATE INDEX IF NOT EXISTS IX_Asistencia_Becado ON Asistencia(becado_id, fecha);
CREATE INDEX IF NOT EXISTS IX_Notas_Becado ON Notas(becado_id, periodo);
"""

# ── Migracion ─────────────────────────────────────────────────
def migrate():
    print("Conectando a SQL Server...")
    src = pyodbc.connect(SRC)
    src_cur = src.cursor()

    print("Creando SQLite...")
    dst = sqlite3.connect(DST)
    dst_cur = dst.cursor()
    dst_cur.executescript(SCHEMA)

    TABLAS = [
        "Departamentos",
        "Universidades",
        "Carreras",
        "Monitores",
        "TiposSeguimiento",
        "Becados",
        "Seguimientos",
        "Asistencia",
        "Voluntariado",
        "Notas",
        "ReportesGenerados",
        "UniversidadCarreras",
    ]

    for t in TABLAS:
        src_cur.execute(f"SELECT * FROM {t}")
        rows = src_cur.fetchall()
        if not rows:
            print(f"  {t}: 0 filas (sin datos)")
            continue
        cols = [c[0] for c in src_cur.description]
        placeholders = ",".join("?" for _ in cols)
        colnames = ",".join(cols)
        for row in rows:
            vals = list(row)
            # convertir datetime objects a string ISO
            for i, v in enumerate(vals):
                if hasattr(v, "isoformat"):
                    vals[i] = v.isoformat(sep=" ", timespec="seconds")
                elif isinstance(v, bytes):
                    vals[i] = v.decode()
            dst_cur.execute(f"INSERT INTO {t} ({colnames}) VALUES ({placeholders})", vals)
        dst.commit()
        print(f"  {t}: {len(rows)} filas migradas")

    src.close()
    dst.close()
    print("\nMigracion completada. Archivo: " + DST)

if __name__ == "__main__":
    migrate()

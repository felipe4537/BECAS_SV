import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BECAS_SV.db")
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Obtener columnas actuales
cur.execute("PRAGMA table_info(Becados)")
cols = {r[1] for r in cur.fetchall()}

nuevas = {
    "fecha_nacimiento": "ALTER TABLE Becados ADD COLUMN fecha_nacimiento TEXT",
    "genero": "ALTER TABLE Becados ADD COLUMN genero TEXT",
    "municipio": "ALTER TABLE Becados ADD COLUMN municipio TEXT",
    "contacto_emergencia": "ALTER TABLE Becados ADD COLUMN contacto_emergencia TEXT",
    "telefono_emergencia": "ALTER TABLE Becados ADD COLUMN telefono_emergencia TEXT",
    "carnet": "ALTER TABLE Becados ADD COLUMN carnet TEXT",
    "anno_graduacion": "ALTER TABLE Becados ADD COLUMN anno_graduacion INTEGER",
    "promedio": "ALTER TABLE Becados ADD COLUMN promedio REAL",
    "ultimo_anio_cursado": "ALTER TABLE Becados ADD COLUMN ultimo_anio_cursado INTEGER",
}

for nombre, sql in nuevas.items():
    if nombre not in cols:
        cur.execute(sql)
        print(f"  + {nombre}")

# Crear tabla NotasBecados si no existe
cur.execute("""CREATE TABLE IF NOT EXISTS NotasBecados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    becado_id INTEGER NOT NULL,
    monitor_id INTEGER NOT NULL,
    nota TEXT NOT NULL,
    tipo TEXT DEFAULT 'general',
    fecha TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (becado_id) REFERENCES Becados(id),
    FOREIGN KEY (monitor_id) REFERENCES Monitores(id)
)""")
cur.execute("CREATE INDEX IF NOT EXISTS idx_notas_becado ON NotasBecados(becado_id)")

conn.commit()
conn.close()
print("\nMigracion completada.")

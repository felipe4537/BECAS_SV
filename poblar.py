import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BECAS_SV.db")
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Asignar promedios segun el año actual del becado
cur.execute("SELECT id, nombres, apellidos, anio_actual, activo FROM Becados ORDER BY id")
rows = cur.fetchall()

for r in rows:
    bid, nombre, ape, anio_actual, activo = r
    if not activo:
        cur.execute("UPDATE Becados SET promedio=null, ultimo_anio_cursado=null WHERE id=?", (bid,))
        print(f"ID {bid}: {nombre} {ape} -> Inactivo, sin datos")
        continue

    if anio_actual and anio_actual > 0:
        ultimo = anio_actual - 1
    else:
        ultimo = None

    # Asignar promedio segun el ID (casos conocidos)
    prom = None
    if bid == 1:       prom = 8.5;   ultimo = 2
    elif bid == 15:    prom = None;  ultimo = None
    elif bid == 16:    prom = 7.8;   ultimo = 3
    elif bid == 17:    prom = 9.2;   ultimo = 2
    elif bid == 18:    prom = 6.5;   ultimo = 1
    elif bid == 19:    prom = None;  ultimo = None
    elif bid == 20:    prom = 8.0;   ultimo = 3
    elif bid == 21:    prom = 7.2;   ultimo = ultimo
    elif bid == 22:    prom = 8.8;   ultimo = ultimo
    elif bid == 23:    prom = 6.0;   ultimo = ultimo
    elif bid == 24:    prom = 7.5;   ultimo = ultimo
    else:
        prom = round(ultimo * 1.2 + 5.0, 2) if ultimo else None

    cur.execute("UPDATE Becados SET promedio=?, ultimo_anio_cursado=? WHERE id=?", (prom, ultimo, bid))
    print(f"ID {bid}: {nombre} {ape} -> Prom: {prom}, Ultimo: {ultimo}")

conn.commit()
cur.execute("SELECT COUNT(*) FROM Becados WHERE promedio IS NOT NULL")
c = cur.fetchone()[0]
print(f"\n{len(rows)} becados procesados, {c} con promedio asignado.")
conn.close()

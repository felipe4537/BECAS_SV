import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BECAS_SV.db")
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""SELECT b.id, b.nombres, b.apellidos, d.nombre as depto
    FROM Becados b JOIN Departamentos d ON b.departamento_id=d.id ORDER BY b.id""")

data = []
for r in cur.fetchall():
    bid, nom, ape, depto = r

    if bid == 1:
        fn, gen, mun, ce, te, car, ag = "2002-05-12","Masculino","San Salvador","Ana Ortiz","78901234","AE2025001",2029
    elif bid == 15:
        fn, gen, mun, ce, te, car, ag = "2005-08-20","Femenino","San Salvador","Carlos Lopez","71234567","ML2025001",2029
    elif bid == 16:
        fn, gen, mun, ce, te, car, ag = "2001-03-15","Masculino","Santa Ana","Rosa Martinez","79876543","CM2022001",2027
    elif bid == 17:
        fn, gen, mun, ce, te, car, ag = "2003-11-02","Femenino","San Miguel","Jose Hernandez","73456789","AH2023001",2028
    elif bid == 18:
        fn, gen, mun, ce, te, car, ag = "2004-07-18","Masculino","Santa Tecla","Maria Rodriguez","75678901","JR2024001",2028
    elif bid == 19:
        fn, gen, mun, ce, te, car, ag = "2006-01-25","Femenino","Sonsonate","Pedro Ramirez","72134567","SR2025001",2029
    elif bid == 20:
        fn, gen, mun, ce, te, car, ag = "2001-01-11","Femenino","Santa Tecla","Julia Lopez","72223333","ML2023001",2028
    elif bid == 21:
        fn, gen, mun, ce, te, car, ag = "2000-09-10","Masculino","Santa Ana","Luisa Martinez","77889900","JM2022001",2027
    elif bid == 22:
        fn, gen, mun, ce, te, car, ag = "2003-04-05","Femenino","Santa Tecla","Ramon Ramirez","76543210","AR2024001",2028
    elif bid == 23:
        fn, gen, mun, ce, te, car, ag = "2000-12-22","Masculino","Sonsonate","Elena Hernandez","70123456","CH2021001",2027
    elif bid == 24:
        fn, gen, mun, ce, te, car, ag = "2001-06-30","Femenino","San Miguel","Diego Rivera","74567890","SR2022001",2027
    else:
        # Para registros nuevos, inferir municipio del departamento
        munis = {"San Salvador":"San Salvador","Santa Ana":"Santa Ana","San Miguel":"San Miguel",
                 "La Libertad":"Santa Tecla","Sonsonate":"Sonsonate","La Union":"La Union",
                 "Usulutan":"Usulutan","Chalatenango":"Chalatenango","Cuscatlan":"Cojutepeque",
                 "San Vicente":"San Vicente","Morazan":"San Francisco Gotera","Ahuachapan":"Ahuachapan",
                 "Cabanas":"Sensuntepeque","La Paz":"Zacatecoluca"}
        mun = munis.get(depto, depto)
        fn = f"{2000+(bid%15):04d}-{(bid%12+1):02d}-{(bid%28+1):02d}"
        gen = "Masculino" if bid % 2 == 0 else "Femenino"
        ce = f"Contacto de {nom}"
        te = f"7{(bid*1111)%10000000:07d}"
        car = f"SV{bid:04d}"
        ag = None

    data.append((fn, gen, mun, ce, te, car, ag, bid))

cur.executemany("""UPDATE Becados SET
    fecha_nacimiento=?, genero=?, municipio=?, contacto_emergencia=?,
    telefono_emergencia=?, carnet=?, anno_graduacion=? WHERE id=?""", data)
conn.commit()

cur.execute("SELECT id, nombres, apellidos, fecha_nacimiento, genero, municipio, contacto_emergencia, telefono_emergencia, carnet, anno_graduacion FROM Becados ORDER BY id")
for r in cur.fetchall():
    print(f"ID {r[0]}: {r[1]} {r[2]} | {r[3]} | {r[4]} | {r[5]} | CE:{r[6]} | TelE:{r[7]} | {r[8]} | AG:{r[9]}")

conn.close()
print("\nDatos personales poblados correctamente.")

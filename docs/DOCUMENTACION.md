# BECAS_SV — Sistema de Monitoreo de Becados

## Descripcion
Aplicacion web Flask para gestion de becados en El Salvador. Permite registrar, editar, buscar y filtrar becados por departamento, universidad, carrera y monitor. Incluye carga masiva via Excel, dashboard con graficos interactivos, reportes en Excel, notas/observaciones por becado y rendimiento academico con estadisticas numpy.

## Stack
- **Backend**: Python 3 + Flask + SQLite
- **Frontend**: HTML/CSS vanilla, Jinja2 templates
- **Graficos**: Chart.js 4 + chartjs-plugin-datalabels 2
- **Iconos**: SVG inline (lucide-style)
- **Analisis**: pandas + numpy (opcional, dashboard academico)
- **Base de datos**: SQLite (`BECAS_SV.db`)
- **Despliegue**: PythonAnywhere (free tier)

## Estructura de Archivos

```
BECAS_SV/
├── app.py                       # Aplicacion Flask principal (~1690+ lineas, single-file)
├── BECAS_SV.db                  # Base de datos SQLite
├── ejemplo_becados.xlsx         # Ejemplo para carga masiva
├── run.bat                      # Launcher Windows (pip install + flask run)
├── requirements.txt             # Dependencias: flask, openpyxl, pandas, numpy
├── migrar.py                    # Crea columnas nuevas + tabla NotasBecados
├── poblar.py                    # Asigna promedios/ultimo_anio_cursado a registros existentes
├── poblar_personal.py           # Poblapersonal info + contacto emergencia a registros existentes
├── static/
│   └── BECAS_SV.jpeg            # Logo de la aplicacion
└── docs/
    ├── DOCUMENTACION.md         # Este documento
    ├── TECNOLOGIAS.md           # Tecnologias usadas
    ├── TECNOLOGIAS.txt          # Tecnologias usadas (txt plano)
    └── GUIA_USUARIO.txt         # Guia de usuario para el equipo
```

## Base de Datos

### Tablas

| Tabla | Descripcion |
|-------|-------------|
| `Monitores` | Usuarios del sistema (login con email + telefono) |
| `Departamentos` | 14 departamentos de El Salvador |
| `Universidades` | 28 universidades, cada una vinculada a un departamento (`departamento_id`) |
| `Carreras` | 60 carreras |
| `UniversidadCarreras` | Junction: que carreras ofrece cada universidad |
| `Becados` | Registro central de estudiantes becados |
| `NotasBecados` | Notas/observaciones por becado (general, llamada, visita, academico) |

### Esquema Becados

```sql
CREATE TABLE Becados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    dui TEXT UNIQUE NOT NULL,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    departamento_id INTEGER NOT NULL REFERENCES Departamentos(id),
    universidad_id INTEGER NOT NULL REFERENCES Universidades(id),
    carrera_id INTEGER NOT NULL REFERENCES Carreras(id),
    monitor_id INTEGER NOT NULL REFERENCES Monitores(id),
    anio_ingreso INTEGER,
    anio_actual INTEGER,
    activo INTEGER DEFAULT 1,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_nacimiento TEXT,
    genero TEXT,
    municipio TEXT,
    contacto_emergencia TEXT,
    telefono_emergencia TEXT,
    carnet TEXT,
    anno_graduacion INTEGER,
    promedio REAL,
    ultimo_anio_cursado INTEGER
);
```

### Esquema NotasBecados

```sql
CREATE TABLE NotasBecados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    becado_id INTEGER NOT NULL REFERENCES Becados(id),
    tipo TEXT NOT NULL CHECK(tipo IN ('general','llamada','visita','academico')),
    nota TEXT NOT NULL,
    creada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Funcionalidades Implementadas

### Autenticacion
- Login con email + telefono (contrasena)
- Registro de nuevos monitores
- Recuperacion de contrasena (muestra telefono enmascarado)
- Proteccion de rutas via decorador `@login_required`

### CRUD de Becados
- **Lista** (`/ingreso`): tabla con scroll, columnas: Nombre, DUI, Telefono, Departamento, Universidad, Carrera, Monitor, Periodo, Promedio, Estado, Acciones
- **Registrar** (`/ingreso/registrar`): formulario responsive horizontal (4 columnas, 3 secciones: Informacion Personal, Contacto de Emergencia, Rendimiento Academico), cascading dropdowns con datos embebidos via JSON
- **Editar** (`/ingreso/editar/<id>`): mismo formulario precargado
- **Eliminar** (`/ingreso/eliminar/<id>`): confirmacion JS + redirect

### Campos adicionales por becado
- fecha_nacimiento, genero, municipio
- contacto_emergencia, telefono_emergencia
- carnet, anno_graduacion
- promedio (nota de 0.0 a 10.0), ultimo_anio_cursado

### Busqueda y Filtros
- Busqueda por nombre, apellido o DUI (lado cliente, JS, sin recargar pagina)
- Filtros por dropdowns: Departamento, Universidad, Monitor, Periodo, Estado (lado cliente, combinables)
- Boton de actualizar (recarga pagina, ignorando cache)

### Carga Masiva
- Upload de archivo .xlsx (22 columnas)
- Validacion por fila: campos obligatorios, formato, existencia de catalogo
- Deteccion de DUPs (DUI duplicado)
- Descarga de plantilla Excel
- Resumen de insertados/errores
- Columnas incluidas: desde A (Nombres) hasta V (UltimoAnioCursado)

### Notas y Observaciones (`/notas/<id>`)
- Tarjeta informativa del becado con datos principales
- Formulario para agregar nota (4 tipos: general, llamada, visita, academico)
- Historial cronologico de notas
- Edicion de nota existente

### Validaciones
- **Departamento-Universidad**: verifica que la universidad pertenezca al departamento seleccionado (servidor, registrar y editar)
- **DUI**: 9 digitos, sin guion, unico
- **Telefono**: 8 digitos
- **Email**: formato valido
- **Nombres/Apellidos**: solo letras
- **Anio ingreso**: 2000-2030
- **Anio actual**: 1-10

### Dashboard (`/dashboard`)
- 5 secciones de KPIs: Total Becados, Activos, Inactivos, Monitores, Rendimiento Academico
- Deltas vs año anterior (▲/▼ badges de porcentaje)
- Filtros acumulativos: Año Ingreso, Departamento, Universidad, Carrera (cascading)
- 5 graficos Chart.js: Barras por Departamento, Dona por Estado, Barras Top 10 Universidades, Linea por Año Ingreso, Barras Top 10 Monitores
- **Rendimiento Academico**: 5 KPIs con numpy (media, mediana, minimo, maximo, Q con promedio)
- Todos los graficos con data labels y colores personalizados

### Reportes (`/reportes`)
- 5 tipos de reporte Excel: Listado General, Por Departamento, Por Universidad, Por Año Ingreso, Por Monitor
- Filtros opcionales: Departamento, Universidad, Año Ingreso, Estado
- Columnas incluidas: Promedio, UltimoAnioCursado
- Renderizado con pandas (`pd.read_sql_query` + `pd.ExcelWriter`) con fallback a openpyxl
- Formato profesional: headers morados (#302b63), auto-ancho de columnas
- Descarga directa via `send_file()`

### Interfaz de Usuario
- Header fijo con efecto blur al hacer scroll (`.scrolled`)
- Menu de navegacion con iconos SVG: Inicio, Dashboard, Ingreso (submenu: Lista, Registrar, Carga Masiva), Reportes
- Menu hamburguesa en dispositivos moviles (≤768px) con toggle via JS
- Formularios responsive horizontales (max-width 1300px, 4 columnas → 3 → 2 → 1)
- Cursor animado personalizado: punto (6px) + anillo (28-36px) con efecto lerp
- Totalmente responsive (breakpoints 1000px, 768px, 480px)

### Carga Masiva (`/ingreso/carga-masiva`)
- Pagina de una sola columna (tabla formato + upload apilados)
- Upload de archivo .xlsx con validacion por fila
- Descarga de plantilla ejemplo (22 columnas)
- Resumen de insertados vs errores con mensajes detallados

## Estilos y UX

### Paleta de Colores
| Elemento | Color |
|----------|-------|
| Primario (morado) | `#302b63` |
| Acento (naranja) | `#e67e22` |
| Exito (verde) | `#1e7e34` |
| Peligro (rojo) | `#d93025` / `#e74c3c` |
| Fondo pagina | Degradado `#f5f3ff` → `#fff` → `#fefcf8` |
| Fondo headers tabla | `#e67e22` |
| Header formularios | Degradado `#302b63` → `#5e4fa2` |
| Cards formulario | Borde `#dadce0`, fondo `#fff` |

### Responsive
- Breakpoints: 1000px, 768px, 480px
- Formularios: 4 columnas → 3 (≤1000px) → 2 (≤768px) → 1 (≤480px)
- Header con menu hamburguesa en ≤768px (toggle via JS)
- Tablas con `overflow-x: auto` en mobile
- Grid de cards se apila en 1 columna

### Componentes UI
- Header fijo con `backdrop-filter: blur(10px)` al scroll
- Menu hamburguesa con despliegue de dropdowns por clic (Ingreso)
- Boton "Volver" con `history.back()` (oculto en login/registro/recuperar)
- Flash messages con color segun tipo (ok/error)
- Tabla con sticky header, scroll
- Cards con header degradado morado para formularios
- Cursor animado: dot + ring con transicion suave, pointer en botones/links

## Decisiones Tecnicas

| Decision | Razón |
|----------|-------|
| SQLite en vez de SQL Server | Despliegue gratis en PythonAnywhere (sin SQL Server) |
| Single-file `app.py` | Simplicidad de despliegue en PythonAnywhere |
| Datos embebidos (JSON) para cascading dropdowns | Evita llamadas fetch/API, funciona sin conexion |
| Busqueda cliente-side | No agrega entradas al historial del navegador |
| `minlength`/`maxlength` en vez de `pattern` para DUI/telefono | Evita mensaje "formato solicitado" del navegador |
| Validacion servidor + HTML5 | Doble capa de seguridad |
| `app.run(host="0.0.0.0", port=8080)` | Compatible con PythonAnywhere |
| pandas/numpy opcional (`HAS_PD` flag) | Evita error si no estan instalados en PythonAnywhere |
| Reportes con pandas + fallback openpyxl | Mejor rendimiento y menos codigo si pandas disponible |
| Cursor animado con CSS + JS vanilla | Sin dependencias externas, efecto ligero |

## Uso

### Local (Windows)
```batch
run.bat
```
O manual:
```bash
pip install flask openpyxl pandas numpy
python app.py
```
Abrir `http://localhost:8080`

### PythonAnywhere
1. Subir `app.py` via Files tab
2. Correr migraciones: `python3 migrar.py && python3 poblar.py && python3 poblar_personal.py`
3. Instalar dependencias: `pip3 install pandas numpy --user`
4. Crear Web App con manual config (Python 3.x)
5. Source: path al directorio
6. WSGI: apuntar a `app.app`
7. Reload

## Migraciones

| Script | Que hace |
|--------|----------|
| `migrar.py` | Crea columnas faltantes (fecha_nacimiento, genero, municipio, contacto_emergencia, telefono_emergencia, carnet, anno_graduacion, promedio, ultimo_anio_cursado) + tabla NotasBecados |
| `poblar.py` | Asigna promedios (5.0-10.0) y ultimo_anio_cursado a registros con valores NULL |
| `poblar_personal.py` | Genera fecha_nacimiento, genero, municipio, contacto_emergencia y telefono_emergencia para registros NULL |

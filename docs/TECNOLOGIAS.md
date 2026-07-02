# Tecnologias Utilizadas — BECAS_SV

## Backend

| Tecnologia | Version | Uso |
|------------|---------|-----|
| Python | 3.12+ | Lenguaje principal del servidor |
| Flask | 3.x | Framework web (rutas, sesiones, templates) |
| SQLite 3 | — | Base de datos embebida |
| openpyxl | 3.x | Lectura/escritura de Excel (carga masiva + reportes) |
| pandas | 2.x | Consultas a BD y generacion de Excel en reportes (pd.read_sql_query + pd.ExcelWriter) |
| numpy | 1.x | Estadisticas de rendimiento academico en dashboard (mean, median, std, percentile) |
| Werkzeug | — | Hashing de contrasenas, utilidades HTTP |

## Frontend

| Tecnologia | Version | Uso |
|------------|---------|-----|
| HTML5 | — | Estructura de paginas |
| CSS3 | — | Estilos, flex/grid, responsive design, animacion cursor |
| JavaScript (vanilla) | ES6 | Busqueda cliente-side, menu hamburguesa, cascading dropdowns, scroll header, cursor follower |
| Jinja2 | — | Templates HTML con variables desde Flask |
| Chart.js | 4.x | Graficos del dashboard (barras, dona, linea) |
| chartjs-plugin-datalabels | 2.x | Etiquetas de datos en graficos |

## Base de Datos

| Objeto | Descripcion |
|--------|-------------|
| BECAS_SV.db | Archivo SQLite unico |
| 7 tablas | Monitores, Departamentos, Universidades, Carreras, UniversidadCarreras, Becados, NotasBecados |
| 25 columnas en Becados | Incluye fecha_nacimiento, genero, municipio, contacto_emergencia, telefono_emergencia, carnet, anno_graduacion, promedio, ultimo_anio_cursado |
| SQL embebido | Consultas directas en app.py (sin ORM) |

## Infraestructura

| Componente | Detalle |
|------------|---------|
| Servidor | Flask development server (local), mod_wsgi (PythonAnywhere) |
| Despliegue | PythonAnywhere free tier |
| Puerto local | 8080 |
| SO objetivo | Windows (desarrollo), Linux (produccion) |

## Iconos

| Tipo | Origen |
|------|--------|
| SVG inline | Creados manualmente estilo lucide (stroke-width 2.5, 16x16) |
| Iconos | Inicio, Dashboard, Ingreso, Lista, Registrar, Upload, Reportes, Usuario, Logout |

## Dependencias Python

```
flask
openpyxl
pandas
numpy
```

## CDN

```
https://cdn.jsdelivr.net/npm/chart.js@4
https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2
```

## Scripts de Migracion

| Script | Proposito |
|--------|-----------|
| migrar.py | Crea columnas nuevas y tabla NotasBecados (idempotente) |
| poblar.py | Asigna promedios y ultimo_anio_cursado a registros existentes |
| poblar_personal.py | Genera datos personales y contacto de emergencia |

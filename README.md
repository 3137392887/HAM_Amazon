# HAM Amazon - Web Scraper y API REST

Sistema completo de web scraping de productos Amazon con almacenamiento en base de datos SQLite y API REST para consultas.

##  Estructura del Proyecto

```
HAM_Amazon/
├── Script/
│   ├── main.py                 # Oequestado
│   ├── scraper.py              # Web scraper con Selenium
│   ├── web_app.py              # Aplicación Flask para consultas
│   ├── config.py               # Configuración centralizada
│   ├── emailer.py              # Metodo enviar correo
│   ├── setup_config.py         # Solicita los datos requeridos del proyecto
│   ├── config.py               # Obtiene los datos del .env requeridos del proyecto
|   ├── .env                    # Variables de entorno
│   ├── templates/
│   │   └── index.html          # Interfaz HTML para consultas
├── Log/
│   └── bot.log                 # Registros de ejecución
├── Api/
│   └── api.py                  # API REST para acceder a datos
├── Insumos/
│   └── AmazonProductos.db      # Base de datos SQLite
│   └── Producto.xlsx           # Archivo Productos
├── Resultado/
│   └── Resultados.xlsx         # Archivo a enviar por correo
└── README.md                   # Este archivo
```

##  Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes)
- ChromeDriver (para Selenium)

##  Instalación

### 1. Clonar o descargar el proyecto
```bash
cd HAM_Amazon
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows
source .venv/bin/activate  # En Linux/Mac
```

### 3. Instalar librerías requeridas

#### Opción A: Instalar todas de una vez (recomendado)
```bash
pip install -r requirements.txt
```

#### Opción B: Instalar manualmente

```bash
# Framework web
pip install Flask==3.1.0

# Web scraping y automatización
pip install Selenium==4.15.0

# Manejo de variables de entorno
pip install python-dotenv==1.0.0

# Peticiones HTTP
pip install requests==2.31.0


```

### 4. Descargar ChromeDriver

1. Ve a: https://chromedriver.chromium.org/
2. Descarga la versión que coincida con tu versión de Chrome
3. Extrae el archivo `chromedriver.exe`
4. Colócalo en una de estas ubicaciones:
   - En la carpeta del proyecto
   - En `C:\Windows\System32\` (Windows)
   - O agrega su ubicación al PATH del sistema

**Verificar instalación:**
```bash
chromedriver --version
```

### 5. Configurar variables de entorno

Ejucutar el archivo septup_config.py OBLIGATORIO en la primera ejecucion
para crea un archivo `.env` en la raíz del proyecto:
```
cd Script
python septup_config.py

Soliciatara al usuario ingresar las variables requeridas para
el correcto funcionamiento del bot 

```

##  Descripción de Librerías

| Librería | Versión | Propósito |
|----------|---------|----------|
| **Flask** | 3.1.0 | Framework web para la interfaz y API |
| **Selenium** | 4.15.0 | Automatización web para scraping |
| **python-dotenv** | 1.0.0 | Gestión de variables de entorno |
| **requests** | 2.31.0 | Peticiones HTTP (conversión de divisas) |

##  Uso

### 1. Ejecutar Web Main
```bash
cd Script
python main.py
```
El main se encargara de orquesatar todo el flujo,
consulta de rutas, ingreso a la web, generar la base de datos y envia un correo con los resultados.

### 2. Acceder a la Interfaz Web
```bash
python web_app.py
```
Abre tu navegador en: `http://localhost:5000`

**Funcionalidades:**
- Filtrar productos por nombre
- Filtrar por rango de precios (USD)
- Ver tipo de entrega

### 3. Usar la API REST
```bash
cd ../Api
python api.py
```
Abre tu navegador o usa cURL en: `http://localhost:5000`

**Endpoints disponibles:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/diagnostico` | Verifica estado de la BD |
| GET | `/productos` | Obtiene todos los productos |
| GET | `/producto/<id>` | Obtiene un producto por ID |

**Ejemplos:**
```bash
# Ver diagnóstico
curl http://localhost:5000/diagnostico

# Obtener todos los productos
curl http://localhost:5000/productos

# Obtener producto con ID 1
curl http://localhost:5000/producto/1
```

##  Base de Datos

### Estructura de la tabla `Productos`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| idProducto | INTEGER | ID único (autoincremental) |
| Nombre | TEXT | Nombre del producto |
| Precio | REAL | Precio en USD |
| TipoEntrega | TEXT | Tipo de entrega (Prime, estándar, etc.) |

##  Componentes

### `scraper.py`
- Utiliza Selenium WebDriver para automatizar búsquedas en Amazon
- Extrae información de productos (nombre, precio, tipo de entrega)
- Almacena datos en SQLite
- Genera logs en `bot.log`

### `web_app.py`
- Framework Flask para interfaz web
- Filtros avanzados por nombre y rango de precios
- Conexión a BD SQLite

### `api.py`
- API REST con endpoints JSON
- Diagnóstico de BD
- Consultas por ID o listado completo

### `config.py`
- Centraliza rutas y constantes
- Lee variables del archivo `.env`

### `index.html`
- Interfaz responsiva
- Tabla de productos con estilos CSS
- Formulario de filtrado

##  Logs

Los registros se guardan en `Lod/bot.log` con información de:
- Búsquedas realizadas
- Productos encontrados
- Errores y advertencias

Ejemplo:
```
2025-11-12 06:14:05 - INFO - Iniciando búsqueda para: laptop
2025-11-12 06:14:10 - INFO - Producto agregado: Dell Laptop - $799.99
2025-11-12 06:14:15 - INFO - Total de productos encontrados: 20
```

##  Configuración Avanzada

### Cambiar límite de productos
Edita `.env`:
```
LIMITE_PRODUCTOS=50
```

### Cambiar ubicación de BD
Edita `.env`:
```
DB_PATH=C:\ruta\a\tu\bd.db
```

##  Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install Flask==3.1.0
```

### Error: "ModuleNotFoundError: No module named 'selenium'"
```bash
pip install Selenium==4.15.0
```

### Error: "Base de datos no encontrada"
- Verifica que la ruta en `.env` sea correcta
- Asegúrate de que el archivo `AmazonProductos.db` existe

### Error: "No se encuentra ChromeDriver"
- Descarga ChromeDriver desde: https://chromedriver.chromium.org/
- Asegúrate de que esté en el PATH del sistema
- O colócalo en la misma carpeta que el script

### Scraper no encuentra productos
- Verifica tu conexión a internet
- Comprueba que Amazon no haya bloqueado las solicitudes
- Revisa los logs en `bot.log`

##  Archivo requirements.txt

Crea un archivo `requirements.txt` en la raíz del proyecto con:

```txt
Flask==3.1.0
Selenium==4.15.0
python-dotenv==1.0.0
requests==2.31.0
colorlog==6.8.0
```

Luego instala todo con:
```bash
pip install -r requirements.txt
```

##  Autor

Desarrollado como parte del proyecto AlmaMater

##  Licencia

Este proyecto es de código abierto.

---

**Última actualización:** Noviembre 12, 2025
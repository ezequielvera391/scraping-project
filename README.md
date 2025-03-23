# Scraping Letterboxd

Este proyecto permite realizar scraping en **Letterboxd** para construir un conjunto de datos de películas.
Extrae información detallada de cada película y descarga sus pósters, generando un **dataset reutilizable** para cualquier aplicación que necesite información cinematográfica similar a Letterboxd.

---

## Instalación

### 1. Clonar el repositorio  
Ejecuta los siguientes comandos en tu terminal:  

```sh
# Ubicarse en el directorio donde se desea clonar el proyecto
cd /ruta/deseada

# Clonar el repositorio
git clone https://github.com/tu-usuario/scraping-letterboxd.git
cd scraping-letterboxd
```

### 2. Crear y activar un entorno virtual  

```sh
# Crear el entorno virtual
type python &> /dev/null && python -m venv venv || python3 -m venv venv

# Activar el entorno virtual:
# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias  

```sh
pip install -r requirements.txt
```

---

## Entrada del sistema

El scraper utiliza un archivo JSON con la lista de películas como entrada.
Este archivo debe ser creado por el usuario, ya que el que se incluye en el repositorio es solo un ejemplo de prueba.  
El archivo debe tener la siguiente estructura:

```json
[
    {"title": "flow"},
    {"title": "past-lives"},
    {"title": "the-zone-of-interest"},
    {"title": "anatomy-of-a-fall"}
]
```

Este archivo debe estar ubicado en:  
`data/movies.json`

---

## Uso

### Ejecutar el scraper  
Para iniciar el scraping, ejecuta:

```sh
python scraping_letterboxd/main.py
```

El scraper procesará cada película de la lista de entrada, descargando su portada y extrayendo su información.

---

## Salida del sistema

El scraper genera dos tipos de salida:

1. **Pósters de películas**
   - Se guardan en la carpeta `results/`.
   - Los archivos tienen el siguiente formato: `{nombre-pelicula}-cover.jpg`.
   - La ruta en el JSON de salida se ajusta según la configuración.

2. **JSON con información de películas**
   - Se almacena en `results/movie_data.json`.
   - La estructura del JSON es la siguiente:

```json
[
  {
    "title": "The Zone of Interest",
    "sinopsis": "The commandant of Auschwitz, Rudolf Höss, and his wife Hedwig, strive to build a dream life for their family in a house and garden next to the camp.",
    "year": 2023,
    "director": {
      "id": 12756022148002307130,
      "name": "Christian Friedel"
    },
    "genero": {
      "id": 5673693341140147561,
      "name": ""
    },
    "cover": "assets/images/temp/cards/the-zone-of-interest-cover.jpg",
    "was_watched": false,
    "rating": null,
    "actors": [
      {"id": 12756022148002307130, "name": "Christian Friedel"},
      {"id": 11991609446548266039, "name": "Sandra Hüller"}
    ],
    "poster_url": "https://a.ltrbxd.com/resized/film-poster/3/9/8/8/0/0/398800-the-zone-of-interest-0-1000-0-1500-crop.jpg?v=0514f658e1",
    "id": 3
  }
]
```

---

## Configuración

Puedes modificar las rutas de entrada, salida y logs en el archivo `config.py`:

```python
# URL base de Letterboxd
BASE_URL = "https://letterboxd.com/film/"

# Rutas de almacenamiento
DATA_PATH = "./data/movies.json" # De este archivo toma las peliculas que va a buscar
OUTPUT_PATH = "results/" # En esta ruta se guardan las imagenes
LOG_PATH = "logs/scraping.log" # En esta ruta se guardan los logs
CLIENT_ASSETS_PATH = "assets/images/temp/cards/" # Es la ruta del cliente para que el json quede armado correctamente y no necesite modificaciones
```

---

## Tecnologías utilizadas  

- **Python**  
- **Selenium** (automatización de navegación)  
- **BeautifulSoup** (análisis de HTML)  
- **webdriver-manager** (gestión de drivers de navegador)  

---

## Contribución  

Las contribuciones son bienvenidas. Para colaborar:  

1. Realiza un **fork** del repositorio.  
2. Crea una nueva rama con las mejoras o correcciones.  
3. Envía un **pull request** con los cambios propuestos.  

Para cualquier consulta, no dudes en comunicarte.


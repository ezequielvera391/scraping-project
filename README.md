# Scraping Letterboxd

Este proyecto permite realizar scraping en **Letterboxd** para extraer pósters de películas de forma automatizada.

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

El scraper utiliza un archivo JSON con la lista de películas como entrada. Este archivo debe crearlo cada usuario, ya que el que se incluye en el repositorio es solo un ejemplo de prueba.  
El archivo debe tener la siguiente estructura:

```json
[
    {"title": "flow"},
    {"title": "past-lives"},
    {"title": "the-zone-of-interest"},
    {"title": "anatomy-of-a-fall"}
]
```

Debe estar ubicado en `data/movies.json`.

---

## Uso

### Ejecutar el scraper principal  
Para iniciar el scraping, ejecuta:

```sh
python scraping_letterboxd/main.py
```

Los pósters descargados se guardarán en la carpeta `results/` con nombres como `flow-cover.jpg`.

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

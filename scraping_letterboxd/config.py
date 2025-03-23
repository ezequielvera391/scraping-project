# config.py
BASE_URL = "https://letterboxd.com/film/"

# Rutas de almacenamiento
DATA_PATH = "./data/movies.json" # De este archivo toma las peliculas que va a buscar
OUTPUT_PATH = "results/" # En esta ruta se guardan las imagenes
LOG_PATH = "logs/scraping.log" # En esta ruta se guardan los logs
CLIENT_ASSETS_PATH = "assets/images/temp/cards/" # Es la ruta del cliente para que el json quede armado correctamente y no necesite modificaciones
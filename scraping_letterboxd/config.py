# config.py
BASE_URL = "https://letterboxd.com/film/"

# Rutas de almacenamiento
DATA_PATH = "./data/movies.json" # De este archivo toma las peliculas que va a buscar
OUTPUT_PATH = "results/" # En esta ruta se guarda el archivo json
OUTPUT_COVERS_PATH = "results/covers/" # En esta ruta se guardan las portadas miniatura 16:9
OUTPUT_POSTERS_PATH = "results/posters/" # En esta ruta se guardan las portadas apaisadas
LOG_PATH = "logs/" # En esta ruta se guardan los logs
CLIENT_COVERS_PATH = "assets/images/temp/cards/" # Es la ruta del cover del cliente para que el json quede armado correctamente y no necesite modificaciones
CLIENT_POSTERS_PATH = "assets/images/temp/posters/" # Es la ruta de la portada del cliente para que el json quede armado correctamente y no necesite modificaciones
import os
import time
import json
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from scraping_letterboxd.utils import setup_logger, ensure_dir_exists, log_summary, generate_id
from scraping_letterboxd.config import BASE_URL, DATA_PATH, OUTPUT_PATH, LOG_PATH, CLIENT_COVERS_PATH, OUTPUT_COVERS_PATH, OUTPUT_POSTERS_PATH, CLIENT_POSTERS_PATH

ensure_dir_exists("results")
logger = setup_logger(LOG_PATH)

def setup_driver() -> webdriver.Chrome | None:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logger.error(f"Error al iniciar el WebDriver: {e}")
        return 

def get_movie_data(film_name, year):
    """
    Obtiene los datos de la película y descarga las imágenes.
    Intenta la URL sin año primero. Si falla y el año está en el JSON, intenta la URL con año.
    """
    driver = setup_driver()
    if not driver:
        return None

    film_urls = [f"{BASE_URL}{film_name}/"]
    # Letterboxd a vece usa el formato nombre-pelicula-yyyy donde yyyy es el año de lanzamiento, si falla la primera vez se intenta con esta nueva manera
    if year:  
        film_urls.append(f"{BASE_URL}{film_name}-{year}/")

    for index, film_url in enumerate(film_urls):
        driver.get(film_url)
        time.sleep(3)

        try:
            title = driver.find_element(By.CSS_SELECTOR, "h1.headline-1").text
            sinopsis = driver.find_element(By.CSS_SELECTOR, "div.truncate p").text
            year = int(driver.find_element(By.CSS_SELECTOR, "div.releaseyear a").text)
            director = driver.find_element(By.CSS_SELECTOR, "a.text-slug").text
            genero = driver.find_element(By.CSS_SELECTOR, "a[href*='/films/genre/']").text
            actors = [elem.text for elem in driver.find_elements(By.CSS_SELECTOR, "a[href*='/actor/']")][:5]

            cover_element = driver.find_element(By.CSS_SELECTOR, "section.poster-list a[data-js-trigger='postermodal']")
            cover_url = cover_element.get_attribute("href")
            backdrop_element = driver.find_element(By.ID, "backdrop")
            poster_url = backdrop_element.get_attribute("data-backdrop")

            cover_filename = f"{film_name}-cover.jpg"
            cover_path = os.path.join(OUTPUT_COVERS_PATH, cover_filename)
            download_image(cover_url, cover_path)

            poster_filename = f"{film_name}-poster.jpg"
            poster_path = os.path.join(OUTPUT_POSTERS_PATH, poster_filename)
            download_image(poster_url, poster_path)

            driver.quit()

            return {
                "title": title,
                "sinopsis": sinopsis,
                "year": year,
                "director": {"id": generate_id(director), "name": director},
                "genero": {"id": generate_id(genero), "name": genero},
                "cover": f"{CLIENT_COVERS_PATH}{cover_filename}",
                "was_watched": False,
                "rating": None,
                "actors": [{"id": generate_id(actor), "name": actor} for actor in actors],
                "poster_url": f"{CLIENT_POSTERS_PATH}{poster_filename}"
            }
        except Exception as e:
            logger.warning(f"Error obteniendo datos desde {film_url}: {e}")

            # Si la primera búsqueda falló y no hay segunda URL, se corta el intento
            if index == 0 and len(film_urls) == 1:
                break

    driver.quit()
    return 

def download_image(image_url, save_path):
    """
    Descarga una imagen desde una URL y la guarda en el sistema de archivos.
    """
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            logger.info(f"Imagen guardada en {save_path}")
            return True
        else:
            logger.error(f"Error al descargar la imagen: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error en la descarga: {e}")
        return False

def main():
    ensure_dir_exists(OUTPUT_PATH)

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            movies = json.load(file)
    except Exception as e:
        logger.error(f"Error al leer el archivo JSON: {e}")
        return

    total = len(movies)
    success = 0
    failed_movies = []
    movie_data_list = []

    for idx, movie in enumerate(movies, start=1):
        film_name = movie["title"].replace(" ", "-").lower()
        year = movie.get("year", "")
        movie_data = get_movie_data(film_name, year)

        if movie_data:
            movie_data["id"] = idx
            movie_data_list.append(movie_data)
            success += 1
        else:
            failed_movies.append(film_name)

    with open(os.path.join(OUTPUT_PATH, "movies_data.json"), "w", encoding="utf-8") as json_file:
        json.dump(movie_data_list, json_file, indent=2, ensure_ascii=False)

    log_summary(logger, total, success, failed_movies)

if __name__ == "__main__":
    main()

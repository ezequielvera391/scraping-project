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
        print(f"Error al iniciar el WebDriver: {e}")
        return  

def get_movie_data(film_url, film_name):
    driver = setup_driver()
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
            "cover": f"{CLIENT_COVERS_PATH}{film_name}-cover.jpg",
            "was_watched": False,
            "rating": None,
            "actors": [{"id": generate_id(actor), "name": actor} for actor in actors],
            "poster_url": f"{CLIENT_POSTERS_PATH}{film_name}-poster.jpg",  # Ruta local del poster descargado
            "cover_url": cover_url
        }
    except Exception as e:
        logger.error(f"Error obteniendo datos de {film_url}: {e}")
        driver.quit()
        return None

def download_image(image_url, save_path):
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
        film_url = f"{BASE_URL}{film_name}/"
        
        movie_data = get_movie_data(film_url, film_name)
        if movie_data:
            save_path = os.path.join(OUTPUT_COVERS_PATH, f"{film_name}-cover.jpg")
            if download_image(movie_data["cover_url"], save_path):
                movie_data["id"] = idx
                del movie_data["cover_url"]
                movie_data_list.append(movie_data)
                success += 1
            else:
                failed_movies.append(film_name)
        else:
            failed_movies.append(film_name)

    with open(os.path.join(OUTPUT_PATH, "movies_data.json"), "w", encoding="utf-8") as json_file:
        json.dump(movie_data_list, json_file, indent=2, ensure_ascii=False)

    log_summary(logger, total, success, failed_movies)

if __name__ == "__main__":
    main()

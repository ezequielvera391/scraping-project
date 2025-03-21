import os
import time
import json
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from scraping_letterboxd.utils import setup_logger, ensure_dir_exists, log_summary
from scraping_letterboxd.config import BASE_URL, DATA_PATH, OUTPUT_PATH, LOG_PATH

# Configurar logger
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

        service = Service(ChromeDriverManager().install())  # Configura el servicio correctamente
        driver = webdriver.Chrome(service=service, options=options)  # Usa service y options correctamente
        return driver
    except Exception as e:
        print(f"Error al iniciar el WebDriver: {e}")
        return  
def get_poster_url(poster_url):
    driver = setup_driver()
    driver.get(poster_url)
    time.sleep(3)

    try:
        poster_element = driver.find_element(By.CSS_SELECTOR, "section.poster-list a[data-js-trigger='postermodal']")
        poster_url = poster_element.get_attribute("href")
        driver.quit()
        return poster_url
    except Exception as e:
        logger.error(f"Error obteniendo póster de {poster_url}: {e}")
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

    for movie in movies:
        film_name = movie["title"].replace(" ", "-").lower()
        film_url = f"{BASE_URL}{film_name}/"

        poster_url = get_poster_url(film_url)
        if poster_url:
            save_path = os.path.join(OUTPUT_PATH, f"{film_name}-cover.jpg")
            if download_image(poster_url, save_path):
                success += 1
            else:
                failed_movies.append(film_name)
        else:
            failed_movies.append(film_name)

    log_summary(logger, total, success, failed_movies)

if __name__ == "__main__":
    main()
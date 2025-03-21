import sys
import os

# Agregar la ruta del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraping_letterboxd.scraper import main

if __name__ == "__main__":
    main()
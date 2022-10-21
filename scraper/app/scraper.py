import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from app.product_dto import ProductDTO, UnitPrice
from contextlib import contextmanager
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

PRICE_DOLLARS_SELECTOR = ".shelfProductTile-information .price .price-dollars"


def get_path_to_chromedriver():
    return os.getenv("CHROMEDRIVER_PATH", r"./chromedriver")


@contextmanager
def get_driver():
    driver = webdriver.Chrome(options=options, service=Service(executable_path=get_path_to_chromedriver()))

    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine", fix_hairline=True, )
    yield driver
    driver.quit()


def parse_unit_price(unit_price: str):
    import re
    m = re.match(r'\$(\d+\.\d+) / (\w+)', unit_price)
    if m:
        price, unit = m.groups()
        return UnitPrice(price=price, unit=unit)


def get_product_price(id_: str, url: str, category: str = None, timeout_seconds=10) -> ProductDTO:
    logger.info(f"Getting product price for: {url} {category}")
    with get_driver() as driver:
        driver.get(url)
        WebDriverWait(driver, timeout_seconds).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, PRICE_DOLLARS_SELECTOR)
            )
        )
        html = driver.page_source
        return parse_product_html(html, url=url, category=category, id_=id_)


def parse_product_html(html: str, id_: str, url: str, category: str) -> ProductDTO:
    soup = BeautifulSoup(html, 'html.parser')
    product_title = soup.select_one("h1.shelfProductTile-title").text
    dollars = soup.select_one(PRICE_DOLLARS_SELECTOR).text
    cents = soup.select_one(".shelfProductTile-information .price .price-cents").text
    unit_price_text = soup.select_one(".shelfProductTile-information .shelfProductTile-cupPrice").text
    unit_price_parsed = parse_unit_price(unit_price_text)
    price = float(f"{dollars}.{cents}")
    p = ProductDTO(id=id_, name=product_title, category=category, url=url, price=price, unit_price=unit_price_parsed)
    logger.info(f'{p}')
    return p


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sample_product = "https://www.woolworths.com.au/shop/productdetails/689674/shine-antibacterial-dishwashing-liquid-lemon"
    logger.info(get_product_price(url=sample_product, category='dishwashing'))

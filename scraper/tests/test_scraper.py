import contextlib
from unittest.mock import patch, MagicMock

import pytest
import selenium.webdriver.support.ui

from app import scraper
from app.product_dto import UnitPrice, Product
from selenium.common.exceptions import TimeoutException

URL = 'http://a.com/product'
CATEGORY = 'Category'
HTML_PRODUCT_IN_STOCK = """
        <html>
          <body>
            <div class="shelfProductTile-information">
              <h1 class="shelfProductTile-title heading3">Oat Milk</h1>
              <ar-product-price class="ar-product-price">
                <div class="shelfProductTile-price">
                  <div>
                    <div class="price price--large">
                      <span class="price-symbol">$</span>
                      <span class="price-dollars">5</span>
                      <div class="price-centsPer">
                        <span class="sr-only">.</span>
                        <span class="price-cents">23</span>
                      </div>
                    </div>
                  </div>
                  <div class="shelfProductTile-cupPrice">$0.52 / 100ML</div>
                </div>
              </ar-product-price>
            </div>
          </body>
        </html>
        """


@contextlib.contextmanager
def driver_for_when_product_in_stock():
    magic_mock = MagicMock()
    magic_mock.page_source = HTML_PRODUCT_IN_STOCK
    yield magic_mock


def assert_in_stock_product_scraped(product: Product):
    assert product.name == 'Oat Milk'
    assert product.url == URL
    assert product.category == CATEGORY
    assert product.price == 5.23
    assert product.unit_price == UnitPrice(price='0.52', unit='100ML')


class TestGetProductPrice:

    @patch.object(selenium.webdriver.support.ui, 'WebDriverWait')
    @patch.object(scraper, 'get_driver', side_effect=driver_for_when_product_in_stock)
    def test_when_product_in_stock(self, mock_driver, mock_wait):
        product = scraper.get_product_price(
            url='http://a.com/product',
            category='Category'
        )
        assert_in_stock_product_scraped(product)

    # TODO: do we want to classify if product out of stock / only available in-store?
    @patch.object(selenium.webdriver.support.ui.WebDriverWait, 'until',
                  side_effect=TimeoutException())
    @patch.object(scraper, 'get_driver')
    def test_when_product_out_of_stock(self, mock_driver, mock_wait):
        with pytest.raises(TimeoutException):
            scraper.get_product_price(
                url='',
                category='',
                timeout_seconds=0
            )


class TestParseProductHTML:
    def test_when_product_in_stock(self):
        product = scraper.parse_product_html(html=HTML_PRODUCT_IN_STOCK, url=URL, category=CATEGORY)
        assert_in_stock_product_scraped(product)

import pytest

from app.parser import extract_products_from_file
from app.product_info import ProductInfo

SAMPLE_YAML = """
---
- category: 'oats'
  products:
    - url: http://www.shop.com/oats
      name: 'Oats - 500g'
- category: 'milk'
  products:
    - url: http://www.shop.com/milk-lactose-free
      name: 'Lactose Free Milk 1l'
    - url: http://www.shop.com/milk
      name: 'Full-Cream Milk 1l'
"""


@pytest.fixture()
def sample_products_file(tmp_path):
    file = tmp_path / 'products.yaml'
    file.write_text(SAMPLE_YAML)
    yield file


def test_parser(sample_products_file):
    assert extract_products_from_file(filepath=sample_products_file) == [
        ProductInfo(name='Oats - 500g', url='http://www.shop.com/oats', category='oats'),
        ProductInfo(name='Lactose Free Milk 1l', url='http://www.shop.com/milk-lactose-free', category='milk'),
        ProductInfo(name='Full-Cream Milk 1l', url='http://www.shop.com/milk', category='milk'),
    ]

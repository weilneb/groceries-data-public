from typing import List, Dict

import yaml

from app.product_info import ProductInfo


def extract_products_from_file(filepath: str) -> List[ProductInfo]:
    with open(filepath) as f:
        obj = yaml.load(f, Loader=yaml.FullLoader)
        return extract_products(obj)


def extract_products(list_of_objects: List[Dict]) -> List[ProductInfo]:
    products = []
    for category in list_of_objects:
        for product in category['products']:
            products.append(ProductInfo(name=product['name'],
                                        url=product['url'],
                                        category=category['category']))

    return products

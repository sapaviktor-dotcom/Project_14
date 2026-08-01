import json
from typing import List
from src.product import Product
from src.category import Category


def load_data_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и данные о продуктах из файла JSON.

    Аргументы:
        file_path: путь к файлу JSON.

    Возвращает:
        Список объектов категории

    Исключения:
        FileNotFoundError: Если файл не существует
        json.JSONDecodeError: Если файл содержит недопустимый JSON
    Load categories and products data from JSON file.

    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for category_data in data:
        products = []
        for product_data in category_data.get("products", []):
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            products.append(product)

        category = Category(name=category_data["name"], description=category_data["description"], products=products)
        categories.append(category)

    return categories

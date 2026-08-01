from typing import List
from src.product import Product


class Category:
    """Класс, представляющий категорию продукта."""

    # Атрибуты класса
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """
        Инициализируем экземпляр категории.

         Аргументы:
             name: Название категории (string)
             description: Описание категории (string)
             products: Список объектов продукта в этой категории.

        """

        self.name = name
        self.description = description
        self.products = products

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)

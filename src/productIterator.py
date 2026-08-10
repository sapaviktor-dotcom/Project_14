from src.category import Category
from src.product import Product


class ProductIterator:
    """
     Итератор для перебора товаров в категории
    Позволяет использовать цикл for для перебора товаров категории
    """

    def __init__(self, category: Category):
        self.category = category
        self.index = 0

    def __iter__(self) -> "ProductIterator":
        return self

    def __next__(self) -> Product:
        """
        Возвращает следующий товар из категории
        При достижении конца списка выбрасывает StopIteration
        """
        products = self.category.get_products_list()
        if self.index < len(products):
            product = products[self.index]
            self.index += 1
            return product
        raise StopIteration

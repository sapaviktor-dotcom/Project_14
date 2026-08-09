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
        self.__products = products  # Приватный атрибут

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)

    @property
    def products(self) -> str:
        """
        Геттер для продуктов с форматированным выводом.
        Возвращает:
            Строка со всеми продуктами в формате:
            "Название продукта, X руб. Остаток: X шт.\n"
        """
        if not self.__products:
            return ""

        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def add_product(self, product: Product) -> None:
        """
        ЗАДАНИЕ 3: Добавляет продукт в категорию.
        Проверяет, что добавляемый объект является экземпляром Product или его наследником.
        Используется функция isinstance() для проверки.

        Аргументы:
            product: Объект Product для добавления
        Примечание:
            Увеличивает product_count на 1
        """
        # Проверяем, что объект является экземпляром Product или его наследником
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

    def get_products_list(self) -> List[Product]:
        """
        Получает список продуктов (для внутреннего использования/тестирования).

        Возвращает:
            Список объектов Product
        """
        return self.__products

    def __str__(self) -> str:
        """
        Задание 1: Строковое представление категории
        Возвращает строку в формате: "Название категории, количество продуктов: X шт."
        Где X - общее количество всех товаров на складе в этой категории
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def get_total_quantity(self) -> int:
        """
        Вспомогательный метод для получения общего количества товаров в категории
        """
        return sum(product.quantity for product in self.__products)

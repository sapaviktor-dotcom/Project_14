from typing import List, Union

from src.base import BaseStorage
from src.product import Product
from src.exceptions import ZeroQuantityError


class Category(BaseStorage):
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
        Добавляет продукт в категорию с обработкой нулевого количества.
        Проверяет, что добавляемый объект является экземпляром Product или его наследником.
        Используется функция isinstance() для проверки.

        Аргументы:
            product: Объект Product для добавления
        Примечание:
            Увеличивает product_count на 1
        """
        try:
            # СНАЧАЛА проверяем тип объекта
            if not isinstance(product, Product):
                raise TypeError("Можно добавлять только объекты класса Product или его наследников")

            # ПОТОМ проверяем количество
            if product.quantity == 0:
                raise ZeroQuantityError("Товар с нулевым количеством не может быть добавлен")

            # Если все проверки пройдены - добавляем продукт
            self.__products.append(product)
            Category.product_count += 1

        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
        except TypeError as e:
            print(f"Ошибка типа: {e}")
        else:
            print("Товар добавлен успешно")
        finally:
            print("Обработка добавления товара завершена")

    def get_products_list(self) -> List[Product]:
        """
        Получает список продуктов (для внутреннего использования/тестирования).

        Возвращает:
            Список объектов Product
        """
        return self.__products

    def __str__(self) -> str:
        """
        Строковое представление категории
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

    def get_total_price(self) -> Union[int, float]:
        """
        Получение общей стоимости всех товаров в категории (реализация абстрактного метода)
        """
        return sum(product.price * product.quantity for product in self.__products)

    def get_average_price(self) -> Union[int, float]:
        """
        Подсчет среднего ценника всех товаров в категории.
        Если товаров нет, возвращает 0.
        """
        try:
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0

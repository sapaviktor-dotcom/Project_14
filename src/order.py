from typing import Union

from src.base import BaseStorage
from src.product import Product


class Order(BaseStorage):
    """Класс, представляющий заказ на один товар."""

    def __init__(self, product: Product, quantity: int):
        """
        Инициализация заказа.

        Аргументы:
            product: Объект Product
            quantity: Количество товара в заказе
        """
        self.product = product
        self.quantity = quantity

    def get_products_list(self) -> list:
        """
        Получение списка товаров в заказе.

        Возвращает:
            list: Список с одним товаром
        """
        return [self.product]

    def add_product(self, product: Product) -> None:
        """
        Добавление товара в заказ (не поддерживается для Order).

        Исключения:
            NotImplementedError: так как Order содержит только один товар
        """
        raise NotImplementedError("Order не поддерживает добавление товаров")

    def get_total_price(self) -> Union[int, float]:
        """Расчет итоговой стоимости заказа."""
        return self.product.price * self.quantity

    def get_total_quantity(self) -> int:
        """Получение количества товаров в заказе."""
        return self.quantity

    def __str__(self) -> str:
        """Строковое представление заказа."""
        total_price = self.get_total_price()
        return f"{self.product.name} - Количество: {self.quantity} шт., Стоимость: {total_price} руб"

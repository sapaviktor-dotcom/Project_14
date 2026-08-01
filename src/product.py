from typing import Union


class Product:
    """Класс, представляющий товар в магазине."""

    def __init__(self, name: str, description: str, price: Union[int, float], quantity: int):
        """
        Инициализация экземпляра продукта.

         Аргументы:
             name: название продукта (string)
             description: описание продукта (string)
             price: цена продукта (integer or float, can be with kopecks)
             quantity: количество продукта на складе (integer, measured in pieces)
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

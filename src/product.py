from typing import Any, Dict
from typing import Union

from src.base import BaseProduct


class ProductMixin:  # pragma: no cover
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):  # pragma: no cover
        """Логируем создание объекта"""
        # Формируем строку с параметрами
        params = []

        # Добавляем позиционные аргументы
        for arg in args:
            params.append(repr(arg))

        # Добавляем именованные аргументы
        for key, value in kwargs.items():
            params.append(f"{key}={repr(value)}")

        # Выводим информацию в консоль
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: {', '.join(params)}")

        # Вызываем родительский конструктор
        super().__init__(*args, **kwargs)

class Product(BaseProduct, ProductMixin):
    # Глобальный список всех товаров
    all_products = []

    def __init__(self, name: str, description: str, price: Union[int, float], quantity: int):
        """
        Инициализация экземпляра продукта.

         Аргументы:
             name: название продукта (string)
             description: описание продукта (string)
             price: цена продукта (integer or float, can be with kopecks)
             quantity: количество продукта на складе (integer)
        """
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        # Добавляем товар в глобальный список
        Product.all_products.append(self)

    @property
    def price(self) -> Union[int, float]:
        return self.__price

    @price.setter
    def price(self, new_price: Union[int, float]) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        """
        Класс-метод для создания нового экземпляра Product из данных словаря.
        Автоматически проверяет наличие дубликатов в глобальном списке.
        """
        new_name = product_data.get("name", "")
        new_description = product_data.get("description", "")
        new_price = product_data.get("price", 0)
        new_quantity = product_data.get("quantity", 0)

        # Ищем товар с таким же именем в глобальном списке
        for product in cls.all_products:
            if product.name.lower() == new_name.lower():
                # Обновляем существующий товар
                product.quantity += new_quantity
                if new_price > product.price:
                    product.price = new_price
                if new_description and new_description != product.description:
                    product.description = new_description
                return product

        # Создаем новый товар
        return cls(name=new_name, description=new_description, price=new_price, quantity=new_quantity)

    def __str__(self) -> str:
        """
        Задание 1: Строковое представление продукта
        """
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> Union[int, float]:
        """
        Магический метод сложения с ограничением по классам
        Возвращает сумму произведений цены на количество у двух объектов
        Проверяет, что объекты принадлежат одному классу
        """
        # Проверяем, что оба объекта одного класса
        if not isinstance(other, type(self)):
            raise TypeError(f"Нельзя складывать товары разных классов: {type(self).__name__} и {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """Класс Смартфон, наследник Product"""

    def __init__(
        self,
        name: str,
        description: str,
        price: Union[int, float],
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ):
        """
        Инициализация экземпляра смартфона.

        Аргументы:
            name: название продукта
            description: описание продукта
            price: цена продукта
            quantity: количество на складе
            efficiency: производительность
            model: модель
            memory: объем встроенной памяти (ГБ)
            color: цвет
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс Трава газонная, наследник Product"""

    def __init__(
        self,
        name: str,
        description: str,
        price: Union[int, float],
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        """
        Инициализация экземпляра травы газонной.

        Аргументы:
            name: название продукта
            description: описание продукта
            price: цена продукта
            quantity: количество на складе
            country: страна-производитель
            germination_period: срок прорастания (дней)
            color: цвет
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

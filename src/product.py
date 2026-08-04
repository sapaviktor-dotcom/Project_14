from typing import Union, Dict, Any


class Product:
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
        Задание 2: Магический метод сложения
        Возвращает сумму произведений цены на количество у двух объектов
        """
        if not isinstance(other, Product):
            raise TypeError(f"Нельзя сложить Product с {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)

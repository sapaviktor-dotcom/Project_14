from typing import Union, List
from src.base import BaseStorage
from src.product import Product
from src.exceptions import ZeroQuantityError


class Order(BaseStorage):
    """Класс, представляющий заказ на один товар."""

    def __init__(self, product: Product, quantity: int):
        """
        Инициализация заказа.
        """
        try:
            if quantity == 0:
                raise ZeroQuantityError(f"Заказ с нулевым количеством товара '{product.name}' невозможен")

            self.product = product
            self.quantity = quantity
            print(f"Заказ на товар '{product.name}' в количестве {quantity} шт. создан успешно")

        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
            raise
        finally:
            print("Обработка создания заказа завершена")

    def get_products_list(self) -> List[Product]:
        """Получение списка товаров в заказе."""
        return [self.product]

    def add_product(self, product: Product) -> None:
        """Добавление товара в заказ (не поддерживается для Order)."""
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

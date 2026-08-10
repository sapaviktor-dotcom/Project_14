from abc import ABC, abstractmethod
from typing import Union


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod  # pragma: no cover
    def __init__(self, name: str, description: str, price: Union[int, float], quantity: int):
        pass

    @property  # pragma: no cover
    @abstractmethod
    def price(self) -> Union[int, float]:
        pass

    @price.setter  # pragma: no cover
    @abstractmethod
    def price(self, new_price: Union[int, float]) -> None:
        pass

    @abstractmethod  # pragma: no cover
    def __str__(self) -> str:
        pass

    @abstractmethod  # pragma: no cover
    def __add__(self, other: "BaseProduct") -> Union[int, float]:
        pass


class BaseStorage(ABC):
    """
    Абстрактный базовый класс для хранения товаров.
    Объединяет общую функциональность классов Category и Order.
    """

    @abstractmethod  # pragma: no cover
    def __init__(self, name: str, description: str):
        """
        Инициализация хранилища товаров

        Args:
            name: название хранилища (категории или заказа)
            description: описание хранилища
        """
        pass

    @abstractmethod  # pragma: no cover
    def add_product(self, product) -> None:
        """
        Добавление товара в хранилище

        Args:
            product: добавляемый товар
        """
        pass

    @abstractmethod  # pragma: no cover
    def get_total_quantity(self) -> int:
        """
        Получение общего количества товаров

        Returns:
            int: общее количество товаров
        """
        pass

    @abstractmethod  # pragma: no cover
    def get_total_price(self) -> Union[int, float]:
        """
        Получение общей стоимости всех товаров

        Returns:
            Union[int, float]: общая стоимость
        """
        pass

    @abstractmethod  # pragma: no cover
    def __str__(self) -> str:
        """Строковое представление хранилища"""
        pass

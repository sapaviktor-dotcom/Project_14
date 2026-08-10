import pytest
from src.product import Product
from src.order import Order


class TestOrder:
    """Тесты для класса Order."""

    def test_order_initialization(self):
        """Тест инициализации заказа."""
        product = Product("Ноутбук", "Игровой ноутбук", 50000, 10)
        order = Order(product, 2)

        assert order.product == product
        assert order.quantity == 2

    def test_get_products_list(self):
        """Тест получения списка товаров."""
        product = Product("Мышь", "Беспроводная мышь", 1500, 5)
        order = Order(product, 3)

        products = order.get_products_list()

        assert isinstance(products, list)
        assert len(products) == 1
        assert products[0] == product

    def test_add_product_raises_error(self):
        """Тест, что добавление товара вызывает NotImplementedError."""
        product = Product("Клавиатура", "Механическая клавиатура", 3000, 7)
        order = Order(product, 1)

        with pytest.raises(NotImplementedError, match="Order не поддерживает добавление товаров"):
            order.add_product(Product("Монитор", "27-дюймовый монитор", 25000, 3))

    def test_get_total_price(self):
        """Тест расчета итоговой стоимости."""
        product = Product("Телефон", "Смартфон", 60000, 2)
        order = Order(product, 3)

        assert order.get_total_price() == 180000

    def test_get_total_price_with_float(self):
        """Тест расчета итоговой стоимости с дробной ценой."""
        product = Product("Чехол", "Силиконовый чехол", 999.99, 8)
        order = Order(product, 2)

        assert order.get_total_price() == 1999.98

    def test_get_total_quantity(self):
        """Тест получения количества товаров."""
        product = Product("Наушники", "Беспроводные наушники", 5000, 4)
        order = Order(product, 5)

        assert order.get_total_quantity() == 5

    def test_str_representation(self):
        """Тест строкового представления заказа."""
        product = Product("Планшет", "Планшет для рисования", 30000, 3)
        order = Order(product, 2)

        expected = "Планшет - Количество: 2 шт., Стоимость: 60000 руб"
        assert str(order) == expected

    def test_str_with_float_price(self):
        """Тест строкового представления с дробной ценой."""
        product = Product("Кабель", "USB-C кабель", 499.50, 6)
        order = Order(product, 3)

        expected = "Кабель - Количество: 3 шт., Стоимость: 1498.5 руб"
        assert str(order) == expected

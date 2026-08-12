import pytest

from src.order import Order
from src.product import LawnGrass, Product, Smartphone


class TestBaseProductCoverage:
    """Дополнительные тесты для покрытия всех строк BaseProduct."""

    def test_base_product_property_price_through_inheritance(self):
        """Тест свойства price через наследование."""
        product = Product("Тест", "Описание", 100, 5)
        assert product.price == 100
        product.price = 150
        assert product.price == 150

    def test_base_product_str_through_inheritance(self):
        """Тест __str__ через наследование."""
        product = Product("Тест", "Описание", 100, 5)
        assert str(product) == "Тест, 100 руб. Остаток: 5 шт."

    def test_base_product_add_through_inheritance(self):
        """Тест __add__ через наследование."""
        product1 = Product("Товар1", "Описание1", 100, 2)
        product2 = Product("Товар2", "Описание2", 200, 3)
        result = product1 + product2
        assert result == 800

    def test_base_product_init_through_inheritance(self):
        """Тест __init__ через наследование."""
        product = Product("Ноутбук", "Игровой ноутбук", 50000, 10)
        assert product.name == "Ноутбук"
        assert product.description == "Игровой ноутбук"
        assert product.price == 50000
        assert product.quantity == 10

    def test_base_product_price_setter_through_inheritance(self):
        """Тест сеттера price через наследование."""
        product = Product("Телефон", "Смартфон", 30000, 5)
        product.price = 35000
        assert product.price == 35000
        product.price = -1000
        assert product.price == 35000


class TestBaseStorageCoverage:
    """Дополнительные тесты для покрытия всех строк BaseStorage."""

    def test_base_storage_init_through_inheritance(self):
        """Тест __init__ через наследование."""
        product = Product("Тест", "Описание", 100, 5)
        order = Order(product, 2)
        assert order.product == product
        assert order.quantity == 2

    def test_base_storage_add_product_through_inheritance(self):
        """Тест add_product через наследование."""
        product = Product("Тест", "Описание", 100, 5)
        order = Order(product, 2)
        with pytest.raises(NotImplementedError) as exc_info:
            order.add_product(product)
        assert "Order не поддерживает добавление товаров" in str(exc_info.value)

    def test_base_storage_get_total_quantity_through_inheritance(self):
        """Тест get_total_quantity через наследование."""
        product = Product("Тест", "Описание", 100, 5)
        order = Order(product, 3)
        assert order.get_total_quantity() == 3

    def test_base_storage_get_total_price_through_inheritance(self):
        """Тест get_total_price через наследование."""
        product = Product("Тест", "Описание", 200, 5)
        order = Order(product, 4)
        assert order.get_total_price() == 800

    def test_base_storage_str_through_inheritance(self):
        """Тест __str__ через наследование."""
        product = Product("Ноутбук", "Игровой", 50000, 10)
        order = Order(product, 2)
        expected = "Ноутбук - Количество: 2 шт., Стоимость: 100000 руб"
        assert str(order) == expected


class TestProductCoverage:
    """Дополнительные тесты для покрытия всех строк Product."""

    def test_product_new_product_creates_new(self):
        """Тест new_product для создания нового товара."""
        from src.product import Product

        Product.all_products.clear()

        product_data = {"name": "Новый товар", "description": "Описание", "price": 1000, "quantity": 5}
        product = Product.new_product(product_data)

        assert product.name == "Новый товар"
        assert product.price == 1000
        assert product.quantity == 5
        assert len(Product.all_products) == 1

    def test_product_new_product_updates_existing(self):
        """Тест new_product для обновления существующего товара."""
        from src.product import Product

        Product.all_products.clear()

        product1_data = {"name": "Товар", "description": "Описание", "price": 1000, "quantity": 5}
        product1 = Product.new_product(product1_data)

        product2_data = {"name": "Товар", "description": "Новое описание", "price": 1500, "quantity": 3}
        product2 = Product.new_product(product2_data)

        assert product1 is product2
        assert product1.quantity == 8
        assert product1.price == 1500
        assert product1.description == "Новое описание"
        assert len(Product.all_products) == 1

    def test_product_new_product_updates_only_quantity_if_price_lower(self):
        """Тест new_product: обновляется только количество, если цена ниже."""
        from src.product import Product

        Product.all_products.clear()

        product1_data = {"name": "Товар", "description": "Описание", "price": 2000, "quantity": 5}
        product1 = Product.new_product(product1_data)

        product2_data = {"name": "Товар", "description": "Описание", "price": 1500, "quantity": 3}
        product2 = Product.new_product(product2_data)

        assert product1.price == 2000  # Цена не изменилась (была выше)
        assert product1.description == "Описание"  # Описание не изменилось
        assert product1.quantity == 8  # Количество увеличилось: 5 + 3
        assert product2 is product1  # Должен вернуться тот же объект
        assert len(Product.all_products) == 1

    def test_product_new_product_updates_description_if_new(self):
        """Тест new_product: обновляется описание, если новое отличается."""
        from src.product import Product

        Product.all_products.clear()

        product1_data = {"name": "Товар", "description": "Старое описание", "price": 1000, "quantity": 5}
        product1 = Product.new_product(product1_data)

        product2_data = {"name": "Товар", "description": "Новое описание", "price": 1000, "quantity": 3}
        product2 = Product.new_product(product2_data)

        assert product1.description == "Новое описание"  # Описание обновилось
        assert product1.quantity == 8  # Количество увеличилось
        assert product1.price == 1000  # Цена не изменилась
        assert product2 is product1  # Вернулся существующий объект
        assert len(Product.all_products) == 1  # В списке только один продукт

    def test_product_new_product_ignores_empty_description(self):
        """Тест new_product: игнорирует пустое описание."""
        from src.product import Product

        Product.all_products.clear()

        product1_data = {"name": "Товар", "description": "Описание", "price": 1000, "quantity": 5}
        product1 = Product.new_product(product1_data)

        product2_data = {"name": "Товар", "description": "", "price": 1000, "quantity": 3}
        product2 = Product.new_product(product2_data)

        assert product1.description == "Описание"  # Описание не изменилось
        assert product1.quantity == 8  # Количество увеличилось
        assert product2 is product1
        assert len(Product.all_products) == 1

    def test_product_add_same_class(self):
        """Тест __add__ с объектами одного класса."""
        product1 = Product("Товар1", "Описание1", 100, 2)
        product2 = Product("Товар2", "Описание2", 200, 3)
        result = product1 + product2
        assert result == 800

    def test_product_add_different_classes(self):
        """Тест __add__ с разными классами."""
        product = Product("Товар", "Описание", 100, 2)
        smartphone = Smartphone("Phone", "Smart", 500, 1, "High", "Model", 128, "Black")

        result = product + smartphone
        expected = (100 * 2) + (500 * 1)
        assert result == expected

    def test_product_price_setter_validates(self, capsys):
        """Тест сеттера price с валидацией."""
        product = Product("Товар", "Описание", 100, 5)
        product.price = -50
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100

        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100

        product.price = 200
        assert product.price == 200

    def test_product_str_with_float_price(self):
        """Тест __str__ с дробной ценой."""
        product = Product("Товар", "Описание", 99.99, 3)
        expected = "Товар, 99.99 руб. Остаток: 3 шт."
        assert str(product) == expected

    def test_product_all_products_global_list(self):
        """Тест глобального списка all_products."""
        from src.product import Product

        Product.all_products.clear()

        product1 = Product("Товар1", "Описание1", 100, 2)
        product2 = Product("Товар2", "Описание2", 200, 3)

        assert len(Product.all_products) == 2
        assert product1 in Product.all_products
        assert product2 in Product.all_products

    def test_smartphone_inheritance(self):
        """Тест наследования Smartphone."""
        smartphone = Smartphone(
            "iPhone 15", "Флагманский смартфон", 100000, 5, "Высокая", "iPhone 15 Pro", 256, "Титан"
        )
        assert smartphone.name == "iPhone 15"
        assert smartphone.price == 100000
        assert smartphone.quantity == 5
        assert smartphone.efficiency == "Высокая"
        assert smartphone.model == "iPhone 15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Титан"

    def test_lawn_grass_inheritance(self):
        """Тест наследования LawnGrass."""
        grass = LawnGrass("Газонная трава", "Смесь для спортивного газона", 1500, 10, "Германия", 14, "Зеленый")
        assert grass.name == "Газонная трава"
        assert grass.price == 1500
        assert grass.quantity == 10
        assert grass.country == "Германия"
        assert grass.germination_period == 14
        assert grass.color == "Зеленый"


class TestAdditionalCoverage:
    """Дополнительные тесты для покрытия оставшихся строк."""

    def test_product_price_property(self):
        """Тест свойства price."""
        product = Product("Товар", "Описание", 100, 5)
        assert product.price == 100
        product.price = 200
        assert product.price == 200

    def test_product_price_setter_negative(self, capsys):
        """Тест сеттера price с отрицательным значением."""
        product = Product("Товар", "Описание", 100, 5)
        product.price = -10
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100

    def test_product_price_setter_zero(self, capsys):
        """Тест сеттера price с нулевым значением."""
        product = Product("Товар", "Описание", 100, 5)
        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100

    def test_product_new_product_case_insensitive(self):
        """Тест new_product с регистронезависимым поиском."""
        from src.product import Product

        Product.all_products.clear()

        product1_data = {"name": "Товар", "description": "Описание", "price": 1000, "quantity": 5}
        product1 = Product.new_product(product1_data)

        product2_data = {"name": "товар", "description": "Новое описание", "price": 1500, "quantity": 3}
        product2 = Product.new_product(product2_data)

        assert product1 is product2
        assert product1.quantity == 8
        assert product1.price == 1500
        assert product1.description == "Новое описание"

    def test_product_new_product_empty_name(self):
        """Тест new_product с пустым именем."""
        from src.product import Product

        Product.all_products.clear()

        product_data = {"name": "", "description": "Описание", "price": 1000, "quantity": 5}
        product = Product.new_product(product_data)

        assert product.name == ""
        assert product.price == 1000
        assert product.quantity == 5
        assert len(Product.all_products) == 1

    def test_product_new_product_missing_fields(self):
        """Тест new_product с отсутствующими полями."""
        from src.product import Product

        Product.all_products.clear()

        product_data = {}

        # Проверяем, что при отсутствии quantity выбрасывается исключение
        with pytest.raises(ValueError) as exc_info:
            Product.new_product(product_data)

        assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)
        assert len(Product.all_products) == 0  # Товар не должен быть добавлен

    def test_product_abstract_methods_implemented(self):
        """Тест, что все абстрактные методы реализованы."""
        product = Product("Тест", "Описание", 100, 5)

        assert hasattr(product, "price")
        assert hasattr(product, "__str__")
        assert hasattr(product, "__add__")

        assert product.price == 100
        assert str(product) == "Тест, 100 руб. Остаток: 5 шт."
        assert product + product == 1000

    def test_order_abstract_methods_implemented(self):
        """Тест, что все абстрактные методы Order реализованы."""
        product = Product("Тест", "Описание", 100, 5)
        order = Order(product, 2)

        assert hasattr(order, "add_product")
        assert hasattr(order, "get_total_quantity")
        assert hasattr(order, "get_total_price")
        assert hasattr(order, "__str__")

        assert order.get_total_quantity() == 2
        assert order.get_total_price() == 200
        assert str(order) == "Тест - Количество: 2 шт., Стоимость: 200 руб"

        with pytest.raises(NotImplementedError):
            order.add_product(product)

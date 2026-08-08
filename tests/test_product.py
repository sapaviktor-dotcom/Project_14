import pytest
from typing import Dict, Any
from src.product import Product


class TestProduct:
    """Тесты для класса Product."""

    @pytest.fixture(autouse=True)
    def reset_all_products(self):
        """Сбрасываем глобальный список продуктов перед каждым тестом."""
        Product.all_products = []
        yield

    @pytest.fixture
    def sample_product(self) -> Product:
        """Создает тестовый продукт."""
        return Product("Laptop", "High-performance laptop", 999.99, 10)

    @pytest.fixture
    def sample_product_data(self) -> Dict[str, Any]:
        """Создает тестовые данные для продукта."""
        return {"name": "Smartphone", "description": "Latest model smartphone", "price": 799.99, "quantity": 15}

    def test_product_initialization(self, sample_product):
        """Тест инициализации продукта."""
        assert sample_product.name == "Laptop"
        assert sample_product.description == "High-performance laptop"
        assert sample_product.price == 999.99
        assert sample_product.quantity == 10
        assert sample_product in Product.all_products

    def test_product_initialization_with_int_price(self):
        """Тест инициализации с целочисленной ценой."""
        product = Product("Mouse", "Wireless mouse", 25, 20)
        assert product.price == 25
        assert isinstance(product.price, int)

    def test_product_initialization_with_float_price(self):
        """Тест инициализации с ценой с копейками."""
        product = Product("Keyboard", "Mechanical keyboard", 125.50, 5)
        assert product.price == 125.50
        assert isinstance(product.price, float)

    def test_product_added_to_all_products(self):
        """Тест что продукт добавляется в глобальный список."""
        initial_count = len(Product.all_products)

        product1 = Product("Product1", "Desc1", 100, 10)
        product2 = Product("Product2", "Desc2", 200, 20)

        assert len(Product.all_products) == initial_count + 2
        assert product1 in Product.all_products
        assert product2 in Product.all_products

    def test_price_property_getter(self, sample_product):
        """Тест геттера цены."""
        assert sample_product.price == 999.99

    def test_price_property_setter_valid(self, sample_product):
        """Тест сеттера цены с валидным значением."""
        sample_product.price = 899.99
        assert sample_product.price == 899.99

    def test_price_property_setter_invalid_zero(self, sample_product, capsys):
        """Тест сеттера цены с нулевым значением."""
        sample_product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert sample_product.price == 999.99  # Цена не изменилась

    def test_price_property_setter_invalid_negative(self, sample_product, capsys):
        """Тест сеттера цены с отрицательным значением."""
        sample_product.price = -100
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert sample_product.price == 999.99  # Цена не изменилась

    def test_new_product_creates_new_product(self, sample_product_data):
        """Тест создания нового продукта через класс-метод."""
        product = Product.new_product(sample_product_data)

        assert product.name == "Smartphone"
        assert product.description == "Latest model smartphone"
        assert product.price == 799.99
        assert product.quantity == 15
        assert len(Product.all_products) == 1

    def test_new_product_updates_existing_product(self):
        """Тест обновления существующего продукта через класс-метод."""
        # Создаем первый продукт
        Product.new_product({"name": "Phone", "description": "Old description", "price": 500, "quantity": 10})

        # Обновляем его
        updated_product = Product.new_product(
            {"name": "Phone", "description": "New description", "price": 600, "quantity": 5}
        )

        assert len(Product.all_products) == 1
        assert updated_product.quantity == 15  # 10 + 5
        assert updated_product.price == 600  # Обновилась на большую цену
        assert updated_product.description == "New description"

    def test_new_product_updates_quantity_only(self):
        """Тест обновления только количества."""
        Product.new_product({"name": "Phone", "description": "Description", "price": 500, "quantity": 10})

        updated_product = Product.new_product(
            {"name": "Phone", "description": "Description", "price": 300, "quantity": 5}  # Меньшая цена
        )

        assert updated_product.quantity == 15  # 10 + 5
        assert updated_product.price == 500  # Цена не изменилась
        assert updated_product.description == "Description"

    def test_new_product_does_not_update_price_with_lower_price(self):
        """Тест что цена не обновляется при меньшей цене."""
        Product.new_product({"name": "Phone", "description": "Description", "price": 1000, "quantity": 5})

        updated_product = Product.new_product(
            {"name": "Phone", "description": "Description", "price": 900, "quantity": 3}
        )

        assert updated_product.price == 1000  # Цена осталась прежней

    def test_new_product_handles_missing_fields(self):
        """Тест создания продукта с отсутствующими полями."""
        product_data = {"name": "Test Product"}
        product = Product.new_product(product_data)

        assert product.name == "Test Product"
        assert product.description == ""
        assert product.price == 0
        assert product.quantity == 0

    def test_new_product_case_insensitive_name_matching(self):
        """Тест поиска существующего продукта без учета регистра."""
        Product.new_product({"name": "Phone", "description": "Description", "price": 500, "quantity": 10})

        updated_product = Product.new_product(
            {"name": "PHONE", "description": "New Description", "price": 600, "quantity": 5}  # Другой регистр
        )

        assert len(Product.all_products) == 1
        assert updated_product.quantity == 15

    def test_new_product_updates_description_if_different(self):
        """Тест обновления описания если оно отличается."""
        Product.new_product({"name": "Phone", "description": "Old description", "price": 500, "quantity": 10})

        updated_product = Product.new_product(
            {"name": "Phone", "description": "New description", "price": 500, "quantity": 5}
        )

        assert updated_product.description == "New description"

    def test_new_product_does_not_update_description_if_same(self):
        """Тест что описание не обновляется если оно такое же."""
        Product.new_product({"name": "Phone", "description": "Same description", "price": 500, "quantity": 10})

        updated_product = Product.new_product(
            {"name": "Phone", "description": "Same description", "price": 500, "quantity": 5}
        )

        assert updated_product.description == "Same description"

    def test_multiple_products_in_all_products(self):
        """Тест хранения нескольких продуктов в глобальном списке."""
        products_data = [
            {"name": "Product1", "description": "Desc1", "price": 100, "quantity": 10},
            {"name": "Product2", "description": "Desc2", "price": 200, "quantity": 20},
            {"name": "Product3", "description": "Desc3", "price": 300, "quantity": 30},
        ]

        for data in products_data:
            Product.new_product(data)

        assert len(Product.all_products) == 3
        names = [p.name for p in Product.all_products]
        assert "Product1" in names
        assert "Product2" in names
        assert "Product3" in names

    def test_all_products_shared_across_instances(self):
        """Тест что глобальный список общий для всех экземпляров."""
        product1 = Product("Product1", "Desc1", 100, 10)
        product2 = Product("Product2", "Desc2", 200, 20)

        # Создаем новый экземпляр через класс-метод
        product3 = Product.new_product({"name": "Product3", "description": "Desc3", "price": 300, "quantity": 30})

        assert len(Product.all_products) == 3
        assert product1 in Product.all_products
        assert product2 in Product.all_products
        assert product3 in Product.all_products

    def test_product_attributes_types(self):
        """Тест типов атрибутов продукта."""
        product = Product("Test", "Description", 99.99, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, (int, float))
        assert isinstance(product.quantity, int)

    def test_product_str_representation(self):
        """Тест строкового представления продукта."""
        product = Product("Test", "Description", 99.99, 5)

        # Проверяем что str работает
        str_output = str(product)
        assert isinstance(str_output, str)

        # Проверяем наличие ключевой информации в выводе
        # (если __str__ реализован, иначе будет стандартный вывод)
        if hasattr(Product, "__str__") and Product.__str__ is not object.__str__:
            assert "Test" in str_output
            assert "99.99" in str_output
            assert "5" in str_output

    def test_product_repr_representation(self):
        """Тест repr представления продукта."""
        product = Product("Test", "Description", 99.99, 5)

        # Проверяем что repr работает
        repr_output = repr(product)
        assert isinstance(repr_output, str)

        # Если __repr__ переопределен, проверяем содержание
        if hasattr(Product, "__repr__") and Product.__repr__ is not object.__repr__:
            assert "Product" in repr_output
            assert "Test" in repr_output or "'Test'" in repr_output
            assert "99.99" in repr_output or "99.99" in repr_output
        else:
            # Стандартный repr
            assert "Product" in repr_output
            assert "object at" in repr_output

    def test_product_str(self):
        """Задание 1: Тест строкового представления продукта"""
        product = Product("Ноутбук", "Мощный ноутбук", 50000, 10)
        expected_str = "Ноутбук, 50000 руб. Остаток: 10 шт."
        assert str(product) == expected_str

    def test_product_str_with_float_price(self):
        """Тест строкового представления с дробной ценой"""
        product = Product("Смартфон", "Современный смартфон", 29999.99, 7)
        expected_str = "Смартфон, 29999.99 руб. Остаток: 7 шт."
        assert str(product) == expected_str

    def test_product_add(self):
        """Задание 2: Тест магического метода сложения"""
        product1 = Product("Товар A", "Описание A", 100, 10)
        product2 = Product("Товар B", "Описание B", 200, 2)

        result = product1 + product2
        expected = 100 * 10 + 200 * 2  # 1000 + 400 = 1400
        assert result == expected

    def test_product_add_with_floats(self):
        """Тест сложения с дробными ценами"""
        product1 = Product("Товар A", "Описание A", 99.99, 3)
        product2 = Product("Товар B", "Описание B", 149.50, 2)

        result = product1 + product2
        expected = 99.99 * 3 + 149.50 * 2
        assert result == expected

    def test_product_add_invalid_type(self):
        """Тест сложения с объектом не типа Product"""
        product = Product("Товар", "Описание", 100, 10)
        with pytest.raises(TypeError) as excinfo:
            result = product + "не продукт"
        assert "Нельзя сложить Product с" in str(excinfo.value)

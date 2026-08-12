from typing import Any, Dict

import pytest

import src.product


class TestProduct:
    """Тесты для класса Product."""

    @pytest.fixture(autouse=True)
    def reset_all_products(self):
        """Сбрасываем глобальный список продуктов перед каждым тестом."""
        src.product.Product.all_products = []
        yield

    @pytest.fixture
    def sample_product(self) -> src.product.Product:
        """Создает тестовый продукт."""
        return src.product.Product("Laptop", "High-performance laptop", 999.99, 10)

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
        assert sample_product in src.product.Product.all_products

    def test_product_initialization_with_int_price(self):
        """Тест инициализации с целочисленной ценой."""
        product = src.product.Product("Mouse", "Wireless mouse", 25, 20)
        assert product.price == 25
        assert isinstance(product.price, int)

    def test_product_initialization_with_float_price(self):
        """Тест инициализации с ценой с копейками."""
        product = src.product.Product("Keyboard", "Mechanical keyboard", 125.50, 5)
        assert product.price == 125.50
        assert isinstance(product.price, float)

    def test_product_added_to_all_products(self):
        """Тест что продукт добавляется в глобальный список."""
        initial_count = len(src.product.Product.all_products)

        product1 = src.product.Product("Product1", "Desc1", 100, 10)
        product2 = src.product.Product("Product2", "Desc2", 200, 20)

        assert len(src.product.Product.all_products) == initial_count + 2
        assert product1 in src.product.Product.all_products
        assert product2 in src.product.Product.all_products

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
        product = src.product.Product.new_product(sample_product_data)

        assert product.name == "Smartphone"
        assert product.description == "Latest model smartphone"
        assert product.price == 799.99
        assert product.quantity == 15
        assert len(src.product.Product.all_products) == 1

    def test_new_product_updates_existing_product(self):
        """Тест обновления существующего продукта через класс-метод."""
        src.product.Product.new_product(
            {"name": "Phone", "description": "Old description", "price": 500, "quantity": 10}
        )

        updated_product = src.product.Product.new_product(
            {"name": "Phone", "description": "New description", "price": 600, "quantity": 5}
        )

        assert len(src.product.Product.all_products) == 1
        assert updated_product.quantity == 15  # 10 + 5
        assert updated_product.price == 600  # Обновилась на большую цену
        assert updated_product.description == "New description"

    def test_new_product_updates_quantity_only(self):
        """Тест обновления только количества."""
        src.product.Product.new_product({"name": "Phone", "description": "Description", "price": 500, "quantity": 10})

        updated_product = src.product.Product.new_product(
            {"name": "Phone", "description": "Description", "price": 300, "quantity": 5}
        )

        assert updated_product.quantity == 15  # 10 + 5
        assert updated_product.price == 500  # Цена не изменилась
        assert updated_product.description == "Description"

    def test_new_product_does_not_update_price_with_lower_price(self):
        """Тест что цена не обновляется при меньшей цене."""
        src.product.Product.new_product({"name": "Phone", "description": "Description", "price": 1000, "quantity": 5})

        updated_product = src.product.Product.new_product(
            {"name": "Phone", "description": "Description", "price": 900, "quantity": 3}
        )

        assert updated_product.price == 1000  # Цена осталась прежней

    def test_new_product_handles_missing_fields(self):
        """Тест создания продукта с отсутствующими полями."""
        product_data = {"name": "Test Product", "quantity": 5}
        product = src.product.Product.new_product(product_data)

        assert product.name == "Test Product"
        assert product.description == ""
        assert product.price == 0
        assert product.quantity == 5

    def test_new_product_case_insensitive_name_matching(self):
        """Тест поиска существующего продукта без учета регистра."""
        src.product.Product.new_product({"name": "Phone", "description": "Description", "price": 500, "quantity": 10})

        updated_product = src.product.Product.new_product(
            {"name": "PHONE", "description": "New Description", "price": 600, "quantity": 5}
        )

        assert len(src.product.Product.all_products) == 1
        assert updated_product.quantity == 15

    def test_new_product_updates_description_if_different(self):
        """Тест обновления описания если оно отличается."""
        src.product.Product.new_product(
            {"name": "Phone", "description": "Old description", "price": 500, "quantity": 10}
        )

        updated_product = src.product.Product.new_product(
            {"name": "Phone", "description": "New description", "price": 500, "quantity": 5}
        )

        assert updated_product.description == "New description"

    def test_new_product_does_not_update_description_if_same(self):
        """Тест что описание не обновляется если оно такое же."""
        src.product.Product.new_product(
            {"name": "Phone", "description": "Same description", "price": 500, "quantity": 10}
        )

        updated_product = src.product.Product.new_product(
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
            src.product.Product.new_product(data)

        assert len(src.product.Product.all_products) == 3
        names = [p.name for p in src.product.Product.all_products]
        assert "Product1" in names
        assert "Product2" in names
        assert "Product3" in names

    def test_all_products_shared_across_instances(self):
        """Тест что глобальный список общий для всех экземпляров."""
        product1 = src.product.Product("Product1", "Desc1", 100, 10)
        product2 = src.product.Product("Product2", "Desc2", 200, 20)

        product3 = src.product.Product.new_product(
            {"name": "Product3", "description": "Desc3", "price": 300, "quantity": 30}
        )

        assert len(src.product.Product.all_products) == 3
        assert product1 in src.product.Product.all_products
        assert product2 in src.product.Product.all_products
        assert product3 in src.product.Product.all_products

    def test_product_attributes_types(self):
        """Тест типов атрибутов продукта."""
        product = src.product.Product("Test", "Description", 99.99, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, (int, float))
        assert isinstance(product.quantity, int)

    def test_product_str_representation(self):
        """Тест строкового представления продукта."""
        product = src.product.Product("Test", "Description", 99.99, 5)

        str_output = str(product)
        assert isinstance(str_output, str)

        # Проверяем, что в строковом представлении есть нужные данные
        assert "Test" in str_output
        assert "99.99" in str_output
        assert "5" in str_output

    def test_product_str(self):
        """Задание 1: Тест строкового представления продукта"""
        product = src.product.Product("Ноутбук", "Мощный ноутбук", 50000, 10)
        expected_str = "Ноутбук, 50000 руб. Остаток: 10 шт."
        assert str(product) == expected_str

    def test_product_str_with_float_price(self):
        """Тест строкового представления с дробной ценой"""
        product = src.product.Product("Смартфон", "Современный смартфон", 29999.99, 7)
        expected_str = "Смартфон, 29999.99 руб. Остаток: 7 шт."
        assert str(product) == expected_str

    def test_product_add(self):
        """Тест магического метода сложения"""
        product1 = src.product.Product("Товар A", "Описание A", 100, 10)
        product2 = src.product.Product("Товар B", "Описание B", 200, 2)

        result = product1 + product2
        expected = 100 * 10 + 200 * 2
        assert result == expected

    def test_product_add_with_floats(self):
        """Тест сложения с дробными ценами"""
        product1 = src.product.Product("Товар A", "Описание A", 99.99, 3)
        product2 = src.product.Product("Товар B", "Описание B", 149.50, 2)

        result = product1 + product2
        expected = 99.99 * 3 + 149.50 * 2
        assert result == expected

    def test_product_add_invalid_type(self):
        """Тест сложения с объектом не типа Product"""
        product = src.product.Product("Товар", "Описание", 100, 10)
        with pytest.raises(TypeError) as excinfo:
            product + "не продукт"
        # Проверяем соответствие сообщению из метода __add__
        assert "Нельзя складывать товары разных классов: Product и str" == str(excinfo.value)

    def test_new_product_handles_partial_fields(self):
        """Тест создания продукта с отсутствующими полями."""
        product_data = {"name": "Test Product"}
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            src.product.Product.new_product(product_data)  # Используем полное имя

    def test_product_zero_quantity(self):
        """Тест: создание товара с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            src.product.Product("Test", "Description", 100, 0)

    def test_product_positive_quantity(self):
        """Тест: создание товара с положительным количеством проходит успешно"""
        product = src.product.Product("Test", "Description", 100, 5)
        assert product.quantity == 5
        assert product.name == "Test"


class TestProductInheritance:
    """Тесты для классов-наследников Product."""

    @pytest.fixture(autouse=True)
    def reset_counts(self):
        """Сбрасываем счетчики перед каждым тестом."""
        src.product.Product.all_products = []
        yield

    def test_smartphone_creation(self):
        """ЗАДАНИЕ 1: Тест создания смартфона"""
        smartphone = src.product.Smartphone(
            "iPhone 15", "Флагманский смартфон", 999.99, 10, "High", "iPhone 15 Pro", 256, "Space Black"
        )

        assert smartphone.name == "iPhone 15"
        assert smartphone.description == "Флагманский смартфон"
        assert smartphone.price == 999.99
        assert smartphone.quantity == 10
        assert smartphone.efficiency == "High"
        assert smartphone.model == "iPhone 15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Space Black"
        assert isinstance(smartphone, src.product.Product)
        assert isinstance(smartphone, src.product.Smartphone)

    def test_lawn_grass_creation(self):
        """ЗАДАНИЕ 1: Тест создания травы газонной"""
        lawn_grass = src.product.LawnGrass(
            "Газонная трава", "Быстрорастущая газонная трава", 49.99, 100, "Россия", 14, "Зеленый"
        )

        assert lawn_grass.name == "Газонная трава"
        assert lawn_grass.description == "Быстрорастущая газонная трава"
        assert lawn_grass.price == 49.99
        assert lawn_grass.quantity == 100
        assert lawn_grass.country == "Россия"
        assert lawn_grass.germination_period == 14
        assert lawn_grass.color == "Зеленый"
        assert isinstance(lawn_grass, src.product.Product)
        assert isinstance(lawn_grass, src.product.LawnGrass)

    def test_smartphone_addition(self):
        """ЗАДАНИЕ 2: Тест сложения смартфонов (один класс)"""
        smartphone1 = src.product.Smartphone(
            "iPhone 15", "Флагманский смартфон", 999.99, 10, "High", "iPhone 15 Pro", 256, "Space Black"
        )

        smartphone2 = src.product.Smartphone(
            "Samsung S23", "Флагманский смартфон Samsung", 899.99, 15, "High", "Galaxy S23", 256, "Phantom Black"
        )

        total = smartphone1 + smartphone2
        expected = 999.99 * 10 + 899.99 * 15
        assert total == expected

    def test_lawn_grass_addition(self):
        """ЗАДАНИЕ 2: Тест сложения травы газонной (один класс)"""
        grass1 = src.product.LawnGrass("Газонная трава А", "Трава для газона", 49.99, 100, "Россия", 14, "Зеленый")

        grass2 = src.product.LawnGrass(
            "Газонная трава Б", "Трава для газона", 39.99, 200, "Германия", 21, "Темно-зеленый"
        )

        total = grass1 + grass2
        expected = 49.99 * 100 + 39.99 * 200
        assert total == expected

    def test_different_classes_addition_raises_type_error(self):
        """Тест сложения объектов разных классов - ошибка TypeError."""
        smartphone = src.product.Smartphone(
            "iPhone 15", "Флагманский смартфон", 999.99, 10, "High", "iPhone 15 Pro", 256, "Space Black"
        )

        lawn_grass = src.product.LawnGrass(
            "Газонная трава", "Быстрорастущая газонная трава", 49.99, 100, "Россия", 14, "Зеленый"
        )

        with pytest.raises(TypeError) as exc_info:
            _ = smartphone + lawn_grass

        assert "Нельзя складывать товары разных классов" in str(exc_info.value)
        assert "Smartphone" in str(exc_info.value)
        assert "LawnGrass" in str(exc_info.value)

    def test_product_with_non_product_addition_raises_type_error(self):
        """Тест сложения продукта с не-продуктом - ошибка TypeError."""
        product = src.product.Product("Ноутбук", "Мощный ноутбук", 50000, 5)

        with pytest.raises(TypeError) as exc_info:
            _ = product + 100

        assert "Нельзя складывать товары разных классов" in str(exc_info.value)

    def test_smartphone_and_product_addition_raises_type_error(self):
        """Тест сложения смартфона и обычного продукта - ошибка TypeError."""
        smartphone = src.product.Smartphone(
            "iPhone 15", "Флагманский смартфон", 999.99, 10, "High", "iPhone 15 Pro", 256, "Space Black"
        )

        product = src.product.Product("Ноутбук", "Мощный ноутбук", 50000, 5)

        with pytest.raises(TypeError) as exc_info:
            _ = smartphone + product

        assert "Нельзя складывать товары разных классов" in str(exc_info.value)
        assert "Smartphone" in str(exc_info.value)
        assert "Product" in str(exc_info.value)

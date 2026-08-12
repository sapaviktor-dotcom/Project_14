import pytest

from src.category import Category
from src.product import LawnGrass, Product, Smartphone


class TestCategory:
    """Тесты для класса Category."""

    @pytest.fixture(autouse=True)
    def reset_counts(self):
        """Сбрасываем счетчики перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0
        yield

    def test_category_initialization_with_products(self):
        """Тест на правильность инициализации Category с помощью продуктов."""
        products = [
            Product("Laptop", "High-performance laptop", 999.99, 10),
            Product("Mouse", "Wireless mouse", 25, 20),
        ]
        category = Category("Electronics", "Electronic devices", products)

        assert category.name == "Electronics"
        assert category.description == "Electronic devices"
        # Проверяем количество продуктов через приватный список
        assert len(category.get_products_list()) == 2
        # Проверяем форматированный вывод
        expected_output = "Laptop, 999.99 руб. Остаток: 10 шт.\nMouse, 25 руб. Остаток: 20 шт.\n"
        assert category.products == expected_output

    def test_category_initialization_without_products(self):
        """Тест инициализации Category с пустым списком товаров."""
        category = Category("Books", "Reading materials", [])

        assert category.name == "Books"
        assert category.description == "Reading materials"
        # Для пустой категории products возвращает пустую строку
        assert category.products == ""
        assert len(category.get_products_list()) == 0

    def test_category_count_automatically_increments(self):
        """Тест автоматического увеличения счетчика категорий."""
        initial_count = Category.category_count

        category1 = Category("Cat1", "Desc1", [])
        category2 = Category("Cat2", "Desc2", [])

        assert Category.category_count == initial_count + 2
        assert category1.category_count == Category.category_count
        assert category2.category_count == Category.category_count

    def test_product_count_automatically_increments(self):
        """Тест автоматического увеличения счетчика продуктов."""
        initial_count = Category.product_count

        products = [
            Product("Phone", "Smartphone", 50000, 2),
            Product("Charger", "Fast charger", 3000, 4),
            Product("Case", "Phone case", 1500, 10),
        ]
        category = Category("Tech", "Tech products", products)

        assert Category.product_count == initial_count + 3
        assert len(category.get_products_list()) == 3

    def test_product_count_with_empty_category(self):
        """Тест счетчика продуктов для пустой категории."""
        initial_count = Category.product_count

        category = Category("Empty", "No products", [])

        assert Category.product_count == initial_count
        assert len(category.get_products_list()) == 0

    def test_multiple_categories_combined_counts(self):
        """Тест суммарного подсчета продуктов в нескольких категориях."""
        initial_cat_count = Category.category_count
        initial_prod_count = Category.product_count

        products1 = [Product("Laptop", "Desc", 1000, 5), Product("Mouse", "Desc", 50, 10)]
        products2 = [Product("Book", "Desc", 20, 3)]
        products3 = []

        category1 = Category("Cat1", "Desc1", products1)
        category2 = Category("Cat2", "Desc2", products2)
        category3 = Category("Cat3", "Desc3", products3)

        # Доступ к приватному атрибуту через name mangling
        assert len(category1._Category__products) == 2
        assert len(category2._Category__products) == 1
        assert len(category3._Category__products) == 0

        # Проверяем глобальные счетчики
        assert Category.category_count == initial_cat_count + 3
        assert Category.product_count == initial_prod_count + 3

    def test_category_attributes_types(self):
        """Тест Category на правильные типы атрибутов."""
        product = Product("Test", "Test product", 10, 5)
        category = Category("Test Category", "Test description", [product])

        assert isinstance(category.name, str)
        assert isinstance(category.description, str)
        assert isinstance(category.products, str)  # products - это строка!
        assert isinstance(category.get_products_list(), list)

    def test_products_property_formatting_with_single_product(self):
        """Тест форматирования для одного продукта."""
        product = Product("Test", "Test product", 10.99, 5)
        category = Category("Test Category", "Desc", [product])

        expected = "Test, 10.99 руб. Остаток: 5 шт.\n"
        assert category.products == expected

    def test_products_property_formatting_with_multiple_products(self):
        """Тест форматирования для нескольких продуктов."""
        products = [
            Product("Product A", "Desc A", 100, 2),
            Product("Product B", "Desc B", 200, 3),
        ]
        category = Category("Category", "Desc", products)

        expected = "Product A, 100 руб. Остаток: 2 шт.\nProduct B, 200 руб. Остаток: 3 шт.\n"
        assert category.products == expected

    def test_add_product_updates_counts(self):
        """Тест обновления счетчиков при добавлении продукта."""
        category = Category("Category", "Desc", [])
        initial_product_count = Category.product_count

        product = Product("New Product", "Desc", 100, 1)
        category.add_product(product)

        assert len(category.get_products_list()) == 1
        assert Category.product_count == initial_product_count + 1

        # Проверяем, что products свойство обновилось
        assert "New Product, 100 руб. Остаток: 1 шт." in category.products

    def test_get_products_list_returns_actual_list(self):
        """Тест что get_products_list возвращает список."""
        product = Product("Test", "Desc", 100, 1)
        category = Category("Category", "Desc", [product])

        products_list = category.get_products_list()

        assert isinstance(products_list, list)
        assert len(products_list) == 1
        assert products_list[0] == product

    def test_products_property_returns_string(self):
        """Тест что свойство products всегда возвращает строку."""
        # С продуктами
        category1 = Category("Cat1", "Desc", [Product("Test", "Desc", 100, 1)])
        assert isinstance(category1.products, str)

        # Без продуктов
        category2 = Category("Cat2", "Desc", [])
        assert isinstance(category2.products, str)
        assert category2.products == ""

    def test_category_add_invalid_product(self, capsys):
        """
        Тест добавления невалидного объекта в категорию.
        Используется isinstance() для проверки.
        """
        category = Category("Смартфоны", "Категория смартфонов", [])

        # Вызываем метод, который должен вывести ошибку в консоль
        category.add_product("not a product")

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "Ошибка типа: Можно добавлять только объекты класса Product или его наследников" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_category_add_none_product(self, capsys):
        """Тест добавления None в категорию."""
        category = Category("Тест", "Тестовая категория", [])

        # Вызываем метод, который должен вывести ошибку в консоль
        category.add_product(None)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "Ошибка типа: Можно добавлять только объекты класса Product или его наследников" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_category_str(self):
        """Тест строкового представления категории"""
        product1 = Product("Товар1", "Описание1", 100, 5)
        product2 = Product("Товар2", "Описание2", 200, 3)
        category = Category("Электроника", "Электронные товары", [product1, product2])

        expected_str = "Электроника, количество продуктов: 8 шт."
        assert str(category) == expected_str

    def test_category_str_empty(self):
        """Тест строкового представления пустой категории"""
        category = Category("Пустая", "Пустая категория", [])
        expected_str = "Пустая, количество продуктов: 0 шт."
        assert str(category) == expected_str

    def test_category_str_with_multiple_quantities(self):
        """Тест строкового представления с разными количествами товаров"""
        product1 = Product("Товар1", "Описание1", 100, 10)
        product2 = Product("Товар2", "Описание2", 200, 1)
        product3 = Product("Товар3", "Описание3", 300, 7)
        category = Category("Тестовая", "Тестовая категория", [product1, product2, product3])

        expected_str = "Тестовая, количество продуктов: 18 шт."  # 10 + 0 + 7
        assert str(category) == expected_str

    def test_category_get_total_quantity(self):
        """Тест метода получения общего количества товаров"""
        product1 = Product("Товар1", "Описание1", 100, 5)
        product2 = Product("Товар2", "Описание2", 200, 3)
        category = Category("Электроника", "Электронные товары", [product1, product2])

        assert category.get_total_quantity() == 8

    def test_category_get_total_price(self):
        """Тест метода получения общей стоимости всех товаров"""
        product1 = Product("Товар1", "Описание1", 100, 5)  # 100 * 5 = 500
        product2 = Product("Товар2", "Описание2", 200, 3)  # 200 * 3 = 600
        category = Category("Электроника", "Электронные товары", [product1, product2])

        assert category.get_total_price() == 1100


class TestCategoryProductAddition:
    """Тесты для добавления продуктов в категорию."""

    @pytest.fixture(autouse=True)
    def reset_counts(self):
        """Сбрасываем счетчики перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0
        yield

    def test_category_add_product(self):
        """Тест добавления продукта в категорию"""
        category = Category("Смартфоны", "Категория смартфонов", [])

        smartphone = Smartphone(
            "iPhone 15", "Флагманский смартфон", 999.99, 10, "High", "iPhone 15 Pro", 256, "Space Black"
        )

        category.add_product(smartphone)
        assert len(category.get_products_list()) == 1
        assert category.get_products_list()[0] is smartphone

    def test_category_add_different_products(self):
        """Тест добавления разных типов продуктов в категорию"""
        category = Category("Товары", "Разные товары", [])

        smartphone = Smartphone(
            "iPhone 15", "Флагманский смартфон", 999.99, 10, "High", "iPhone 15 Pro", 256, "Space Black"
        )

        lawn_grass = LawnGrass("Газонная трава", "Быстрорастущая газонная трава", 49.99, 100, "Россия", 14, "Зеленый")

        product = Product("Ноутбук", "Мощный ноутбук", 50000, 5)

        category.add_product(smartphone)
        category.add_product(lawn_grass)
        category.add_product(product)

        assert len(category.get_products_list()) == 3

    def test_category_add_product_updates_count(self):
        """Тест обновления счетчика при добавлении продукта"""
        category = Category("Тест", "Тестовая категория", [])
        initial_count = Category.product_count

        product = Product("Тестовый", "Тестовый продукт", 100, 5)
        category.add_product(product)

        assert Category.product_count == initial_count + 1
        assert len(category.get_products_list()) == 1

    def test_category_average_price(self):
        """Тест: подсчет среднего ценника товаров в категории"""
        product1 = Product("Товар 1", "Описание 1", 100, 2)
        product2 = Product("Товар 2", "Описание 2", 200, 3)

        category = Category("Тестовая категория", "Описание", [product1, product2])

        # Средняя цена: (100 + 200) / 2 = 150
        assert category.get_average_price() == 150

    def test_category_average_price_empty(self):
        """Тест: подсчет среднего ценника в пустой категории"""
        category = Category("Пустая категория", "Описание", [])

        # В пустой категории должно возвращаться 0
        assert category.get_average_price() == 0

    def test_category_with_different_products(self):
        """Тест: категория с разными типами продуктов (Smartphone и LawnGrass)"""
        smartphone = Smartphone("iPhone 13", "Смартфон Apple", 999.99, 10, "A15 Bionic", "iPhone 13", 128, "черный")

        grass = LawnGrass("Газонная трава", "Смесь трав для газона", 50.0, 100, "Россия", 7, "зеленый")

        category = Category("Разные товары", "Описание", [smartphone, grass])

        # Средняя цена: (999.99 + 50.0) / 2 = 524.995
        assert category.get_average_price() == 524.995

    def test_category_average_price_one_product(self):
        """Тест: категория с одним товаром"""
        product = Product("Один товар", "Описание", 150, 1)
        category = Category("Категория с одним товаром", "Описание", [product])

        assert category.get_average_price() == 150

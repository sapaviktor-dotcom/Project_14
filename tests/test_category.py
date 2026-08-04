import pytest
from src.category import Category
from src.product import Product


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

        assert Category.category_count == initial_cat_count + 3
        assert Category.product_count == initial_prod_count + 3  # 2 + 1 + 0

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


class TestCategoryEdgeCases:
    """Тесты граничных случаев."""

    @pytest.fixture(autouse=True)
    def reset_counts(self):
        Category.category_count = 0
        Category.product_count = 0
        yield

    def test_category_with_very_long_names(self):
        """Тест с очень длинными названиями."""
        long_name = "A" * 1000
        long_desc = "B" * 2000

        product = Product("Test", "Desc", 100, 1)
        category = Category(long_name, long_desc, [product])

        assert category.name == long_name
        assert category.description == long_desc
        assert len(category.products) > 0

    def test_large_number_of_products(self):
        """Тест с большим количеством продуктов."""
        products = [Product(f"Product{i}", f"Desc{i}", i * 100, i) for i in range(100)]

        category = Category("Large", "Large category", products)

        assert category.product_count == 100
        assert len(category.get_products_list()) == 100

        # Проверяем форматирование
        products_output = category.products
        assert "Product0" in products_output
        assert "Product99" in products_output

    def test_add_product_after_initialization(self):
        """Тест добавления продукта после создания категории."""
        category = Category("Category", "Desc", [])
        initial_count = Category.product_count

        # Добавляем несколько продуктов
        products_to_add = [
            Product("P1", "D1", 10, 1),
            Product("P2", "D2", 20, 2),
            Product("P3", "D3", 30, 3),
        ]

        for product in products_to_add:
            category.add_product(product)

        assert len(category.get_products_list()) == 3
        assert Category.product_count == initial_count + 3

        # Проверяем порядок добавления
        products_list = category.get_products_list()
        assert products_list[0].name == "P1"
        assert products_list[1].name == "P2"
        assert products_list[2].name == "P3"

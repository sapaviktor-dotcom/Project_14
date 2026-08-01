from src.category import Category
from src.product import Product


class TestCategory:
    """Набор тестов для class Category."""

    def setup_method(self):
        """Reset  атрибутов класса перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization_with_products(self):
        """Тест на правильность инициализации Category с помощью продуктов."""
        products = [
            Product("Laptop", "High-performance laptop", 999.99, 10),
            Product("Mouse", "Wireless mouse", 25, 20),
        ]
        category = Category("Electronics", "Electronic devices", products)

        assert category.name == "Electronics"
        assert category.description == "Electronic devices"
        assert len(category.products) == 2
        assert isinstance(category.products, list)
        assert isinstance(category.products[0], Product)
        assert category.products[0].name == "Laptop"
        assert category.products[1].name == "Mouse"

    def test_category_initialization_without_products(self):
        """Тест инициализации Category с пустым списком товаров."""
        category = Category("Books", "Reading materials", [])

        assert category.name == "Books"
        assert category.description == "Reading materials"
        assert len(category.products) == 0
        assert isinstance(category.products, list)

    def test_category_count_automatically_increments(self):
        """Тест  что category_count увеличивается автоматически."""
        assert Category.category_count == 0

        Category("Electronics", "Devices", [])
        assert Category.category_count == 1

        Category("Books", "Reading", [])
        assert Category.category_count == 2

        Category("Clothing", "Apparel", [])
        assert Category.category_count == 3

    def test_product_count_automatically_increments(self):
        """Тест, что product_count увеличивается автоматически."""
        assert Category.product_count == 0

        products1 = [Product("Laptop", "Laptop", 999.99, 10), Product("Mouse", "Mouse", 25, 20)]
        Category("Electronics", "Devices", products1)
        assert Category.product_count == 2

        products2 = [Product("Book", "Novel", 15.99, 50), Product("Pen", "Pen", 0.99, 100)]
        Category("Stationery", "Office supplies", products2)
        assert Category.product_count == 4

    def test_product_count_with_empty_category(self):
        """Тест product_count при создании пустой категории."""
        Category("Empty", "Empty category", [])
        assert Category.product_count == 0

    def test_multiple_categories_combined_counts(self):
        """Тест на комбинированный подсчет categories и products."""
        products_electronics = [
            Product("Phone", "Smartphone", 599.99, 5),
            Product("Tablet", "Android tablet", 299.99, 3),
        ]
        products_books = [Product("Python Book", "Programming", 49.99, 15)]
        products_clothing = [
            Product("Shirt", "Cotton shirt", 29.99, 20),
            Product("Jeans", "Blue jeans", 59.99, 10),
            Product("Jacket", "Winter jacket", 89.99, 5),
        ]

        Category("Electronics", "Devices", products_electronics)
        Category("Books", "Reading", products_books)
        Category("Clothing", "Apparel", products_clothing)

        assert Category.category_count == 3
        assert Category.product_count == 6  # 2 + 1 + 3

    def test_category_attributes_types(self):
        """Тест Category на правильные типыматрибутов."""
        products = [Product("Test", "Test product", 10, 5)]
        category = Category("Test Category", "Test description", products)

        assert isinstance(category.name, str)
        assert isinstance(category.description, str)
        assert isinstance(category.products, list)
        assert isinstance(Category.category_count, int)
        assert isinstance(Category.product_count, int)

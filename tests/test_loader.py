import pytest
import json
from src.loader import load_data_from_json
from src.category import Category
from src.product import Product


class TestLoader:
    """Тесты для функции загрузки данных из JSON."""

    @pytest.fixture(autouse=True)
    def reset_counts(self):
        """Сбрасываем счетчики перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0
        Product.all_products = []
        yield

    def test_load_data_from_json(self, tmp_path):
        """Тест загрузки данных из JSON файла."""
        # Создаем тестовые JSON данные
        test_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices",
                "products": [
                    {"name": "Laptop", "description": "High-performance laptop", "price": 999.99, "quantity": 10},
                    {"name": "Mouse", "description": "Wireless mouse", "price": 25, "quantity": 20},
                ],
            },
            {
                "name": "Books",
                "description": "Reading materials",
                "products": [
                    {"name": "Python Book", "description": "Programming book", "price": 49.99, "quantity": 15}
                ],
            },
        ]

        # Записываем тестовые данные во временный файл
        test_file = tmp_path / "test_products.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        # Загружаем данные
        categories = load_data_from_json(str(test_file))

        # Проверки
        assert len(categories) == 2
        assert isinstance(categories[0], Category)
        assert categories[0].name == "Electronics"
        # Используем get_products_list() для получения списка продуктов
        assert len(categories[0].get_products_list()) == 2
        assert categories[0].description == "Electronic devices"

        # Проверяем продукты в первой категории
        products_list = categories[0].get_products_list()
        assert products_list[0].name == "Laptop"
        assert products_list[0].price == 999.99
        assert products_list[0].quantity == 10
        assert products_list[1].name == "Mouse"
        assert products_list[1].price == 25
        assert products_list[1].quantity == 20

        # Проверяем вторую категорию
        assert categories[1].name == "Books"
        assert len(categories[1].get_products_list()) == 1
        assert categories[1].get_products_list()[0].name == "Python Book"

        # Проверяем счетчики
        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_load_data_from_json_empty_file(self, tmp_path):
        """Тест загрузки из пустого JSON файла."""
        # Создаем пустой файл
        test_file = tmp_path / "empty.json"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("[]")

        # Загружаем данные
        categories = load_data_from_json(str(test_file))

        # Проверки
        assert isinstance(categories, list)
        assert len(categories) == 0
        assert Category.category_count == 0
        assert Category.product_count == 0

    def test_load_data_from_json_with_single_product(self, tmp_path):
        """Тест загрузки данных с одной категорией и одним продуктом."""
        test_data = [
            {
                "name": "Test Category",
                "description": "Test Description",
                "products": [
                    {"name": "Test Product", "description": "Test Product Desc", "price": 100, "quantity": 5}
                ],
            }
        ]

        test_file = tmp_path / "single.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        categories = load_data_from_json(str(test_file))

        assert len(categories) == 1
        assert categories[0].name == "Test Category"
        assert len(categories[0].get_products_list()) == 1
        assert categories[0].get_products_list()[0].name == "Test Product"
        assert Category.category_count == 1
        assert Category.product_count == 1

    def test_load_data_from_json_with_multiple_products(self, tmp_path):
        """Тест загрузки данных с одной категорией и несколькими продуктами."""
        test_data = [
            {
                "name": "Category",
                "description": "Description",
                "products": [
                    {"name": "Product1", "description": "Desc1", "price": 100, "quantity": 10},
                    {"name": "Product2", "description": "Desc2", "price": 200, "quantity": 20},
                    {"name": "Product3", "description": "Desc3", "price": 300, "quantity": 30},
                ],
            }
        ]

        test_file = tmp_path / "multiple.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        categories = load_data_from_json(str(test_file))

        assert len(categories) == 1
        assert len(categories[0].get_products_list()) == 3
        assert Category.product_count == 3

        # Проверяем свойства products (строка)
        products_output = categories[0].products
        assert "Product1" in products_output
        assert "Product2" in products_output
        assert "Product3" in products_output

    def test_load_data_from_json_with_category_no_products(self, tmp_path):
        """Тест загрузки категории без продуктов."""
        test_data = [{"name": "Empty Category", "description": "No products", "products": []}]

        test_file = tmp_path / "empty_category.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        categories = load_data_from_json(str(test_file))

        assert len(categories) == 1
        assert categories[0].name == "Empty Category"
        assert len(categories[0].get_products_list()) == 0
        assert categories[0].products == ""  # Пустая строка
        assert Category.product_count == 0

    def test_load_data_from_json_preserves_data_types(self, tmp_path):
        """Тест сохранения типов данных при загрузке."""
        test_data = [
            {
                "name": "Category",
                "description": "Description",
                "products": [{"name": "Product", "description": "Desc", "price": 99.99, "quantity": 5}],
            }
        ]

        test_file = tmp_path / "types.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        categories = load_data_from_json(str(test_file))
        product = categories[0].get_products_list()[0]

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, (int, float))
        assert isinstance(product.quantity, int)

    def test_load_data_from_json_with_unicode(self, tmp_path):
        """Тест загрузки с Unicode символами."""
        test_data = [
            {
                "name": "Тестовая категория",
                "description": "Описание с русскими буквами",
                "products": [{"name": "Продукт", "description": "Описание продукта", "price": 100, "quantity": 5}],
            }
        ]

        test_file = tmp_path / "unicode.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        categories = load_data_from_json(str(test_file))

        assert categories[0].name == "Тестовая категория"
        assert categories[0].description == "Описание с русскими буквами"
        assert categories[0].get_products_list()[0].name == "Продукт"

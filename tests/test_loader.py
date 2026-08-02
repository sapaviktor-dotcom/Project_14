import json
import pytest
from src.loader import load_data_from_json
from src.category import Category
from src.product import Product


class TestLoader:
    """Test suite for JSON loader."""







    def test_load_data_from_json(self, tmp_path):
        """Test loading data from JSON file."""
        # Create test JSON data
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

        # Write test data to temporary file
        test_file = tmp_path / "test_products.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        Category.category_count = 0
        Category.product_count = 0

        # Load data
        categories = load_data_from_json(str(test_file))

        # Assertions
        assert len(categories) == 2
        assert isinstance(categories[0], Category)
        assert categories[0].name == "Electronics"
        assert len(categories[0].products) == 2
        assert isinstance(categories[0].products[0], Product)
        assert categories[0].products[0].name == "Laptop"
        assert categories[0].products[0].price == 999.99

        assert categories[1].name == "Books"
        assert len(categories[1].products) == 1
        assert categories[1].products[0].name == "Python Book"

        # Check that class attributes were updated
        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_load_data_from_json_empty_file(self, tmp_path):
        """Test loading from empty JSON file."""
        test_file = tmp_path / "empty.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump([], f)

        categories = load_data_from_json(str(test_file))
        assert len(categories) == 0

    def test_load_data_from_json_file_not_found(self):
        """Test loading from non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_data_from_json("non_existent_file.json")

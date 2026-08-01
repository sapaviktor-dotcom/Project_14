from src.product import Product


class TestProduct:
    """Test suite for Product class."""

    def test_product_initialization_with_all_attributes(self):
        """Test that Product initializes correctly with all attributes."""
        product = Product("Laptop", "High-performance gaming laptop", 999.99, 10)

        assert product.name == "Laptop"
        assert product.description == "High-performance gaming laptop"
        assert product.price == 999.99
        assert product.quantity == 10

    def test_product_with_integer_price(self):
        """Test Product initialization with integer price."""
        product = Product("Mouse", "Wireless mouse", 25, 20)

        assert isinstance(product.price, int)
        assert product.price == 25

    def test_product_with_float_price(self):
        """Test Product initialization with float price (with kopecks)."""
        product = Product("Phone", "Smartphone", 599.99, 5)

        assert isinstance(product.price, float)
        assert product.price == 599.99

    def test_product_with_zero_quantity(self):
        """Test Product initialization with zero quantity."""
        product = Product("Book", "Python programming book", 49.99, 0)

        assert product.name == "Book"
        assert product.quantity == 0

    def test_product_with_large_quantity(self):
        """Test Product initialization with large quantity."""
        product = Product("Pen", "Blue ballpoint pen", 0.99, 1000)

        assert product.quantity == 1000

    def test_product_attributes_types(self):
        """Test that Product attributes have correct types."""
        product = Product("Tablet", "Android tablet", 299.99, 15)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, (int, float))
        assert isinstance(product.quantity, int)

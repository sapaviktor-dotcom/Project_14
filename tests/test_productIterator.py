import pytest
from src.product import Product
from src.category import Category
from src.productIterator import ProductIterator


class TestProductIterator:
    """Тесты для дополнительного задания - итератор"""

    def setup_method(self):
        """Очищаем глобальные счетчики перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_product_iterator(self):
        """Тест итератора для перебора товаров в категории"""
        product1 = Product("Товар1", "Описание1", 100, 5)
        product2 = Product("Товар2", "Описание2", 200, 3)
        product3 = Product("Товар3", "Описание3", 300, 2)

        category = Category("Тестовая", "Тестовая категория", [product1, product2, product3])

        iterator = ProductIterator(category)

        # Проверяем, что итератор возвращает правильные товары
        products_from_iter = list(iterator)
        assert len(products_from_iter) == 3
        assert products_from_iter[0].name == "Товар1"
        assert products_from_iter[1].name == "Товар2"
        assert products_from_iter[2].name == "Товар3"

    def test_product_iterator_for_loop(self):
        """Тест использования итератора в цикле for"""
        product1 = Product("Товар1", "Описание1", 100, 5)
        product2 = Product("Товар2", "Описание2", 200, 3)

        category = Category("Тестовая", "Тестовая категория", [product1, product2])

        # Проверяем работу в цикле for
        names = []
        for product in ProductIterator(category):
            names.append(product.name)

        assert names == ["Товар1", "Товар2"]

    def test_product_iterator_empty(self):
        """Тест итератора для пустой категории"""
        category = Category("Пустая", "Пустая категория", [])
        iterator = ProductIterator(category)

        with pytest.raises(StopIteration):
            next(iterator)

    def test_product_iterator_multiple_iterations(self):
        """Тест множественных итераций"""
        product1 = Product("Товар1", "Описание1", 100, 5)
        product2 = Product("Товар2", "Описание2", 200, 3)

        category = Category("Тестовая", "Тестовая категория", [product1, product2])
        iterator = ProductIterator(category)

        # Первая итерация
        items1 = list(iterator)
        assert len(items1) == 2

        # Создаем новый итератор для второй итерации
        iterator2 = ProductIterator(category)
        items2 = list(iterator2)
        assert len(items2) == 2
        assert items1[0].name == items2[0].name

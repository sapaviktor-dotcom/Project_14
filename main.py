from src.product import Product
from src.category import Category
from src.productIterator import ProductIterator
from src.loader import load_data_from_json

if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)


    def simple_demo():
        """Простая демонстрация базовой функциональности"""

        print("\n🏪 БАЗОВАЯ ПРОВЕРКА РАБОТЫ\n")

        # 1. Создание продуктов
        print("1. Создание продуктов:")
        p1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        p2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        p3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

        print(f"   ✓ Создано продуктов: {len(Product.all_products)}")

        # 2. Строковое представление
        print("\n2. Строковое представление:")
        print(f"   {p1}")
        print(f"   {p2}")
        print(f"   {p3}")

        # 3. Сложение продуктов
        print("\n3. Сложение продуктов:")
        result = p1 + p2
        print(f"   {p1.name} + {p2.name} = {result} руб.")
        print(f"   ({p1.price}*{p1.quantity} + {p2.price}*{p2.quantity})")

        # 4. Создание категории
        print("\n4. Создание категории:")
        category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
         [p1, p2, p3])
        print(f"   Категория: {category.name}")
        print(f"   {category}")

        # 5. Добавление товара
        print("\n5. Добавление товара в категорию:")
        p4 = Product("Монитор", "4K монитор", 45000, 7)
        category.add_product(p4)
        print(f"   Добавлен: {p4.name}")
        print(f"   Всего товаров в категории: {len(category.get_products_list())}")

        # 6. Итератор
        print("\n6. Перебор товаров через итератор:")
        for i, product in enumerate(ProductIterator(category), 1):
            print(f"   {i}. {product.name} - {product.price} руб. (x{product.quantity})")

        # 7. Обновление продукта
        print("\n7. Обновление продукта через new_product:")
        update_data = {
            "name": "Ноутбук",
            "description": "Обновленный ноутбук",
            "price": 82000,
            "quantity": 5
        }
        updated = Product.new_product(update_data)
        print(f"   Обновленный {updated.name}:")
        print(f"   Цена: {updated.price} руб. (было 75000)")
        print(f"   Количество: {updated.quantity} шт. (было 10 + 5)")

        # 8. Итоговая статистика
        print("\n8. Статистика:")
        print(f"   Всего категорий: {Category.category_count}")
        print(f"   Всего товаров: {Category.product_count}")
        total_value = sum(p.price * p.quantity for p in Product.all_products)
        print(f"   Общая стоимость: {total_value:,.2f} руб.")


    if __name__ == "__main__":
        simple_demo()

    if __name__ == '__main__':
        product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

        print(product1.name)
        print(product1.description)
        print(product1.price)
        print(product1.quantity)

        print(product2.name)
        print(product2.description)
        print(product2.price)
        print(product2.quantity)

        print(product3.name)
        print(product3.description)
        print(product3.price)
        print(product3.quantity)

        category1 = Category("Смартфоны",
                             "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                             [product1, product2, product3])

        print(category1.name == "Смартфоны")
        print(category1.description)
        print(len(category1.products))
        print(category1.category_count)
        print(category1.product_count)

        product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
        category2 = Category("Телевизоры",
                             "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                             [product4])

        print(category2.name)
        print(category2.description)
        print(len(category2.products))
        print(category2.products)

        print(Category.category_count)
        print(Category.product_count)
from sqlalchemy import delete

from app.database import SessionLocal
from app.models import Category, Client, Order, OrderItem, Product


def seed_database():
    db = SessionLocal()
    try:
        db.execute(delete(OrderItem))
        db.execute(delete(Order))
        db.execute(delete(Product))
        db.execute(delete(Category))
        db.execute(delete(Client))

        # Категории
        cat_data = [
            Category(name="Электроника", parent_id=None),
            Category(name="Компьютеры", parent_id=1),
            Category(name="Ноутбуки", parent_id=2),
            Category(name="Смартфоны", parent_id=1),
            Category(name="Одежда", parent_id=None),
            Category(name="Мужская", parent_id=5),
            Category(name="Женская", parent_id=5),
        ]
        for cat in cat_data:
            db.add(cat)
        db.flush()

        # Товары
        prod_data = [
            Product(name="Ноутбук ASUS", quantity=10, price=50000.00, category_id=3),
            Product(name="Ноутбук HP", quantity=5, price=45000.00, category_id=3),
            Product(name="iPhone 15", quantity=20, price=80000.00, category_id=4),
            Product(name="Футболка", quantity=50, price=1500.00, category_id=6),
            Product(name="Платье", quantity=30, price=3000.00, category_id=7),
        ]
        for prod in prod_data:
            db.add(prod)

        # Клиенты
        client_data = [
            Client(name="Иванов Иван", address="Москва, ул. Пушкина, 1"),
            Client(name="Петров Петр", address="СПб, Невский пр., 10"),
        ]
        for client in client_data:
            db.add(client)

        db.commit()

        # Заказы
        order_data = [
            Order(client_id=1),
            Order(client_id=2),
        ]
        for order in order_data:
            db.add(order)

        db.commit()

        # Позиции заказов
        order_item_data = [
            OrderItem(order_id=1, product_id=1, quantity=1),
            OrderItem(order_id=1, product_id=3, quantity=2),
            OrderItem(order_id=2, product_id=4, quantity=3),
            OrderItem(order_id=2, product_id=5, quantity=1),
        ]
        for item in order_item_data:
            db.add(item)

        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

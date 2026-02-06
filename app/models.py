from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive"),
        CheckConstraint("price >= 0", name="check_price_positive"),
    )


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(512))


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(
        Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(TIMESTAMP, server_default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
        CheckConstraint("quantity > 0", name="check_order_quantity_positive"),
    )

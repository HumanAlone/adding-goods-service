from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category, Client, Order, OrderItem, Product
from app.schemas import OrderItemAdd, OrderItemResponse

router = APIRouter()


@router.get("/")
def health_check():
    return {
        "service": "Order Item Service",
        "version": "1.0.0",
        "health": "OK",
        "docs": "/docs",
        "endpoint": "POST /orders/{order_id}/items",
    }


@router.get("/all-data")
def get_all_data(db: Session = Depends(get_db)):
    """Возвращает все данные из всех таблиц БД"""

    categories = db.query(Category).all()
    products = db.query(Product).all()
    clients = db.query(Client).all()
    orders = db.query(Order).all()
    order_items = db.query(OrderItem).all()

    return {
        "categories": [
            {"id": c.id, "name": c.name, "parent_id": c.parent_id} for c in categories
        ],
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "quantity": p.quantity,
                "price": float(p.price),
                "category_id": p.category_id,
            }
            for p in products
        ],
        "clients": [
            {"id": cl.id, "name": cl.name, "address": cl.address} for cl in clients
        ],
        "orders": [
            {"id": o.id, "client_id": o.client_id, "created_at": o.created_at}
            for o in orders
        ],
        "order_items": [
            {
                "id": oi.id,
                "order_id": oi.order_id,
                "product_id": oi.product_id,
                "quantity": oi.quantity,
            }
            for oi in order_items
        ],
    }


@router.post(
    "/orders/{order_id}/items",
    response_model=OrderItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Добавить товар в заказ",
    description="""
    Добавляет товар в существующий заказ.
    
    - Если товар уже есть в заказе - увеличивает его количество.
    - Если товара нет в наличии - возвращает ошибку 400.
    - Если заказа или товара не существует - 404.
    """,
)
def add_item_to_order(order_id: int, item: OrderItemAdd, db: Session = Depends(get_db)):
    # Проверка существования заказа
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден",
        )

    # Проверка товара и наличия
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Товар с ID {item.product_id} не найден",
        )

    if product.quantity < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недостаточно товара на складе. Доступно: {product.quantity}, запрошено: {item.quantity}",
        )

    # Проверка товара в заказе
    order_item = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order_id, OrderItem.product_id == item.product_id)
        .first()
    )

    if order_item:
        order_item.quantity += item.quantity
    else:
        order_item = OrderItem(
            order_id=order_id, product_id=item.product_id, quantity=item.quantity
        )
        db.add(order_item)

    product.quantity -= item.quantity

    try:
        db.commit()
        db.refresh(order_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при добавлении товара в заказ",
        )

    return order_item

from pydantic import BaseModel, Field


class OrderItemAdd(BaseModel):
    product_id: int = Field(gt=0, description="ID товара")
    quantity: int = Field(gt=0, description="Количество, должно быть > 0")


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

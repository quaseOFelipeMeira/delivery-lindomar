from sqlalchemy import Column, Integer, String, Double, ForeignKey
from core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Double)


class OrderItem(Base):
    __tablename__ = "orderItem"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(ForeignKey("products.id"))
    order_id = Column(Integer) # n sei se é melhor deixar como integer para criar os itens, dps a compra final, ou deixar como foreign key da outra tabela


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"))
    order_item_id = Column(ForeignKey("orderItem.id"))
    total_price = Column(Double)

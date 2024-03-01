from sqlalchemy import Column, Integer, String, Double, ForeignKey
from core.database import Base


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Double)


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(ForeignKey("account.id"))
    complement = Column(String)
    street = Column(String)
    house_number = Column(String)
    neighborhood = Column(String)
    city = Column(String)
    state = Column(String(2))
    CEP = Column(String)


class OrderItem(Base):
    __tablename__ = "orderItem"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(ForeignKey("product.id"))
    order_id = Column(
        Integer
    )  # n sei se é melhor deixar como integer para criar os itens, dps a compra final, ou deixar como foreign key da outra tabela


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(ForeignKey("account.id"))
    order_item_id = Column(ForeignKey("orderItem.id"))
    total_price = Column(Double)

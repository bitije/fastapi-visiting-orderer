from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func 
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=False)
    phone = Column(String(255), nullable=False, unique=True)
    store_id = Column(Integer, ForeignKey("stores.id"))

    stores = relationship("Store")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True, unique=False)
    phone = Column(String(255), nullable=False, unique=True)
    store_id = Column(Integer, ForeignKey('stores.id'))

    store = relationship("Store")

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
        
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    creation_date = Column(DateTime, default=func.now())
    deadline = Column(DateTime)
    store_id = Column(Integer, ForeignKey("stores.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    status = Column(String)

    store = relationship("Store")
    customer = relationship("Customer")
    employee = relationship("Employee")

class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, default=func.now())
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True, nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    
    store = relationship("Store")
    customer = relationship("Customer")
    employee = relationship("Employee")
    order = relationship("Order", uselist=False)

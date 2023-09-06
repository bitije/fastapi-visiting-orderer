from pydantic import BaseModel
from datetime import datetime


class StoreSchema(BaseModel):
    id: int
    title: str

class BasePersonSchema(BaseModel):
    id: int
    name: str
    phone: str
    store_id: int 

class CustomerSchema(BasePersonSchema):
    pass

class EmployeeSchema(BasePersonSchema):
    pass

class OrderSchema(BaseModel):
    id: int
    creation_date: datetime
    deadline: datetime
    status: str
    store: StoreSchema 
    customer: CustomerSchema 
    employee: EmployeeSchema
   
    class Config:
        orm_mode = True

class CreateOrderSchema(OrderSchema):
    store: int
    customer: int
    employee: int

class VisitSchema(BaseModel):
    id: int
    creation_date: datetime
    employee: EmployeeSchema 
    order: OrderSchema
    customer: CustomerSchema 
    store: StoreSchema

class CreateVisitSchema(VisitSchema):
    pass



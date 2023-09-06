from fastapi import Depends, FastAPI, HTTPException, Path
from schemas import CreateVisitSchema, StoreSchema, OrderSchema, CreateOrderSchema, VisitSchema
import services
import models
from sqlalchemy.orm import Session
from typing  import List

app = FastAPI()

def order_validate(store, customer, employee):
    if (store or customer or employee) is None:
        raise HTTPException(status_code=500, detail="Wrong data!")

    if customer.store_id != store.id:
        raise HTTPException(status_code=500, detail="Customer and store are not related.")

    if employee.store_id != store.id:
        raise HTTPException(status_code=500, detail="Employee and store are not related.")
    
@app.get("/api/stores/", response_model=List[StoreSchema])
async def get_all_stores(db: Session = Depends(services.get_db)):
    return db.query(models.Store).all()

@app.get("/api/orders/{order_id}/", response_model=OrderSchema)
async def get_order_by_id(order_id: int = Path(), db: Session = Depends(services.get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/orders/", response_model=OrderSchema)
async def create_order(order: CreateOrderSchema, db: Session = Depends(services.get_db)):
        
    store = db.query(models.Store).filter(models.Store.id == order.store).first()
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer).first()
    employee = db.query(models.Employee).filter(models.Employee.id == order.employee).first()

    order_validate(store, customer, employee)

    order_obj = models.Order(
        creation_date=order.creation_date,
        deadline=order.deadline,
        store=store,
        customer=customer,
        employee=employee,
        status=order.status
     )
    db.add(order_obj)
    db.commit()
    db.refresh(order_obj)
    return order_obj

@app.put("/api/orders/{order_id}")
async def update_order(order_id: int, updated_order: CreateOrderSchema, db:Session = Depends(services.get_db)):
    existing_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    store = db.query(models.Store).filter(models.Store.id == updated_order.store).first()
    customer = db.query(models.Customer).filter(models.Customer.id == updated_order.customer).first()
    employee = db.query(models.Employee).filter(models.Employee.id == updated_order.employee).first()

    order_validate(store, customer, employee)

    existing_order.creation_date = updated_order.creation_date
    existing_order.deadline = updated_order.deadline
    existing_order.store = store 
    existing_order.customer = customer 
    existing_order.employee = employee 
    existing_order.status = updated_order.status

    db.commit()
    db.refresh(existing_order)

    return existing_order

@app.delete("/api/orders/{order_id}", response_model=OrderSchema)
async def delete_order(order_id: int, db: Session = Depends(services.get_db)):
    existing_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(existing_order)
    db.commit()
    return {"message": "Order deleted successfully"}

@app.get("/api/visits/{visit_id}/", response_model=VisitSchema)
async def get_visit_by_id(visit_id: int = Path(), db: Session = Depends(services.get_db)):
    visit = db.query(models.Visit).filter(models.Visit.id == visit_id).first()
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit

@app.post("/api/visits/", response_model=VisitSchema)
async def create_visit(visit: CreateVisitSchema, db: Session = Depends(services.get_db)):
    
    employee = db.query(models.Employee).filter(models.Employee.id == visit.employee.id).first()
    order = db.query(models.Order).filter(models.Order.id == visit.order.id).first()
    customer = db.query(models.Customer).filter(models.Customer.id == visit.order.id).first()
    store = db.query(models.Store).filter(models.Store.id == visit.order.id).first()

    if (employee or order or customer or store) is None:
        raise HTTPException(status_code=500, detail="Wrong data!")

    visit_obj = models.Visit(
        creation_date=visit.creation_date,
        employee=employee,
        order=order,
        customer=customer,
        store=store,
    )

    db.add(visit_obj)
    db.commit()
    db.refresh(visit_obj)
    return visit_obj


@app.put("/api/visits/{visit_id}", response_model=VisitSchema)
async def update_visit(visit_id: int, updated_visit: CreateVisitSchema, db: Session = Depends(services.get_db)):
    existing_visit = db.query(models.Visit).filter(models.Visit.id == visit_id).first()
    
    if existing_visit is None:
        raise HTTPException(status_code=404, detail="Visit found")

    store = db.query(models.Store).filter(models.Store.id == updated_visit.store.id).first()
    customer = db.query(models.Customer).filter(models.Customer.id == updated_visit.customer.id).first() 
    employee = db.query(models.Employee).filter(models.Employee.id == updated_visit.employee.id).first()

    if (store or customer or employee) is None:
        raise HTTPException(status_code=500, detail="Wrong data!")

    existing_visit.creation_date = updated_visit.creation_date
    existing_visit.store = store 
    existing_visit.customer = customer 
    existing_visit.employee = employee 

    db.commit()
    db.refresh(existing_visit)

    return existing_visit

@app.delete("/api/visits/{visit_id}")
async def delete_visit(visit_id: int, db: Session = Depends(services.get_db)):
    existing_visit = db.query(models.Visit).filter(models.Visit.id == visit_id).first()

    if existing_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")

    db.delete(existing_visit)
    db.commit()
    return {"message": "Visit deleted successfully"}


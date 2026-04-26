from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="SEMBA Inventory API")

@app.get("/api/products", tags=["Products"])
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()

@app.post("/api/products", response_model=schemas.Product, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas

# إنشاء الجداول
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="SEMBA Inventory API",
    description="Advanced Inventory Management for SEMBA Brand",
    version="1.0.0"
)

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

@app.put("/api/products/{product_id}", tags=["Products"])
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
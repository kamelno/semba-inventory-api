from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SEMBA Inventory API")

@app.get("/products", response_model=list[schemas.Product])
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()

@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(
        name=product.name, 
        price=product.price, 
        stock=product.stock,
        color=product.color  
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": f"Product with ID {product_id} deleted successfully"}
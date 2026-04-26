from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.orm import Session
from jose import jwt, JWTError 
from . import models, database, schemas
from .auth import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="SEMBA Inventory API")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/")
def home():
    return {"message": "Welcome to SEMBA Inventory Professional API!"}


@app.post("/auth/register", response_model=schemas.UserOut, tags=["Auth"])
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed = hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", tags=["Auth"])
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Wrong username or password")
    
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/products", tags=["Products"])
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()

@app.post("/api/products", response_model=schemas.Product, tags=["Products"])
def create_product(
    product: schemas.ProductCreate, 
    db: Session = Depends(database.get_db),
    current_user: str = Depends(get_current_user)
):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.delete("/api/products/{product_id}", tags=["Products"])
def delete_product(
    product_id: int, 
    db: Session = Depends(database.get_db),
    current_user: str = Depends(get_current_user)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
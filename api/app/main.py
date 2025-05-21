from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas, auth, scraper
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insper Cloud - RESTful API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

security = HTTPBearer()

@app.post("/registrar", response_model=schemas.Token)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.senha)
    db_user = models.User(
        name=user.nome,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    token_data = {"sub": str(db_user.id), "name": db_user.name}
    jwt_token = auth.create_jwt_token(token_data)
    
    return {"jwt": jwt_token}

@app.post("/login", response_model=schemas.Token)
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not auth.verify_password(user_credentials.senha, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token_data = {"sub": str(db_user.id), "name": db_user.name}
    jwt_token = auth.create_jwt_token(token_data)
    
    return {"jwt": jwt_token}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = auth.decode_jwt_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@app.get("/consultar")
def get_bovespa_data(current_user: models.User = Depends(get_current_user), format: Optional[str] = "json"):
    if format.lower() == "csv":
        return scraper.get_bovespa_data_csv()
    else:
        return scraper.get_bovespa_data()

@app.get("/")
def read_root():
    return {"status": "API is running"} 
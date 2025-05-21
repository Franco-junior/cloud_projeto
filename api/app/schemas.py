from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    nome: str
    senha: str

class User(UserBase):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    senha: str

class Token(BaseModel):
    jwt: str 
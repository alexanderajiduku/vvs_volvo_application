from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str

    
    
class UserCreate(UserBase):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str  

    class Config:
        orm_mode = True  


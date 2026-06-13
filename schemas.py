from pydantic import BaseModel, Field
class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=2)
class UserResponse(BaseModel):
    id: int
    email: str
    role:str
    is_active:bool
    model_config={"from_attributes":True}
class Token(BaseModel):
    access_token: str
    token_type: str
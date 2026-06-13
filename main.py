from fastapi import FastAPI,Request
from routers import auth,users
from database import Base,engine
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(users.router)
@app.get("/",tags=["Health"])
def health_check():
    return {"status":"ok","version":"1.0.0"}


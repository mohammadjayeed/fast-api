
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, post, user
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# fastapi works its way down the first match
# function, decorator, http method and path
     

@app.get("/")  
def root():  # try to be descriptive
    return {"message":"hello world fastapi"}
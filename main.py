from fastapi import FastAPI


app = FastAPI()


# function, decorator, http method and path

@app.get("/")  
def root():  # try to be descriptive
    return {"message":"hello world fastapi"}



@app.get("/posts")
def get_posts():
    # logic
    return {"data":"This is your posts"}
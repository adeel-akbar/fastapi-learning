from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Hello World !!"}

# Using Postman to test our API since we don't have a frontend yet.

@app.post("/create")
def create_posts(data: dict = Body(...)):
    print(data)
    return {"message": "Successfully created a post"}
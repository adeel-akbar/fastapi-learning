from fastapi import Body,FastAPI
from pydantic import BaseModel

app = FastAPI()
# Practice 1 — Basic GET

# Create:
# GET /about
# It should return something like:
# {
#     "name": "Adeel",
#     "learning": "FastAPI"
# }

@app.get("/about")
def about():
    return {"name": "Adeel", "learning": "FastAPI"}

# Practice 2 — Raw POST body

# Create:
# POST /calculate
# The request body should contain:
# {
#     "a": 10,
#     "b": 5
# }
# Use Body(...) and return:
# {
#     "sum": 15,
#     "difference": 5
# }
# Don't use Pydantic for this one.

@app.post("/calculate")
def calculate(calculation: dict = Body(...)):
    return {"sum": calculation['a'] + calculation['b'],
            "difference": calculation['a'] - calculation['b']}

# Practice 3 — Pydantic schema

# Create a model called Product containing:
# name → string
# price → float
# in_stock → boolean, default True
# description → optional string, default None
# Then create:
# POST /products
# and return the received product.

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    description: str | None = None

@app.post("/products")
def create_product(product: Product):
    return {"product": product}


# Practice 4 — Validation

# Using your Product model, test these through Postman:
# Valid:
# {
#     "name": "Keyboard",
#     "price": 2500
# }
# Then deliberately send:
# {
#     "name": "Keyboard",
#     "price": "hello"
# }
# And then:
# {
#     "price": 2500
# }
# Observe what FastAPI/Pydantic does.
# Don't just look at the result — understand why it happened.
'''ANSWERS'''
# The first one prints just fine because name is string and price is also a number.
# The second one throws error because the number field is string but we are requiring 
# a number(float).
# The third one throws error because the name field is not defined which is 
# required.

# Practice 5 — Explain this code

# Without running it, tell me what happens when each of these requests is sent:
# class User(BaseModel):
#     username: str
#     age: int
#     active: bool = True
#     bio: str | None = None
# A:
# {
#     "username": "Adeel",
#     "age": 21
# }
'''ANSWER'''
# {
#     "username": "Adeel",
#     "age": 21,
#     "active": true,
#     "bio": null
# }
# B:
# {
#     "username": "Adeel",
#     "age": 21,
#     "active": false
# }
'''ANSWER'''
# {
#     "username": "Adeel",
#     "age": 21,
#     "active": false,
#     "bio": null
# }
# C:
# {
#     "username": "Adeel"
# }
'''ANSWER'''
# This will trow an error because the age field which is required and take int
# is empty. 
# D:
# {
#     "username": "Adeel",
#     "age": "hello"
# }
'''ANSWER'''
# Throws an error because the age field requires a int and string is given.
# For each one, tell me:
# Will it succeed or fail, and why?
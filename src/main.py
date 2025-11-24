from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from math import pow

app = FastAPI(title="Ragu Calculator API")

# Pydantic Models
# -----------------------------
class Numbers(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")

class Result(BaseModel):
    operation: str
    a: float
    b: float
    result: Optional[float] = None
    error: Optional[str] = None

# In-memory history
history: List[Result] = []

# -----------------------------
# Utility functions
# -----------------------------
def save_history(op: str, a: float, b: float, result: Optional[float], error: Optional[str] = None):
    """Save operation result to in-memory history"""
    history.append(Result(operation=op, a=a, b=b, result=result, error=error))

# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/", summary="Home endpoint")
def home():
    """Welcome message for the calculator API"""
    return {"message": "Welcome to the FastAPI Calculator!"}

@app.get("/history", response_model=List[Result], summary="Get operation history")
def get_history():
    """Returns a list of all previous calculations"""
    return history

# For each operation we support both GET (query params) and POST (JSON body).
# Tests in this repository use GET with query params, so GET handlers are required.

# Add
@app.get("/add", response_model=Result, summary="Add two numbers (GET)")
@app.post("/add", response_model=Result, summary="Add two numbers (POST)")
def add(nums: Optional[Numbers] = None, a: Optional[float] = Query(None), b: Optional[float] = Query(None)):
    if nums is not None:
        a_val, b_val = nums.a, nums.b
    else:
        if a is None or b is None:
            raise HTTPException(status_code=400, detail="Query params a and b are required")
        a_val, b_val = a, b

    result = a_val + b_val
    save_history("add", a_val, b_val, result)
    return Result(operation="add", a=a_val, b=b_val, result=result)

# Subtract
@app.get("/subtract", response_model=Result, summary="Subtract two numbers (GET)")
@app.post("/subtract", response_model=Result, summary="Subtract two numbers (POST)")
def subtract(nums: Optional[Numbers] = None, a: Optional[float] = Query(None), b: Optional[float] = Query(None)):
    if nums is not None:
        a_val, b_val = nums.a, nums.b
    else:
        if a is None or b is None:
            raise HTTPException(status_code=400, detail="Query params a and b are required")
        a_val, b_val = a, b

    result = a_val - b_val
    save_history("subtract", a_val, b_val, result)
    return Result(operation="subtract", a=a_val, b=b_val, result=result)

# Multiply
@app.get("/multiply", response_model=Result, summary="Multiply two numbers (GET)")
@app.post("/multiply", response_model=Result, summary="Multiply two numbers (POST)")
def multiply(nums: Optional[Numbers] = None, a: Optional[float] = Query(None), b: Optional[float] = Query(None)):
    if nums is not None:
        a_val, b_val = nums.a, nums.b
    else:
        if a is None or b is None:
            raise HTTPException(status_code=400, detail="Query params a and b are required")
        a_val, b_val = a, b

    result = a

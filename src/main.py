from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

# ❌ Hardcoded secret (SonarQube will flag this)
API_KEY = "12345-SECRET-KEY"

# ❌ Unsafe global database connection (SonarQube warning)
conn = sqlite3.connect("test.db", check_same_thread=False)

@app.get("/login")
def login(username: str):
    # ❌ SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor = conn.execute(query)
    result = cursor.fetchone()
    return {"user": result}

@app.post("/execute")
async def execute(request: Request):
    body = await request.json()
    code = body.get("code")

    # ❌ Dangerous: executing user-provided code
    exec(code)  # SonarQube flags "Use of exec is insecure"

    return {"status": "Executed"}

@app.get("/secret")
def secret():
    # ❌ Sensitive data exposure
    return {"api_key": API_KEY}

@app.get("/divide")
def divide(a: float, b: float):
    # ❌ Missing proper validation & potential ZeroDivisionError
    return {"result": a / b}

@app.get("/calc")
def calc(expr: str):
    # ❌ SECURITY ISSUE: Using eval on user-controlled input
    return {"result": eval(expr)}


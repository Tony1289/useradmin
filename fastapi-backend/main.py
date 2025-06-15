from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from typing import Literal
import mysql.connector
import bcrypt
import os

# Load environment variables
load_dotenv()

# Retrieve all required environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
ADMIN_CODE_HASH = os.getenv("ADMIN_SECURITY_CODE_HASH")

# Validate environment variables
required_env_vars = {
    "DB_HOST": DB_HOST,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
    "ADMIN_SECURITY_CODE_HASH": ADMIN_CODE_HASH,
}

for var, value in required_env_vars.items():
    if not value:
        raise Exception(f"Environment variable {var} must be set")

# Initialize FastAPI
app = FastAPI()

# MySQL connection using environment variables
DB_CONFIG = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME
}
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Pydantic models
class SignupModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal['user', 'admin']
    security_code: str = None

class LoginModel(BaseModel):
    username: str
    password: str
    role: Literal['user', 'admin']
    security_code: str = None

# Helper function to hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Helper function to check password
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Signup route
@app.post("/signup")
def signup(data: SignupModel):
    if data.role == 'admin':
        if not data.security_code or not bcrypt.checkpw(data.security_code.encode(), ADMIN_CODE_HASH.encode()):
            raise HTTPException(status_code=403, detail="Invalid admin security code")

    hashed_pwd = hash_password(data.password)

    cursor.execute("SELECT * FROM users WHERE username=%s", (data.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Username already exists")

    cursor.execute(
        "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
        (data.username, data.email, hashed_pwd, data.role)
    )
    conn.commit()
    return {"message": f"{data.role.capitalize()} signed up successfully"}

# Login route
@app.post("/login")
def login(data: LoginModel):
    cursor.execute("SELECT password, role FROM users WHERE username=%s", (data.username,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_password, stored_role = result
    if stored_role != data.role:
        raise HTTPException(status_code=403, detail="Incorrect login path for this role")

    if not verify_password(data.password, stored_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    if data.role == 'admin':
        if not data.security_code or not bcrypt.checkpw(data.security_code.encode(), ADMIN_CODE_HASH.encode()):
            raise HTTPException(status_code=403, detail="Invalid admin security code")

    return {"message": f"{data.role.capitalize()} logged in successfully"}

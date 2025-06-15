from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt

# Load .env variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
ADMIN_CODE_HASH = os.getenv("ADMIN_CODE_HASH")

# App instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SignupData(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    security_code: str | None = None

class LoginData(BaseModel):
    email: EmailStr
    password: str

# Database connection function
def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Create users table (run once)
@app.on_event("startup")
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS newusers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            role ENUM('user', 'admin'),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()
    db.close()

@app.post("/signup")
def signup(data: SignupData):
    db = get_db()
    cursor = db.cursor()

    # Admin validation
    if data.role == "admin":
        if not data.security_code:
            raise HTTPException(status_code=400, detail="Security code is required for admin.")
        if not bcrypt.checkpw(data.security_code.encode(), ADMIN_CODE_HASH.encode()):
            raise HTTPException(status_code=403, detail="Invalid admin security code.")

    hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (data.username, data.email, hashed_pw.decode(), data.role)
        )
        db.commit()
        return {"message": f"{data.role.capitalize()} registered successfully!"}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists.")
    finally:
        db.close()

@app.post("/login")
def login(data: LoginData):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (data.email,))
    user = cursor.fetchone()
    db.close()

    if user and bcrypt.checkpw(data.password.encode(), user["password"].encode()):
        return {"message": f"Welcome back, {user['username']}!", "role": user["role"]}
    raise HTTPException(status_code=401, detail="Invalid email or password.")

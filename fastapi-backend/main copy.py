# --- FastAPI Backend (main.py) ---
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
import mysql.connector
import bcrypt
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
ADMIN_CODE_HASH = os.getenv("ADMIN_CODE_HASH")  # hashed using bcrypt

app = FastAPI()

# Allow CORS (for frontend interaction)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class SignupData(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    security_code: str | None = None

class LoginData(BaseModel):
    email: EmailStr
    password: str
    role: str
    security_code: str | None = None

class LogoutData(BaseModel):
    email: EmailStr

# DB connection helper
def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.post("/signup")
def signup(data: SignupData):
    db = get_db()
    cursor = db.cursor()

    if data.role == "admin":
        if not data.security_code or not bcrypt.checkpw(data.security_code.encode(), ADMIN_CODE_HASH.encode()):
            raise HTTPException(status_code=403, detail="Invalid admin security code.")

    hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    hashed_email = bcrypt.hashpw(data.email.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute(
            """
            INSERT INTO newusers (username, hashed_email, hashed_password, login_time, logout_time, role)
            VALUES (%s, %s, %s, NULL, NULL, %s)
            """,
            (data.username, hashed_email, hashed_pw, data.role)
        )
        db.commit()
        return {"message": f"{data.role.capitalize()} registered successfully!"}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists.")
    finally:
        db.close()

@app.post("/login")
def login(data: LoginData):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM newusers")
    all_users = cursor.fetchall()

    matched_user = None
    for user in all_users:
        if bcrypt.checkpw(data.email.encode(), user["hashed_email"].encode()):
            matched_user = user
            break

    if not matched_user or not bcrypt.checkpw(data.password.encode(), matched_user["hashed_password"].encode()):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    if data.role == "admin":
        if not data.security_code or not bcrypt.checkpw(data.security_code.encode(), ADMIN_CODE_HASH.encode()):
            db.close()
            raise HTTPException(status_code=403, detail="Invalid admin security code.")

    login_time = datetime.now()
    hashed_email = bcrypt.hashpw(data.email.encode(), bcrypt.gensalt()).decode()
    hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    cursor.execute(
        """
        INSERT INTO loginlogs (email, username, hashed_email, hashed_password, login_time, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (data.email, matched_user["username"], hashed_email, hashed_pw, login_time, data.role)
    )
    db.commit()
    db.close()

    return {"message": f"Welcome back, {matched_user['username']}!", "role": data.role}

@app.post("/logout")
def logout(data: LogoutData):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE loginlogs
        SET logout_time = %s
        WHERE email = %s AND logout_time IS NULL
        ORDER BY login_time DESC
        LIMIT 1
        """,
        (datetime.now(), data.email)
    )
    db.commit()
    db.close()

    return {"message": "Logout time recorded successfully."}

@app.get("/admin/users")
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT username, hashed_email, hashed_password, login_time, logout_time
        FROM loginlogs
        WHERE role = 'user'
        """
    )
    logs = cursor.fetchall()
    db.close()
    return {"users": logs}

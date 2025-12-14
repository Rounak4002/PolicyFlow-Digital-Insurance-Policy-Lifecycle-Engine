from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import date

app = FastAPI(title="PolicyFlow API")

DB_NAME = "policyflow.db"

class Policy(BaseModel):
    id: int | None = None
    customer_name: str
    policy_type: str
    premium_amount: float
    start_date: date
    end_date: date
    status: str = "Active"

def get_db():
    return sqlite3.connect(DB_NAME)

@app.on_event("startup")
def startup():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            policy_type TEXT,
            premium_amount REAL,
            start_date TEXT,
            end_date TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.post("/policies")
def create_policy(policy: Policy):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO policies (customer_name, policy_type, premium_amount, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)",
        (policy.customer_name, policy.policy_type, policy.premium_amount, policy.start_date, policy.end_date, policy.status)
    )
    conn.commit()
    conn.close()
    return {"message": "Policy created successfully"}

@app.get("/policies", response_model=List[Policy])
def list_policies():
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM policies").fetchall()
    conn.close()
    return [
        Policy(
            id=r[0],
            customer_name=r[1],
            policy_type=r[2],
            premium_amount=r[3],
            start_date=r[4],
            end_date=r[5],
            status=r[6]
        )
        for r in rows
    ]

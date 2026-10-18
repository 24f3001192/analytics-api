from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# This satisfies the CORS requirement in the assignment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_xoh1apdsobos82j7vipxqoj2"
MY_EMAIL = "24f3001192@ds.study.iitm.ac.in" 

# Define what the incoming data looks like
class Event(BaseModel):
    user: str
    amount: float
    ts: int

class EventBatch(BaseModel):
    events: List[Event]

@app.post("/analytics")
async def process_analytics(
    batch: EventBatch,
    x_api_key: Optional[str] = Header(None) # FastAPI automatically looks for 'X-API-Key'
):
    # 1. Security Check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2. Math Setup
    events = batch.events
    total_events = len(events)
    unique_users = set()
    user_spending = {}
    revenue = 0.0

    # 3. Calculate Totals
    for event in events:
        unique_users.add(event.user)
        
        # Only process positive amounts for revenue and top user
        if event.amount > 0:
            revenue += event.amount
            user_spending[event.user] = user_spending.get(event.user, 0.0) + event.amount
    
    # 4. Find the Top Spender
    top_user = ""
    max_spent = -1
    for user, spent in user_spending.items():
        if spent > max_spent:
            max_spent = spent
            top_user = user

    # 5. Return the Final Report
    return {
        "email": MY_EMAIL,
        "total_events": total_events,
        "unique_users": len(unique_users),
        "revenue": revenue,
        "top_user": top_user
    }
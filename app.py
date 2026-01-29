from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="POWERGRID AI Ticketing API")

class TicketRequest(BaseModel):
    name: str
    emp_id: str
    email: str
    phone: str
    subject: str
    body: str

@app.post("/predict")
def predict_ticket(data: TicketRequest):
    return {
        "employee": data.name,
        "ticket_type": "VPN Issue",
        "priority": "High",
        "queue": "Network Team",
        "solution": "Please reset VPN and try again."
    }

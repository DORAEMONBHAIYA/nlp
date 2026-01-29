from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import re
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="POWERGRID AI Ticketing API")

# ===== Load Models =====
type_model = joblib.load("type_model.pkl")
lang_model = joblib.load("lang_model.pkl")
queue_model = joblib.load("queue_model.pkl")
tfidf = joblib.load("tfidf.pkl")
kb_df = joblib.load("kb.pkl")

# ===== Utils =====
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def suggest_solution(text):
    vec = tfidf.transform([text])
    kb_vec = tfidf.transform(kb_df["clean_text"])
    idx = cosine_similarity(vec, kb_vec).argmax()
    return kb_df.iloc[idx]["answer"]

def assign_priority(text, ticket_type):
    if any(w in text.lower() for w in ["urgent", "asap", "critical"]):
        return "High"
    return "Medium"

# ===== Request Schema =====
class Ticket(BaseModel):
    name: str
    emp_id: str
    email: str
    phone: str
    subject: str
    body: str

# ===== API Endpoint =====
@app.post("/predict")
def predict(ticket: Ticket):
    raw = ticket.subject + " " + ticket.body
    clean = clean_text(raw)
    vec = tfidf.transform([clean])

    return {
        "ticket_type": type_model.predict(vec)[0],
        "language": lang_model.predict(vec)[0],
        "queue": queue_model.predict(vec)[0],
        "priority": assign_priority(raw, ""),
        "solution": suggest_solution(clean)
    }

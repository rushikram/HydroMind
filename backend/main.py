from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from backend.db import init_db, add_entry, get_history, reset_db
from backend.models import WaterEntry
from agent.hydration_agent import run_agent
from datetime import datetime
import time

# Initialize FastAPI app
app = FastAPI()

# Allow all CORS origins for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run on startup
@app.on_event("startup")
def startup_event():
    print("🔧 Initializing database...")
    init_db()

# Background reminder function
def send_reminder():
    print(f"[Reminder] Time to hydrate! — {datetime.now().strftime('%H:%M:%S')}")

def schedule_reminder(delay_minutes: int = 60):
    time.sleep(delay_minutes * 60)
    send_reminder()

# Route to log water intake
@app.post("/add-entry/")
def add_water_entry(entry: WaterEntry, background_tasks: BackgroundTasks):
    try:
        result = add_entry(entry.amount_ml)
        background_tasks.add_task(schedule_reminder, delay_minutes=60)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Route to get water intake history
@app.get("/history/")
def get_water_history():
    try:
        return get_history()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Route to query hydration AI agent
@app.post("/ask-agent/")
async def ask_agent(request: Request):
    try:
        body = await request.json()
        question = body.get("question")
        groq_key = body.get("groq_key")
        goal_ml = body.get("goal_ml", 2000)

        if not question or not groq_key:
            return {"response": "Missing question or API key."}

        response = run_agent(question, groq_key, goal_ml)
        return {"response": response}
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}

# Route to manually reset hydration log
@app.post("/reset/")
def reset_water_log():
    try:
        reset_db()
        return {"status": "reset", "message": "Hydration log cleared."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

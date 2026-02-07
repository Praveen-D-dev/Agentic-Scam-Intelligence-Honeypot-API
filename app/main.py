from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import time

# Import your custom modules
import model_engine as engine
import data_extractor as detective
import agent_brain as agent

app = FastAPI(title="Agentic Honey-Pot System v2.0")

# --- API Schemas ---
class IncomingMessage(BaseModel):
    sender: str
    message: str
    message_count: int = 1

class FinalResponse(BaseModel):
    state: str
    ml_confidence: float
    extracted_intel: dict
    ai_reply: str
    timestamp: int

# --- The Master Workflow ---
@app.post("/process", response_model=FinalResponse)
async def process_scam_logic(data: IncomingMessage):
    try:
        # 1. Classification (Security Guard)
        # Determines if the user is a SCAMMER, SUSPICIOUS, or HAM
        state, confidence = engine.classify_message(data.message)

        # 2. Intelligence Extraction (Detective)
        # Pulls UPI IDs, Links, and Keywords regardless of state
        intel = detective.extract_intelligence(data.message)

        # 3. Agentic Response (The Voice)
        # Selects one of the 3 prompting paths based on the 'state'
        reply = agent.get_agent_response(data.message, state)

        # 4. Return the consolidated intelligence package
        return {
            "state": state,
            "ml_confidence": round(confidence, 2),
            "extracted_intel": intel,
            "ai_reply": reply,
            "timestamp": int(time.time())
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")

# --- Execution ---
if __name__ == "__main__":
    import uvicorn
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)

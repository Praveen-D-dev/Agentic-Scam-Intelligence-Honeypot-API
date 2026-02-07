🧠 Agentic Scam Intelligence Honeypot API

A FastAPI-based agentic system that detects scam messages and engages suspected scammers in controlled conversations to extract high-confidence fraud indicators such as UPI IDs, payment handles, phishing links, and scam scripts.

The system uses a local language model for response generation and does not rely on IP tracking, cloud APIs, or invasive data collection.

🎯 Objective

Scam operations depend on:

reusable payment identifiers

scripted social-engineering messages

repeated behavioral patterns

Most systems stop at classification.
This project goes one step further: intelligence collection.

🧩 How It Works

Incoming messages are analyzed using a hybrid ML + rule-based classifier

Scam indicators (UPI IDs, URLs, keywords) are extracted

A state-aware agent generates short, human-like replies using a local LLM

Responses are designed to encourage further disclosure without escalation

The API returns consolidated intelligence for analysis

🏗️ Architecture
Incoming Message
      ↓
Hybrid Classifier (ML + Rules)
      ↓
Intel Extraction (UPI, URLs, keywords)
      ↓
Agentic Reply Generator
(Local LLM via llama.cpp CLI)
      ↓
Structured Intelligence Output

🛠️ Tech Stack

Python 3

FastAPI

Scikit-learn

Regex-based NLP

Local LLM (GGUF format via llama.cpp CLI)

Agent-controlled prompt logic

✨ Core Features

Message classification: SCAMMER / SUSPICIOUS / HAM

Extraction of payment identifiers (UPI IDs, account patterns)

Phishing link and keyword detection

Local LLM-powered conversational replies

Strict output control (short, WhatsApp-style responses)

No IP logging or device fingerprinting

Modular and extensible design

⚖️ Legal & Ethical Design

No IP address collection

No user deanonymization

No impersonation of banks or authorities

Only processes voluntarily provided message text

Designed for research, detection, and prevention

No blocking or enforcement actions

📂 Project Structure
agentic-scam-honeypot/
│
├── app/
│   ├── main.py
│   ├── model_engine.py
│   ├── data_extractor.py
│   ├── agent_brain.py
│
├── models/
│   └── model.py
│
├── requirements.txt
├── .gitignore
├── README.md
├── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

🚀 Running the Project
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Add ML model (optional)

Place the trained classifier here:

models/final_high_acc_model.pkl


If the model is not present, the system can still run with rule-based detection.

3️⃣ Configure Local LLM

This project uses a local GGUF chat model via llama.cpp.

Update paths in agent_brain.py:

LLAMA_CLI_PATH = "path/to/llama-cli"
MODEL_PATH = "path/to/model.gguf"


Any llama.cpp-compatible chat model can be used.

4️⃣ Start the API
uvicorn app.main:app --reload


API will be available at:

http://localhost:8000

🔗 API Endpoint
POST /process

Request

{
  "sender": "unknown",
  "message": "Your bank account will be blocked. Pay immediately to abc@upi",
  "message_count": 1
}


Response

{
  "state": "SCAMMER",
  "ml_confidence": 0.78,
  "extracted_intel": {
    "upiIds": ["abc@upi"],
    "phishingLinks": [],
    "suspiciousKeywords": ["blocked", "urgent"]
  },
  "ai_reply": "Which bank should I use to make this payment?"
}

🔮 Planned Enhancements

Conversation memory and session tracking

Scam pattern clustering

Multi-language scam detection

Intelligence analytics dashboard

Advanced agent deception strategies

📜 Disclaimer

This project is intended strictly for educational and research purposes.
It does not identify individuals, perform enforcement actions, or claim legal authority.

👤 Author

Lord
Focus areas: AI systems, backend engineering, security-aware design

🔥 Final note (straight talk)

This README positions your work as:

agentic

security-aware

ethically defensible

technically mature

This is no longer a “college FastAPI project”.
This is portfolio-grade.

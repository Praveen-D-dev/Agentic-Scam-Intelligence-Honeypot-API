import subprocess
import re
import time

# --------------------------------------------------
# CONFIGURATION (CHANGE ONLY IF PATHS CHANGE)
# --------------------------------------------------

LLAMA_CLI_PATH = r"D:\scam\llama-b7947-bin-win-cpu-x64\llama-cli.exe"
MODEL_PATH = r"D:\scam\TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"

# --------------------------------------------------
# OUTPUT CLEANER (CRITICAL)
# --------------------------------------------------

def clean_llama_output(raw_output: str) -> str:
    """
    Cleans llama-cli output and guarantees a WhatsApp-style reply.
    """

    if not raw_output:
        return "Could you clarify that?"

    # Remove performance stats
    raw_output = re.sub(r"\[ Prompt:.*?\]", "", raw_output, flags=re.DOTALL)

    # Remove exit text
    raw_output = raw_output.replace("Exiting...", "").strip()

    # Extract assistant response
    if "<|assistant|>" in raw_output:
        raw_output = raw_output.split("<|assistant|>")[-1]

    # Remove role tokens
    raw_output = re.sub(r"<\|.*?\|>", "", raw_output)

    # Normalize whitespace
    raw_output = raw_output.replace("\r", "\n")

    # Split into clean lines
    lines = [line.strip() for line in raw_output.split("\n") if line.strip()]

    # Fallback (MANDATORY)
    if not lines:
        return "Could you clarify that?"

    # Limit verbosity (2 short lines max)
    return " ".join(lines[:2])


# --------------------------------------------------
# CORE LLM CALL
# --------------------------------------------------

def get_agent_response(user_message: str, state: str) -> str:
    """
    Generates a controlled scam-bait reply using llama-cli.
    """

    # ---- STATE-BASED SYSTEM PROMPTS ----

    if state == "SCAMMER":
        system_prompt = (
            "You are a normal person chatting on WhatsApp. "
            "You are confused but cooperative. "
            "Ask short questions to get payment or identity details. "
            "Reply in one or two sentences only. "
            "Do not explain anything."
        )

    elif state == "SUSPICIOUS":
        system_prompt = (
            "You are unsure who this person is. "
            "Reply politely and ask one short question to verify identity. "
            "Keep the reply very short."
        )

    else:  # HAM
        system_prompt = (
            "You are a professional person. "
            "Reply briefly and politely in one short sentence."
        )

    # ---- CHAT TEMPLATE ----

    prompt = f"""<|system|>
{system_prompt}
</s>
<|user|>
{user_message}
</s>
<|assistant|>
"""

    command = [
        LLAMA_CLI_PATH,
        "-m", MODEL_PATH,
        "-p", prompt,
        "--single-turn",
        "-n", "80",
        "--temp", "0.6",
        "-t", "4",
        "--no-display-prompt"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30
        )

        return clean_llama_output(result.stdout)

    except Exception:
        return "Could you clarify that?"


# --------------------------------------------------
# DEMO / TEST ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    tests = [
        ("Your account will be blocked urgently", "SUSPICIOUS"),
        ("Send the processing fee to hrdepartment@upi", "SCAMMER"),
        ("Meeting confirmed for tomorrow", "HAM")
    ]

    for msg, state in tests:
        response = get_agent_response(msg, state)
        print("\n-----------------------------")
        print("STATE:", state)
        print("INPUT:", msg)
        print("BOT :", response)
        time.sleep(1)

"""
File: os_layer/ai/groq_translator.py

Purpose
-------
This module translates natural language user commands into a structured
OS command schema using the Groq LLM API.

The translator is the first stage of the OS command pipeline.

Pipeline Flow
-------------
User Text
    ↓
Groq Translator
    ↓
Structured JSON Command
    ↓
Validation Layer
    ↓
Execution Router
    ↓
Execution Engines

Design Goals
------------
* Strict JSON output from the LLM
* Strong error handling
* Safe API communication
* Defensive parsing of model output
* Clear debugging logs for pipeline inspection
"""

import os
import json
import requests
from time import sleep


# -------------------------------------------------
# GROQ CONFIGURATION
# -------------------------------------------------

# API key loaded from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq OpenAI-compatible endpoint
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# -------------------------------------------------
# SYSTEM PROMPT
# -------------------------------------------------

SYSTEM_PROMPT = """
You convert natural language user requests into structured OS commands.

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include text outside JSON

Command Schema:

{
 "intent": "...",
 "parameters": {},
 "execution_type": "filesystem | application | shell | web | system",
 "risk_level": "low | medium | high"
}

Examples:

User: open calculator
{
 "intent": "open_application",
 "parameters": {"app_name":"calculator"},
 "execution_type": "application",
 "risk_level": "low"
}

User: check system status
{
 "intent": "get_system_info",
 "parameters": {},
 "execution_type": "system",
 "risk_level": "low"
}

User: open youtube
{
 "intent": "open_website",
 "parameters": {"url":"https://youtube.com"},
 "execution_type": "web",
 "risk_level": "low"
}
"""


# -------------------------------------------------
# TRANSLATION FUNCTION
# -------------------------------------------------

def translate_to_structured_command(user_text: str) -> dict:
    """
    Converts a natural language command into a structured OS command.

    Parameters
    ----------
    user_text : str
        The natural language instruction from the user.

    Returns
    -------
    dict
        Structured command dictionary that follows the OS command schema.

    Raises
    ------
    RuntimeError
        If the Groq API request fails.

    ValueError
        If the model returns invalid JSON.
    """

    # -------------------------------------------------
    # Validate API Key
    # -------------------------------------------------

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY environment variable not set")

    # -------------------------------------------------
    # Prepare Request Headers
    # -------------------------------------------------

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # -------------------------------------------------
    # Prepare Request Payload
    # -------------------------------------------------

    payload = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }

    # -------------------------------------------------
    # Send Request to Groq
    # -------------------------------------------------

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
    except Exception as e:
        raise RuntimeError(f"Groq API request failed: {str(e)}")

    # -------------------------------------------------
    # Validate HTTP Response
    # -------------------------------------------------

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq API returned error {response.status_code}: {response.text}"
        )

    # -------------------------------------------------
    # Parse Response JSON
    # -------------------------------------------------

    data = response.json()

    # Ensure expected structure exists
    if "choices" not in data or not data["choices"]:
        raise RuntimeError(f"Unexpected Groq response format: {data}")

    # Extract model output
    content = data["choices"][0]["message"]["content"]

    # -------------------------------------------------
    # Clean Output (Remove Markdown Blocks if Model Adds Them)
    # -------------------------------------------------

    content = content.strip()

    if content.startswith(""):
        content = content.replace("json", "").replace("```", "").strip()

    # -------------------------------------------------
    # Convert JSON Text → Python Dict
    # -------------------------------------------------

    try:
        structured_command = json.loads(content)
    except Exception as e:
        raise ValueError(f"Invalid JSON returned by Groq: {content}")

    # -------------------------------------------------
    # Debug Log (Useful During Development)
    # -------------------------------------------------

    print("GROQ STRUCTURED COMMAND:", structured_command)

    return structured_command
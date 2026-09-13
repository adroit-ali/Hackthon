"""
Utility functions for validation, Groq LLM invocation, and JSON sanitization.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


def get_groq_api_key() -> str:
    """Retrieve Groq API key from environment or Streamlit secrets."""
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            key = ""
    return key.strip()


def sanitize_json_response(raw_text: str) -> Dict[str, Any]:
    """Extract and parse clean JSON from LLM output markdown."""
    clean = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", clean)
    if match:
        clean = match.group(1).strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        json_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", clean)
        if json_match:
            return json.loads(json_match.group(1))
        raise ValueError(f"Could not parse valid JSON from LLM response: {raw_text[:200]}")


def validate_participants(participants: List[Dict[str, Any]]) -> None:
    """Ensure sufficient participants exist to build teams."""
    if not participants:
        raise ValueError("No participants provided.")
    leaders = [p for p in participants if p.get("role") == "leader"]
    members = [p for p in participants if p.get("role") != "leader"]
    if not leaders:
        raise ValueError("At least one Leader with a project idea is required.")
    if len(members) < 3:
        raise ValueError(f"Need at least 3 Members (currently have {len(members)}) to form a 4-person squad.")


def call_groq_llm(prompt: str, model: str = "llama-3.3-70b-versatile", temperature: float = 0.2) -> Optional[Dict[str, Any]]:
    """Invoke Groq API with structured JSON output, returns None if no API key is set."""
    api_key = get_groq_api_key()
    if not api_key:
        return None
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a hackathon team architect. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        response_text = completion.choices[0].message.content
        return sanitize_json_response(response_text)
    except Exception as e:
        print(f"Groq API call failed (falling back to local engine): {e}")
        return None

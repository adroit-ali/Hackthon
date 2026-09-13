"""
Project analyzer module.
Breaks down raw hackathon ideas into essential technical and operational capabilities for an MVP.
"""

from typing import Any, Dict
from prompts import ANALYZE_PROJECT_PROMPT
from utils import call_groq_llm


def heuristic_analyze_project(project_idea: str) -> Dict[str, Any]:
    """Fallback project capability decomposition when Groq API key is not configured."""
    clean = project_idea.lower()
    capabilities = ["Frontend UI", "Backend APIs", "Product / Pitch"]

    if any(w in clean for w in ["ai", "llm", "resume", "assistant", "recommend", "model", "nlp", "vision", "chat"]):
        capabilities.insert(0, "AI / LLM")
    if any(w in clean for w in ["data", "dataset", "analytics", "satellite", "insights"]):
        capabilities.append("Data Engineering")
    if any(w in clean for w in ["audio", "voice", "stream", "realtime", "websocket"]):
        capabilities.append("Real-time Audio / APIs")

    return {
        "title": "Hackathon MVP Project",
        "summary": project_idea.strip()[:200],
        "mvp_goal": "A fully working end-to-end demo ready for live testing during 3-minute judge presentations.",
        "critical_capabilities": capabilities[:5],
        "required_roles": ["Team Leader", "Lead Frontend & UI", "Lead Backend / AI Engineer", "Product & Pitch Lead"],
        "recommended_stack": ["React / Streamlit", "FastAPI", "Python", "Groq / OpenAI API"]
    }


def analyze_project(project_idea: str) -> Dict[str, Any]:
    """Analyze a project idea using Groq LLM with local fallback."""
    if not project_idea.strip():
        return heuristic_analyze_project("Hackathon Project MVP")

    prompt = ANALYZE_PROJECT_PROMPT.format(project_idea=project_idea)
    result = call_groq_llm(prompt)

    if result and "critical_capabilities" in result:
        result.setdefault("title", "Hackathon MVP")
        result.setdefault("summary", project_idea[:200])
        result.setdefault("mvp_goal", "Working hackathon MVP demo")
        return result

    return heuristic_analyze_project(project_idea)

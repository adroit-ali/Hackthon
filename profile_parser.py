"""
Profile parser module.
Extracts structured roles, skills, experience level, and superpowers from messy bios or GitHub links.
"""

import re
from typing import Any, Dict
from prompts import PARSE_PROFILE_PROMPT
from utils import call_groq_llm

SKILL_TAXONOMY = {
    "AI / ML Engineer": ["ai", "machine learning", "ml", "llm", "langchain", "prompt", "nlp", "pytorch", "tensorflow", "vector", "rag", "embeddings"],
    "Frontend Developer": ["frontend", "react", "next.js", "vue", "javascript", "typescript", "tailwind", "html", "css", "svelte", "ui"],
    "Backend Engineer": ["backend", "python", "fastapi", "flask", "node", "express", "django", "rest", "api", "postgresql", "sql", "redis", "mongodb"],
    "UI/UX Designer": ["ui/ux", "figma", "wireframe", "prototype", "design", "user journey", "canva", "product design"],
    "DevOps Engineer": ["docker", "kubernetes", "cloud", "aws", "gcp", "azure", "ci/cd", "git", "linux", "devops", "deployment"],
    "Product / Pitch Lead": ["pitch", "presentation", "demo", "deck", "product management", "storytelling", "research", "technical writer"]
}


def heuristic_parse_bio(name: str, bio: str, github: str = "") -> Dict[str, Any]:
    """Fallback rule-based NLP extraction when Groq API key is not configured."""
    text = (bio + " " + github).lower()
    detected_skills = []
    role_scores = {role: 0 for role in SKILL_TAXONOMY}

    for role, kws in SKILL_TAXONOMY.items():
        for kw in kws:
            if re.search(r"\b" + re.escape(kw) + r"\b", text):
                if kw.title() not in detected_skills:
                    detected_skills.append(kw.title())
                role_scores[role] += 1

    best_role = max(role_scores, key=role_scores.get) if any(role_scores.values()) else "Full-stack Developer"
    
    exp = "intermediate"
    if re.search(r"\b(senior|lead|years|advanced|expert|architect)\b", text):
        exp = "advanced"
    elif re.search(r"\b(beginner|junior|student|learner|new to)\b", text):
        exp = "beginner"

    superpowers = {
        "Frontend Developer": "Rapid visual component implementation & micro-interactions",
        "Backend Engineer": "High-reliability REST endpoints & database schema design",
        "AI / ML Engineer": "LLM prompt optimization, RAG search & model integration",
        "UI/UX Designer": "Polished user journeys & high-converting judge pitch decks",
        "DevOps Engineer": "Zero-downtime containerization & live cloud deployment",
        "Product / Pitch Lead": "Crystal-clear demo storytelling & judge rubric alignment"
    }

    return {
        "name": name.strip() or "Hackathon Contender",
        "primary_role": best_role,
        "skills": detected_skills[:8] if detected_skills else ["Python", "JavaScript", "Problem Solving", "Rapid Prototyping"],
        "experience_level": exp,
        "superpower": superpowers.get(best_role, "Cross-functional feature implementation"),
        "summary": bio.strip() or "Hackathon participant eager to build impactful MVPs."
    }


def parse_participant(participant: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a participant's bio into a structured profile using Groq or local heuristic fallback."""
    name = participant.get("name", "Participant")
    bio = participant.get("bio", "")
    github = participant.get("github", "")

    prompt = PARSE_PROFILE_PROMPT.format(name=name, github=github, bio=bio)
    result = call_groq_llm(prompt)

    if result and "primary_role" in result and "skills" in result:
        result["name"] = name
        result.setdefault("experience_level", "intermediate")
        result.setdefault("superpower", "High-velocity MVP contribution")
        result.setdefault("summary", bio)
        return result

    return heuristic_parse_bio(name, bio, github)

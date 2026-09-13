"""
Team matcher module.
Selects a complementary 3-member cohort to join the project Leader, enforcing role diversity and avoiding redundant skill stacks.
"""

from typing import Any, Dict, List


def role_category(role: str) -> str:
    """Classify role into broad functional archetype."""
    r = role.lower()
    if any(k in r for k in ["frontend", "ui", "ux", "web", "design", "css"]):
        return "frontend_design"
    if any(k in r for k in ["ai", "ml", "data", "llm", "nlp", "machine learning"]):
        return "ai_data"
    if any(k in r for k in ["backend", "api", "database", "devops", "cloud", "system"]):
        return "backend_infra"
    if any(k in r for k in ["pitch", "product", "presentation", "writer", "research"]):
        return "product_pitch"
    return "general_eng"


def form_team(candidates: List[Dict[str, Any]], project: Dict[str, Any], team_size: int = 3) -> List[Dict[str, Any]]:
    """
    Select complementary members using a greedy constraint satisfaction heuristic:
    1. Highest semantic relevance per distinct functional category
    2. Fallback to next best candidates if pool is constrained
    """
    if not candidates:
        return []

    sorted_cands = sorted(candidates, key=lambda c: c.get("semantic_score", 0), reverse=True)
    chosen: List[Dict[str, Any]] = []
    seen_categories = set()

    # Pass 1: pick candidates from distinct functional categories
    for cand in sorted_cands:
        if len(chosen) >= team_size:
            break
        cat = role_category(cand.get("primary_role", ""))
        if cat not in seen_categories:
            seen_categories.add(cat)
            chosen_cand = dict(cand)
            chosen.append(chosen_cand)

    # Pass 2: fill remaining slots if distinct categories were exhausted
    if len(chosen) < team_size:
        chosen_names = {c.get("name") for c in chosen}
        for cand in sorted_cands:
            if len(chosen) >= team_size:
                break
            if cand.get("name") not in chosen_names:
                chosen.append(dict(cand))

    # Assign tactical squad roles & reasons
    for member in chosen:
        role = member.get("primary_role", "Engineer")
        if "Frontend" in role or "UI" in role:
            member["assigned_role"] = "Lead Frontend & User Experience"
            member["selection_reason"] = "Owns UI components, layout design, and smooth user flow for demo day."
        elif "AI" in role or "Data" in role:
            member["assigned_role"] = "Lead AI / Data Pipeline Engineer"
            member["selection_reason"] = "Owns model inference, prompt engineering, and intelligent processing."
        elif "Backend" in role or "DevOps" in role:
            member["assigned_role"] = "Core Backend & Cloud Infrastructure"
            member["selection_reason"] = "Owns REST API endpoints, database schemas, and live deployment uptime."
        elif "Pitch" in role or "Product" in role:
            member["assigned_role"] = "Product Pitch & Presentation Lead"
            member["selection_reason"] = "Owns the 3-minute pitch deck, demo script, and judge value articulation."
        else:
            member["assigned_role"] = role
            member["selection_reason"] = "Selected for cross-functional versatility and technical problem solving."

    return chosen

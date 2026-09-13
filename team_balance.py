"""
Team balance evaluator.
Analyzes collective team capability coverage, role diversity, and overall synergy against project requirements.
"""

from typing import Any, Dict, List
import re


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


ALIASES = {
    "ai": ["ai", "machine learning", "ml", "llm", "langchain", "prompt", "nlp", "rag", "embeddings"],
    "frontend": ["frontend", "react", "javascript", "typescript", "ui", "css", "html", "next js", "tailwind"],
    "backend": ["backend", "api", "fastapi", "flask", "python", "node", "express", "sql", "postgresql"],
    "design": ["design", "ui ux", "figma", "wireframe", "user journey"],
    "devops": ["devops", "docker", "cloud", "deployment", "linux", "ci cd"],
    "pitch": ["pitch", "presentation", "deck", "demo", "product management", "storytelling"]
}


def evaluate_team(team: List[Dict[str, Any]], project: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate realistic project capability coverage, role diversity, and synergy."""
    capabilities = project.get("critical_capabilities") or ["AI / LLM", "Frontend UI", "Backend APIs", "Product / Pitch"]
    
    # 1. Capability Coverage Calculation
    coverage_details = []
    for cap in capabilities:
        cap_norm = _normalize(cap)
        terms = ALIASES.get(cap_norm, [cap_norm])
        
        matches = 0
        for m in team:
            m_text = _normalize(f"{m.get('primary_role', '')} {' '.join(m.get('skills', []))} {m.get('bio', '')}")
            if any(t in m_text for t in terms):
                matches += 1
        
        score = 35 if matches == 0 else (75 if matches == 1 else 95)
        coverage_details.append({
            "capability": cap,
            "match_count": matches,
            "coverage_score": score
        })

    avg_coverage = sum(c["coverage_score"] for c in coverage_details) / max(1, len(coverage_details))

    # 2. Role Diversity Calculation
    roles = [_normalize(m.get("assigned_role", m.get("primary_role", ""))) for m in team]
    unique_categories = set()
    for r in roles:
        if any(k in r for k in ["frontend", "ui", "design"]):
            unique_categories.add("frontend")
        elif any(k in r for k in ["ai", "ml", "data"]):
            unique_categories.add("ai")
        elif any(k in r for k in ["backend", "devops", "infra"]):
            unique_categories.add("backend")
        elif any(k in r for k in ["pitch", "product", "lead", "architect"]):
            unique_categories.add("product")
        else:
            unique_categories.add(r)
            
    diversity_score = min(100.0, (len(unique_categories) / max(1, len(team))) * 100.0)

    # 3. Semantic Relevance & Experience Quality
    semantic_scores = [m.get("semantic_score", 70.0) for m in team if "semantic_score" in m]
    avg_semantic = sum(semantic_scores) / len(semantic_scores) if semantic_scores else 75.0

    exp_weights = {"beginner": 0.9, "intermediate": 1.0, "advanced": 1.1}
    exp_factor = sum(exp_weights.get(m.get("experience_level", "intermediate"), 1.0) for m in team) / max(1, len(team))

    overall_score = round(min(99.0, (avg_coverage * 0.45 + diversity_score * 0.35 + avg_semantic * 0.20) * (exp_factor / 1.02)), 1)

    # Strengths & Gaps
    strengths = []
    gaps = []

    for c in coverage_details:
        if c["coverage_score"] >= 75:
            strengths.append(f"Solid coverage for '{c['capability']}' ({c['match_count']} contributor{'s' if c['match_count'] > 1 else ''}).")
        else:
            gaps.append(f"Limited dedicated coverage for '{c['capability']}' — recommend using pre-built libraries or starter kits.")

    return {
        "overall_score": overall_score,
        "coverage_score": round(avg_coverage, 1),
        "role_diversity_score": round(diversity_score, 1),
        "coverage_details": coverage_details,
        "strengths": strengths[:4],
        "gaps": gaps[:3],
        "team_size": len(team)
    }

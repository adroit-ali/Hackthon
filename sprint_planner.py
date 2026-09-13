"""
Sprint planner module.
Generates a 48-hour time-boxed execution schedule with individual task ownership, milestones, and demo-day checklist.
"""

from typing import Any, Dict, List
from prompts import SPRINT_PLAN_PROMPT
from utils import call_groq_llm


def heuristic_sprint_plan(team: List[Dict[str, Any]], project: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback tailored sprint plan generation."""
    leader = team[0]["name"] if team else "Leader"
    m1 = team[1]["name"] if len(team) > 1 else "Frontend Dev"
    m2 = team[2]["name"] if len(team) > 2 else "Backend Dev"
    m3 = team[3]["name"] if len(team) > 3 else "Pitch Lead"

    return {
        "phases": [
            {
                "name": "Phase 1: Inception & Architecture",
                "timebox": "Hours 0 – 6",
                "objective": "Lock MVP scope, git repo, schema contracts, and UI wireframes",
                "tasks": [
                    {"task": "Initialize Git repository, branch protection & CI deploy pipeline", "owner": m2, "deliverable": "Live staging URL placeholder"},
                    {"task": "Draft high-fidelity Figma UI wireframes & user journey flow", "owner": m1, "deliverable": "Approved 3-screen Figma flow"},
                    {"task": "Define OpenAPI/JSON data contracts & DB models", "owner": leader, "deliverable": "swagger.json / mock API response"},
                    {"task": "Formulate judge value proposition & competitive differentiation narrative", "owner": m3, "deliverable": "1-page pitch thesis"}
                ]
            },
            {
                "name": "Phase 2: Core MVP Build",
                "timebox": "Hours 6 – 24",
                "objective": "Build core functional logic, AI inference, and connect UI to backend",
                "tasks": [
                    {"task": "Develop core AI prompt orchestration, parsing, and error-handling", "owner": leader, "deliverable": "Working LLM inference endpoint"},
                    {"task": "Build responsive UI screens, state management, and file upload components", "owner": m1, "deliverable": "Interactive frontend interface"},
                    {"task": "Implement backend REST endpoints, authentication & vector store index", "owner": m2, "deliverable": "FastAPI server running with tests"},
                    {"task": "Draft judge slide deck (Problem, Solution, Market, Tech Stack)", "owner": m3, "deliverable": "Draft 8-slide presentation"}
                ]
            },
            {
                "name": "Phase 3: Polish & Edge Cases",
                "timebox": "Hours 24 – 38",
                "objective": "End-to-end integration, bug fixes, visual polish, and backup demo video",
                "tasks": [
                    {"task": "Full end-to-end integration test of happy path with mock datasets", "owner": m2, "deliverable": "Zero critical bugs during live test"},
                    {"task": "UI micro-interactions, loading spinners, toast notifications", "owner": m1, "deliverable": "Polished responsive UX"},
                    {"task": "Record backup 2-minute product demo video (in case of live wifi issues)", "owner": m3, "deliverable": "1080p MP4 recording"},
                    {"task": "Feature freeze & code clean-up; update README with architecture diagrams", "owner": leader, "deliverable": "Comprehensive GitHub documentation"}
                ]
            },
            {
                "name": "Phase 4: Pitch & Submission",
                "timebox": "Hours 38 – 48",
                "objective": "3-minute pitch dry runs, Devpost submission, and live judging prep",
                "tasks": [
                    {"task": "Conduct 3 dry-run pitch rehearsals with timed 3-minute stopwatch", "owner": m3, "deliverable": "Pitch completed in under 2:45"},
                    {"task": "Prepare live demo sandbox with pre-loaded realistic data", "owner": leader, "deliverable": "1-click instant demo preset"},
                    {"task": "Complete Devpost project submission with screenshots, tags & live link", "owner": m1, "deliverable": "Confirmed hackathon submission"}
                ]
            }
        ],
        "milestones": [
            {"time": "Hour 6", "name": "Architecture & Wireframe Lock", "deliverable": "Live GitHub repo with boilerplate & approved Figma screen flow"},
            {"time": "Hour 24", "name": "End-to-End Alpha MVP", "deliverable": "Frontend successfully calling backend AI pipeline"},
            {"time": "Hour 38", "name": "Feature Freeze & Video Backup", "deliverable": "Stable demo build and recorded 2-minute backup MP4"},
            {"time": "Hour 48", "name": "Final Submission", "deliverable": "Devpost submitted and live presentation ready"}
        ],
        "demo_checklist": [
            "Verify live demo URL opens in under 2 seconds on incognito browser window",
            "Pre-load realistic demo data so judges do not see empty screens",
            "Upload backup 1080p demo video to YouTube (unlisted)",
            "Hook judges in first 20 seconds with clear problem explanation",
            "Public GitHub repository contains comprehensive README with architecture diagram"
        ]
    }


def generate_sprint_plan(team: List[Dict[str, Any]], project: Dict[str, Any], balance: Dict[str, Any]) -> Dict[str, Any]:
    """Generate sprint plan using Groq LLM or local tailored fallback."""
    team_roster = "\n".join([f"- {m['name']} ({m.get('assigned_role', m.get('primary_role'))}): {m.get('superpower', '')}" for m in team])
    balance_summary = f"Overall Fit: {balance.get('overall_score')}%. Coverage: {balance.get('coverage_score')}%. Strengths: {', '.join(balance.get('strengths', []))}"

    prompt = SPRINT_PLAN_PROMPT.format(
        project_title=project.get("title", "Hackathon Project"),
        mvp_goal=project.get("mvp_goal", "Working hackathon demo"),
        team_roster=team_roster,
        balance_summary=balance_summary
    )

    result = call_groq_llm(prompt)
    if result and "phases" in result:
        return result

    return heuristic_sprint_plan(team, project)

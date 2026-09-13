"""
Prompt templates for LLM interactions in HackOps.
Enforces strict JSON schemas for structured profile parsing, project analysis, and sprint planning.
"""

PARSE_PROFILE_PROMPT = """
You are an expert technical recruiter and hackathon team builder.
Given the messy bio and information of a hackathon participant, extract a structured JSON profile.

Participant Name: {name}
GitHub URL: {github}
Raw Bio / Info:
{bio}

Return ONLY a valid JSON object matching this schema:
{{
  "name": "Full Name",
  "primary_role": "One of: Frontend Developer, Backend Engineer, AI / ML Engineer, Full-stack Engineer, UI/UX Designer, DevOps Engineer, Product / Pitch Lead",
  "skills": ["List", "of", "top", "skills", "technologies"],
  "experience_level": "beginner | intermediate | advanced",
  "superpower": "A punchy 1-sentence description of their unique hackathon edge",
  "summary": "2-sentence professional bio summary"
}}
"""

ANALYZE_PROJECT_PROMPT = """
You are a senior hackathon mentor and technical architect.
Analyze the following hackathon project pitch and extract its core MVP requirements.

Project Pitch:
{project_idea}

Return ONLY a valid JSON object matching this schema:
{{
  "title": "Short Catchy Project Title",
  "summary": "2-sentence summary of what the project builds",
  "mvp_goal": "Clear 1-sentence definition of what must work for the live 3-minute demo",
  "critical_capabilities": ["List", "of", "4-6", "essential", "capabilities", "e.g.", "AI / LLM", "Frontend UI", "Backend APIs", "Product / Pitch"],
  "required_roles": ["3-4 ideal distinct roles needed on the 4-person squad"],
  "recommended_stack": ["Recommended", "technologies", "for", "fast", "MVP"]
}}
"""

SPRINT_PLAN_PROMPT = """
You are an agile hackathon coach. Create a high-velocity 48-hour sprint execution plan for this 4-person squad.

Project Title: {project_title}
MVP Goal: {mvp_goal}
Squad Roster:
{team_roster}

Team Balance Evaluation:
{balance_summary}

Return ONLY a valid JSON object matching this schema:
{{
  "phases": [
    {{
      "name": "Phase 1: Inception & Architecture",
      "timebox": "Hours 0 – 6",
      "objective": "Lock MVP scope, git repo, schema contracts, and UI wireframes",
      "tasks": [
        {{
          "task": "Task title",
          "owner": "Name of assigned squad member",
          "deliverable": "Specific tangible artifact"
        }}
      ]
    }},
    {{
      "name": "Phase 2: Core MVP Build",
      "timebox": "Hours 6 – 24",
      "objective": "Build core functional logic, AI inference, and connect UI to backend",
      "tasks": [
        {{
          "task": "Task title",
          "owner": "Name of assigned squad member",
          "deliverable": "Specific tangible artifact"
        }}
      ]
    }},
    {{
      "name": "Phase 3: Polish & Edge Cases",
      "timebox": "Hours 24 – 38",
      "objective": "End-to-end integration, bug fixes, visual polish, and backup demo video",
      "tasks": [
        {{
          "task": "Task title",
          "owner": "Name of assigned squad member",
          "deliverable": "Specific tangible artifact"
        }}
      ]
    }},
    {{
      "name": "Phase 4: Pitch & Submission",
      "timebox": "Hours 38 – 48",
      "objective": "3-minute pitch dry runs, Devpost submission, and live judging prep",
      "tasks": [
        {{
          "task": "Task title",
          "owner": "Name of assigned squad member",
          "deliverable": "Specific tangible artifact"
        }}
      ]
    }}
  ],
  "milestones": [
    {{
      "time": "Hour 6",
      "name": "Architecture & Wireframe Lock",
      "deliverable": "Live GitHub repo with boilerplate & approved Figma screen flow"
    }},
    {{
      "time": "Hour 24",
      "name": "End-to-End Alpha MVP",
      "deliverable": "Frontend successfully calling backend AI pipeline"
    }},
    {{
      "time": "Hour 38",
      "name": "Feature Freeze & Video Backup",
      "deliverable": "Stable demo build and recorded 2-minute backup MP4"
    }},
    {{
      "time": "Hour 48",
      "name": "Final Submission",
      "deliverable": "Devpost submitted and live presentation ready"
    }}
  ],
  "demo_checklist": [
    "Verify live demo URL opens in under 2 seconds on incognito browser",
    "Pre-load realistic demo data so judges do not see empty screens",
    "Upload backup 1080p demo video to YouTube (unlisted)",
    "Hook judges in first 20 seconds with clear problem explanation",
    "Public GitHub repo contains comprehensive README with architecture diagram"
  ]
}}
"""

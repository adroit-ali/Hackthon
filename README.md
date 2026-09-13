# 🚀 HackOps — AI Hackathon Squad Matcher & 48-Hour Launchpad

> **Transforming messy hackathon bios and project pitches into balanced 4-person dream teams with instant 48-hour execution roadmaps.**

---

## 🎯 The Problem

Solo hackathon participants waste critical opening hours struggling to find compatible teammates, often ending up in unbalanced groups—like **four backend coders with no UI or pitch lead**—that ultimately fail to deliver a working demo.

## ⚡ Our Solution

An intelligent AI launch platform where:
1. **Leaders** pitch their project ideas and target MVP vision.
2. **Solo Hackers** paste their messy bio or GitHub link, and our NLP engine automatically extracts their primary role, skills, experience level, and superpowers.
3. The **AI Squad Matcher** pairs participants into balanced 4-person squads (1 Leader + 3 distinct roles: Frontend/UI, AI/Backend, and Product/Pitch).
4. The system immediately hands the team an actionable **48-Hour Sprint Roadmap & Kanban Board** with assigned deliverables and a demo-day judge checklist.

---

## 🌟 Key Features

- **💡 Project Pitch Studio**: Create and explore hackathon project briefs with automated capability breakdown (AI/ML, Frontend, Backend, UI/UX, Pitch).
- **👥 Hacker Lounge & NLP Bio Parser**: Real-time parsing of unstructured text and GitHub profiles into structured skills and superpowers.
- **⚡ AI Squad Balancer**: Constraint solver ensuring balanced teams with high synergy, capability coverage scoring (0-100%), and role diversity.
- **⏱ 48-Hour Launchpad**: 4-phase execution plan (Inception 0-6h, Core MVP 6-24h, Polish 24-38h, Pitch & Submission 38-48h).
- **🎤 Demo-Day Checklist & Judge Rubric Alignment**: Step-by-step checklist ensuring teams deliver working live demos and pitch effectively.
- **📥 One-Click Export**: Export full team configurations as JSON or copy sprint roadmaps as Markdown for Discord/Slack.

---

## 🖥️ How to Run the Web Application

### Instant Browser Launch
Simply open `index.html` in any modern web browser:

```bash
# On Windows
start index.html

# On macOS
open index.html

# On Linux
xdg-open index.html
```

---

## 🏗️ Architecture & Project Structure

```text
HackOps/
├── index.html           # Main modern web application interface
├── style.css            # Cyber-dark design system & glassmorphism styling
├── app.js               # Core client-side intelligence, matching & sprint engine
├── app.py               # Streamlit alternative interface
├── mock_data.py         # Default demo projects & participant pool
├── profile_parser.py    # Python Groq LLM profile parser
├── project_analyzer.py  # Python project requirement decomposition
├── vector_store.py      # FAISS semantic vector search engine
├── team_matcher.py      # Python team formation optimizer
├── team_balance.py      # Python capability coverage & diversity scoring
├── sprint_planner.py    # Python 48-hour sprint roadmap generator
└── README.md            # Project documentation
```

---

## 🚀 48-Hour Hackathon Execution Phases

| Phase | Timebox | Focus & Deliverables |
| :--- | :--- | :--- |
| **Phase 1: Inception & Architecture** | Hours 0 – 6 | Lock MVP scope, Git repo, API schemas & Figma wireframes |
| **Phase 2: Core MVP Build** | Hours 6 – 24 | Core AI inference, responsive UI screens & live backend endpoints |
| **Phase 3: Polish & Edge Cases** | Hours 24 – 38 | End-to-end testing, animations, error states & backup demo video |
| **Phase 4: Pitch & Submission** | Hours 38 – 48 | 3-minute pitch rehearsals, Devpost submission & live judging |

---

## 🏆 Judge Rubric Alignment

1. **Innovation & Technical Depth (30%)**: Clear AI value-add and architectural elegance over trivial wrappers.
2. **Working Demo Execution (30%)**: Live user interaction flow without relying on static mock screenshots.
3. **UX & Visual Polish (20%)**: Intuitive glassmorphism interface and responsive feedback loops.
4. **Presentation & Business Impact (20%)**: Memorable 3-minute pitch answering "Why now?" and realistic viability.

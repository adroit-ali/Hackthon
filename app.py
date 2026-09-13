import json
import streamlit as st

from mock_data import MOCK_PARTICIPANTS, MOCK_PROJECT
from profile_parser import parse_participant
from project_analyzer import analyze_project
from vector_store import build_profile_index, search_candidates
from team_matcher import form_team
from team_balance import evaluate_team
from sprint_planner import generate_sprint_plan
from utils import validate_participants

TEAM_SIZE_MEMBERS = 3  # each team = 1 Leader + 3 Members = 4-person squad

st.set_page_config(
    page_title="HackOps — Aurora AI Squad Launchpad",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Aurora UI / Gradient Mesh CSS Injection
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

/* Aurora App Canvas */
.stApp {
    background-color: #070b14;
    background-image: 
        radial-gradient(at 10% 20%, rgba(0, 242, 254, 0.12) 0px, transparent 50%),
        radial-gradient(at 90% 15%, rgba(127, 0, 255, 0.15) 0px, transparent 45%),
        radial-gradient(at 50% 85%, rgba(225, 0, 255, 0.1) 0px, transparent 55%),
        radial-gradient(at 80% 80%, rgba(0, 245, 160, 0.08) 0px, transparent 50%);
    background-attachment: fixed;
}

.block-container {
    max-width: 1240px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

/* Aurora Hero Banner */
.aurora-hero {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.75), rgba(30, 41, 59, 0.65));
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 2.25rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.45);
}

.aurora-hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 25%, #7F00FF 50%, #E100FF 75%, #00F5A0 100%);
}

.aurora-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.95rem;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    background: rgba(0, 242, 254, 0.12);
    color: #67e8f9;
    border: 1px solid rgba(0, 242, 254, 0.3);
    margin-bottom: 0.85rem;
}

.aurora-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -1.2px;
    line-height: 1.15;
    background: linear-gradient(135deg, #FFFFFF 20%, #A5B4FC 60%, #00F2FE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.aurora-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    max-width: 820px;
    line-height: 1.55;
    margin-bottom: 0;
}

/* Stepper Component */
.stepper-wrap {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1rem 1.75rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    border: 1.5px solid rgba(255, 255, 255, 0.15);
    background: rgba(255, 255, 255, 0.04);
    color: #64748b;
    transition: all 0.3s ease;
}

.step-circle.active {
    background: linear-gradient(135deg, #00F2FE, #7F00FF);
    color: #ffffff;
    border-color: #00F2FE;
    box-shadow: 0 0 16px rgba(0, 242, 254, 0.55);
}

.step-circle.done {
    background: #10B981;
    color: #ffffff;
    border-color: #34D399;
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.45);
}

.step-label {
    font-size: 0.82rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.step-label.active {
    color: #f8fafc;
}

.step-line {
    flex: 1;
    height: 2px;
    background: rgba(255, 255, 255, 0.08);
    margin: 0 1.25rem;
    border-radius: 2px;
}

.step-line.done {
    background: linear-gradient(90deg, #10B981, #00F2FE);
}

/* Aurora Glass Cards */
.aurora-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.7), rgba(30, 41, 59, 0.5));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    backdrop-filter: blur(14px);
    margin-bottom: 1rem;
    position: relative;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.aurora-card:hover {
    border-color: rgba(0, 242, 254, 0.3);
    transform: translateY(-2px);
}

.aurora-card.leader {
    border-color: rgba(245, 158, 11, 0.4);
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(15, 23, 42, 0.75) 100%);
}

.aurora-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.aurora-card-meta {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.5;
    margin-top: 0.4rem;
}

/* Badges */
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.22rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}

.badge-leader {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.35);
}

.badge-member {
    background: rgba(99, 102, 241, 0.15);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.35);
}

.badge-skill {
    background: rgba(255, 255, 255, 0.05);
    color: #cbd5e1;
    border: 1px solid rgba(255, 255, 255, 0.08);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
}

/* Score Metrics Box */
.metric-box {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.25rem 1rem;
    text-align: center;
}

.metric-val {
    font-size: 2rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: #00F2FE;
}

.metric-lbl {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    margin-top: 0.25rem;
}

/* Progress bar styling */
.stProgress > div > div > div > div {
    background-image: linear-gradient(90deg, #00F2FE, #7F00FF, #E100FF);
}
</style>
""", unsafe_allow_html=True)


def init_state():
    defaults = {
        "step": 1,
        "participants": [],
        "result": None,
        "analysis_complete": False,
        "use_mock": False,
        "participant_role_choice": "Member",
        "selected_team_idx": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_workflow():
    st.session_state.step = 1
    st.session_state.participants = []
    st.session_state.result = None
    st.session_state.analysis_complete = False
    st.session_state.participant_role_choice = "Member"
    st.session_state.selected_team_idx = 0


def stepper(current):
    steps = [
        ("01", "PITCH & PARTICIPANTS"),
        ("02", "AI MATCH"),
        ("03", "SQUAD BALANCE"),
        ("04", "48H LAUNCH"),
    ]
    html = '<div class="stepper-wrap">'
    for i, (num, label) in enumerate(steps, 1):
        cls = "done" if i < current else ("active" if i == current else "")
        txt = "✓" if i < current else num
        lcls = "active" if i == current else ""
        html += f'<div class="step-item"><div class="step-circle {cls}">{txt}</div><div class="step-label {lcls}">{label}</div></div>'
        if i < len(steps):
            html += f'<div class="step-line {"done" if i < current else ""}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def get_leaders():
    return [p for p in st.session_state.participants if p.get("role") == "leader"]


def get_members():
    return [p for p in st.session_state.participants if p.get("role") != "leader"]


def participant_card(i, p):
    name = p.get("name", "Unnamed")
    bio = p.get("bio", "") or "No bio provided"
    github = p.get("github", "")
    is_leader = p.get("role") == "leader"
    badge_cls = "badge-leader" if is_leader else "badge-member"
    role_badge = f'<span class="badge-pill {badge_cls}">{"👑 Leader" if is_leader else "🙋 Member"}</span>'
    idea = p.get("project_idea", "")
    idea_html = f'<div style="margin-top: 0.4rem; color: #fbbf24; font-size: 0.85rem;"><b>💡 Project Idea:</b> {idea}</div>' if is_leader and idea else ""
    github_html = f'<span style="margin-left: 0.6rem; font-size: 0.8rem; color: #67e8f9;">🔗 {github}</span>' if github else ""

    c1, c2 = st.columns([6, 1])
    with c1:
        card_cls = "aurora-card leader" if is_leader else "aurora-card"
        st.markdown(
            f'''<div class="{card_cls}">
                <div class="aurora-card-title">
                    <span>👤 {name}</span>{role_badge}{github_html}
                </div>
                <div class="aurora-card-meta">{bio}</div>
                {idea_html}
            </div>''',
            unsafe_allow_html=True,
        )
    with c2:
        if st.button("✕ Remove", key=f"remove_{i}", use_container_width=True):
            st.session_state.participants.pop(i)
            st.rerun()


init_state()

# Aurora Header
st.markdown("""
<div class="aurora-hero">
    <div class="aurora-pill">⚡ AI Autonomous Squad Matcher</div>
    <div class="aurora-title">HackOps Launchpad</div>
    <div class="aurora-sub">
        Pair solo hackathon leaders and participants into balanced 4-person squads with complementary skills and instant 48-hour execution roadmaps.
    </div>
</div>
""", unsafe_allow_html=True)

stepper(st.session_state.step)

# Sidebar Controls
with st.sidebar:
    st.markdown("### 🌌 HackOps Studio")
    st.caption("AI-Powered Autonomous Team Formation & 48-Hour Sprint Engine")
    
    mock = st.checkbox("✨ Use Built-in Demo Data", value=st.session_state.use_mock)
    if mock != st.session_state.use_mock:
        st.session_state.use_mock = mock
        if mock:
            demo_participants = [dict(p) for p in MOCK_PARTICIPANTS]
            if demo_participants:
                demo_participants[0]["role"] = "leader"
                demo_participants[0]["project_idea"] = MOCK_PROJECT
                for p in demo_participants[1:]:
                    p.setdefault("role", "member")
            st.session_state.participants = demo_participants
            st.session_state.result = None
            st.session_state.analysis_complete = False
            st.session_state.step = 1
            st.session_state.participant_role_choice = "Member"
            st.session_state.selected_team_idx = 0
            st.rerun()
        else:
            reset_workflow()
            st.rerun()

    st.divider()
    if st.button("↻ Reset Everything", use_container_width=True):
        reset_workflow()
        st.rerun()

    st.markdown("---")
    st.markdown("#### 🏆 Judge Alignment")
    st.caption("• 30% Tech & AI Innovation\n• 30% Live Working Demo\n• 20% UI/UX & Polish\n• 20% Pitch & Narrative")

# STEP 1 — PARTICIPANTS & PITCHES
if st.session_state.step == 1:
    st.markdown("## 01 — Projects & Solo Hacker Pool")
    st.write("Add hackers to the pool. Any hacker can pitch a **Leader Project Idea**, and our system automatically matches them with **3 complementary Members**.")
    
    count = len(st.session_state.participants)
    leaders = get_leaders()
    members = get_members()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total in Pool", count)
    col2.metric("Project Leaders", len(leaders))
    col3.metric("Solo Members", len(members))

    st.markdown("### 💡 Pitched Projects")
    if leaders:
        for leader in leaders:
            st.markdown(
                f'''<div class="aurora-card leader">
                    <div class="aurora-card-title">🚀 {leader.get("project_idea", "")[:120]}...</div>
                    <div class="aurora-card-meta">
                        <span style="color: #fbbf24;">👑 Leader: <b>{leader.get("name", "Unknown")}</b></span> — {leader.get("bio", "")}
                    </div>
                </div>''',
                unsafe_allow_html=True,
            )
    else:
        st.info("No projects yet. Add a **Leader** below with their hackathon project idea.")

    st.divider()
    st.markdown("### ＋ Add Participant / Pitch")
    role_choice = st.radio("Are you pitching a Project or joining as a Member?", ["Member", "Leader"], horizontal=True, key="participant_role_choice")

    with st.form("participant_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name or Handle *", placeholder="e.g. Sara Chen")
        with c2:
            github = st.text_input("GitHub URL (optional)", placeholder="https://github.com/sarachen")
        bio = st.text_area("Messy Bio / Technical Skills *", height=100,
                           placeholder="e.g. Frontend developer who loves React, Next.js, and glassmorphism styling. 2 years experience.")
        idea = ""
        if role_choice == "Leader":
            st.markdown("---")
            idea = st.text_area(
                "Hackathon Project Idea & MVP Vision *", height=120,
                placeholder="Example: Build an AI-powered resume analyzer that scans resumes against job descriptions, identifies skill gaps, and suggests ATS optimizations."
            )
        add = st.form_submit_button("＋ Submit to Pool", type="primary", use_container_width=True)

    if add:
        if not name.strip():
            st.error("Please enter a name.")
        elif not bio.strip() and not github.strip():
            st.error("Please add a bio/skills summary or GitHub URL.")
        elif role_choice == "Leader" and not idea.strip():
            st.error("Please enter the hackathon project idea for the Leader.")
        else:
            participant = {
                "name": name.strip(),
                "bio": bio.strip(),
                "github": github.strip(),
                "role": "leader" if role_choice == "Leader" else "member",
            }
            if role_choice == "Leader":
                participant["project_idea"] = idea.strip()
            st.session_state.participants.append(participant)
            st.success(f"{name.strip()} added successfully.")
            st.rerun()

    st.divider()
    st.markdown("### 👥 Current Participant Pool")
    if not st.session_state.participants:
        st.info("No participants added yet. Add at least one Leader and 3 Members, or click 'Use Built-in Demo Data' in the sidebar.")
    else:
        for i, p in enumerate(st.session_state.participants):
            participant_card(i, p)

    st.divider()
    ready = len(leaders) >= 1 and len(members) >= TEAM_SIZE_MEMBERS
    c1, _ = st.columns([1, 1])
    with c1:
        if st.button("⚡ Continue to AI Matcher →", type="primary", disabled=not ready, use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    if not leaders:
        st.warning("⚠️ Add at least one Leader with a project idea to proceed.")
    elif len(members) < TEAM_SIZE_MEMBERS:
        n = TEAM_SIZE_MEMBERS - len(members)
        st.warning(f"⚠️ Need {n} more Member{'s' if n != 1 else ''} to assemble a 4-person squad.")

# STEP 2 — AI MATCH
elif st.session_state.step == 2:
    st.markdown("## 02 — Autonomous AI Squad Matching")
    st.write(f"The engine decomposes each Leader's project into core MVP pillars, performs FAISS vector search, and enforces complementary role balancing to form balanced 4-person squads.")

    if not st.session_state.analysis_complete:
        st.markdown('''
        <div class="aurora-card">
            <div class="aurora-card-title">🚀 Ready to Assemble Balanced Squads?</div>
            <div class="aurora-card-meta">
                This workflow executes bio parsing, capability breakdown, dense embedding search, complementary role optimization, and 48-hour sprint roadmap generation.
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("⚡ Run AI Squad Matching", type="primary", use_container_width=True):
            stage = "validating participants"
            try:
                participants = st.session_state.participants
                validate_participants(participants)

                progress = st.progress(0)
                status = st.empty()

                stage = "parsing participant profiles"
                status.write("🤖 Parsing messy bios & technical skills...")
                all_profiles = []
                for p in participants:
                    profile = parse_participant(p)
                    profile["role"] = p.get("role", "member")
                    if p.get("role") == "leader":
                        profile["project_idea"] = p.get("project_idea", "")
                    all_profiles.append(profile)
                progress.progress(20)

                leader_profiles = [p for p in all_profiles if p.get("role") == "leader"]
                member_pool = [p for p in all_profiles if p.get("role") != "leader"]

                teams = []
                skipped_projects = []
                total = max(1, len(leader_profiles))
                span = 75 / total

                for li, leader_profile in enumerate(leader_profiles, 1):
                    leader_name = leader_profile.get("name", "the Leader")
                    base = 20 + span * (li - 1)

                    stage = f"analyzing project needs for {leader_name}"
                    status.write(f"🔍 Analyzing project #{li}: {leader_name}'s pitch...")
                    project = analyze_project(leader_profile.get("project_idea", ""))
                    progress.progress(int(base + span * 0.25))

                    if len(member_pool) < TEAM_SIZE_MEMBERS:
                        skipped_projects.append(leader_name)
                        continue

                    stage = f"vectorizing and matching candidates for {leader_name}"
                    status.write(f"⚡ FAISS vector search & role balancing for {leader_name}...")
                    index, indexed_profiles = build_profile_index(member_pool)
                    candidates = search_candidates(index, indexed_profiles, project, top_k=len(indexed_profiles))
                    progress.progress(int(base + span * 0.5))

                    chosen = form_team(candidates, project, team_size=TEAM_SIZE_MEMBERS)
                    chosen_names = {c.get("name") for c in chosen}
                    member_pool = [m for m in member_pool if m.get("name") not in chosen_names]

                    leader_member = dict(leader_profile)
                    leader_member["assigned_role"] = "Team Leader & Architect"
                    leader_member["selection_reason"] = "Project founder — owns vision, core architecture and scope."
                    full_team = [leader_member] + chosen

                    stage = f"evaluating team balance for {leader_name}"
                    balance = evaluate_team(full_team, project)
                    progress.progress(int(base + span * 0.75))

                    stage = f"generating 48-hour sprint roadmap for {leader_name}"
                    sprint = generate_sprint_plan(full_team, project, balance)
                    progress.progress(int(base + span))

                    teams.append({
                        "leader_name": leader_name,
                        "project": project,
                        "team": full_team,
                        "balance": balance,
                        "sprint": sprint,
                    })

                progress.progress(100)
                st.session_state.result = {
                    "teams": teams,
                    "leftover_members": member_pool,
                    "skipped_projects": skipped_projects,
                }
                st.session_state.analysis_complete = True
                st.session_state.selected_team_idx = 0
                status.success("✨ AI squad matching successfully completed!")
                st.rerun()
            except Exception as exc:
                st.error(f"Error while {stage}: {exc}")
    else:
        result = st.session_state.result
        teams = result.get("teams", [])
        leftover = result.get("leftover_members", [])

        if not teams:
            st.warning("No squads could be formed. Add more Members and try again.")
        else:
            st.success(f"✨ Successfully assembled {len(teams)} balanced 4-person squad{'s' if len(teams) != 1 else ''}!")
            for t_idx, t in enumerate(teams):
                leader = t["team"][0]
                squad = t["team"][1:]
                st.markdown(
                    f'''<div class="aurora-card leader">
                        <div class="aurora-card-title">👑 Squad #{t_idx+1}: {t["project"].get("summary", "Project")[:100]}...</div>
                        <div class="aurora-card-meta"><b>Leader:</b> {leader.get("name")} · <b>MVP Goal:</b> {t["project"].get("mvp_goal", "")}</div>
                    </div>''',
                    unsafe_allow_html=True,
                )
                
                cols = st.columns(4)
                for c_idx, member in enumerate(t["team"]):
                    with cols[c_idx]:
                        is_lead = c_idx == 0
                        card_cls = "aurora-card leader" if is_lead else "aurora-card"
                        role_str = member.get("assigned_role") or member.get("primary_role", "Team Member")
                        skills_str = " · ".join(member.get("skills", [])[:4])
                        st.markdown(
                            f'''<div class="{card_cls}" style="min-height: 220px;">
                                <div style="font-size: 0.75rem; color: #64748b; font-weight: 700;">#0{c_idx+1}</div>
                                <div style="font-weight: 800; font-size: 1.1rem; color: #f8fafc; margin-top: 0.2rem;">{member.get("name")}</div>
                                <div style="color: #00F2FE; font-size: 0.82rem; font-weight: 700; margin: 0.3rem 0;">{role_str}</div>
                                <div style="font-size: 0.75rem; color: #94a3b8; line-height: 1.4;">{member.get("selection_reason", "")}</div>
                                <div style="margin-top: 0.5rem; font-size: 0.72rem; color: #67e8f9;">{skills_str}</div>
                            </div>''',
                            unsafe_allow_html=True
                        )
                st.divider()

        if leftover:
            names = ", ".join(m.get("name", "Hacker") for m in leftover)
            st.info(f"💡 **Remaining in pool:** {names} are available to form additional squads.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Re-configure Participants", use_container_width=True):
                st.session_state.analysis_complete = False
                st.session_state.result = None
                st.session_state.step = 1
                st.rerun()
        with c2:
            if st.button("View Squad Balance Scores →", type="primary", use_container_width=True, disabled=not teams):
                st.session_state.step = 3
                st.rerun()

# STEP 3 — TEAM BALANCE
elif st.session_state.step == 3:
    st.markdown("## 03 — Squad Synergy & Balance Analysis")
    st.write("Understand your 4-person squad's capability coverage, role diversity, key strengths, and gap mitigations.")
    
    teams = (st.session_state.result or {}).get("teams", [])
    if not teams:
        st.warning("Please build teams first.")
        if st.button("← Back to AI Matcher"): st.session_state.step = 2; st.rerun()
    else:
        if len(teams) > 1:
            idx = st.selectbox(
                "Select a Squad",
                options=list(range(len(teams))),
                index=min(st.session_state.selected_team_idx, len(teams) - 1),
                format_func=lambda i: f"👑 Squad #{i+1}: {teams[i]['leader_name']}'s Project",
            )
            st.session_state.selected_team_idx = idx
        else:
            idx = 0
        
        t = teams[idx]
        balance = t["balance"]
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'''<div class="metric-box">
                <div class="metric-val">{balance.get("overall_score", 0):.0f}/100</div>
                <div class="metric-lbl">Overall Squad Fit</div>
            </div>''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''<div class="metric-box">
                <div class="metric-val" style="color: #10B981;">{balance.get("coverage_score", 0):.0f}%</div>
                <div class="metric-lbl">Capability Coverage</div>
            </div>''', unsafe_allow_html=True)
        with c3:
            st.markdown(f'''<div class="metric-box">
                <div class="metric-val" style="color: #7F00FF;">{balance.get("role_diversity_score", 0):.0f}%</div>
                <div class="metric-lbl">Role Diversity</div>
            </div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns(2)
        with left:
            st.markdown("### ✅ Key Strengths")
            for s in balance.get("strengths", []) or ["Balanced multi-disciplinary team representation."]:
                st.success(f"• {s}")
        with right:
            st.markdown("### ⚠️ Gap Mitigations")
            gaps = balance.get("gaps", [])
            if gaps:
                for g in gaps:
                    st.warning(f"• Consider pre-built templates or third-party tools for: {g}")
            else:
                st.success("✨ Zero major capability gaps detected across all MVP requirements!")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Back to AI Matcher", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        with c2:
            if st.button("⚡ Open 48-Hour Launchpad →", type="primary", use_container_width=True):
                st.session_state.step = 4
                st.rerun()

# STEP 4 — LAUNCHPAD
else:
    st.markdown("## 04 — 48-Hour Launchpad & Sprint Engine")
    st.write("A customized 4-phase execution roadmap with individual task owners, milestone deliverables, and demo-day verification.")

    teams = (st.session_state.result or {}).get("teams", [])
    if not teams:
        st.warning("Please build teams first.")
    else:
        if len(teams) > 1:
            idx = st.selectbox(
                "Select a Squad",
                options=list(range(len(teams))),
                index=min(st.session_state.selected_team_idx, len(teams) - 1),
                format_func=lambda i: f"👑 Squad #{i+1}: {teams[i]['leader_name']}'s Project",
                key="launch_team_select",
            )
            st.session_state.selected_team_idx = idx
        else:
            idx = 0
        
        t = teams[idx]
        project, sprint = t["project"], t["sprint"]

        st.markdown(f'''
        <div class="aurora-card leader">
            <div class="aurora-card-title">🚀 {project.get("summary", "Hackathon Project")}</div>
            <div class="aurora-card-meta"><b>MVP Goal:</b> {project.get("mvp_goal", "Not specified")}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown("### ⏱ 4-Phase Sprint Roadmap")
        for phase in sprint.get("phases", []) or []:
            title = phase.get("title", phase.get("name", "Phase"))
            timebox = phase.get("timebox", phase.get("time_window", ""))
            with st.expander(f"📌 {title} — {timebox}", expanded=True):
                if phase.get("objective") or phase.get("goal"):
                    st.caption(f"**Goal:** {phase.get('objective') or phase.get('goal')}")
                for task in phase.get("tasks", []) or []:
                    if isinstance(task, dict):
                        owner_badge = f" `👤 {task.get('owner', 'Team')}`" if task.get('owner') else ""
                        deliv = f"<br><span style='color: #64748b; font-size: 0.8rem;'>🎯 Deliverable: {task.get('deliverable')}</span>" if task.get("deliverable") else ""
                        st.markdown(f"- **{task.get('task', 'Task')}**{owner_badge}{deliv}", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {task}")

        st.divider()
        st.markdown("### 🎤 Demo-Day Submission Checklist")
        for i, item in enumerate(sprint.get("demo_checklist", []) or []):
            st.checkbox(str(item), key=f"demo_cb_{idx}_{i}", value=True if i < 2 else False)

        st.markdown("<br>", unsafe_allow_html=True)
        raw_export = {"project": project, "team": t["team"], "balance": t["balance"], "sprint": sprint}
        st.download_button(
            "📥 Download Full Squad JSON Plan",
            json.dumps(raw_export, indent=2, ensure_ascii=False),
            f"hackops_squad_{t['leader_name']}.json",
            "application/json",
            use_container_width=True,
            type="primary"
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Back to Balance Scores", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
        with c2:
            if st.button("↻ Pitch New Project", use_container_width=True):
                reset_workflow()
                st.rerun()

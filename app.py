import json
import streamlit as st

from storage import (
    load_storage,
    add_participant_to_storage,
    remove_participant_from_storage,
    save_result_to_storage,
    reset_storage
)
from profile_parser import parse_participant
from project_analyzer import analyze_project
from vector_store import build_profile_index, search_candidates
from team_matcher import form_team
from team_balance import evaluate_team
from sprint_planner import generate_sprint_plan
from utils import validate_participants

TEAM_SIZE_MEMBERS = 3  # each team = 1 Leader + 3 Members = 4-person squad

st.set_page_config(
    page_title="HackOps — Minimalist AI Launchpad",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Minimalist Light Mode CSS Injection
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: #0F172A;
}

/* Light Background Canvas */
.stApp {
    background-color: #F8FAFC;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.75rem;
    padding-bottom: 4rem;
}

/* Minimalist Hero Header */
.minimal-hero {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.minimal-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    background: #F1F5F9;
    color: #334155;
    border: 1px solid #E2E8F0;
    margin-bottom: 0.6rem;
}

.live-pulse {
    display: inline-block;
    width: 7px;
    height: 7px;
    background-color: #10B981;
    border-radius: 50%;
}

.minimal-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.8px;
    line-height: 1.2;
    color: #0F172A;
    margin-bottom: 0.35rem;
}

.minimal-sub {
    color: #475467;
    font-size: 0.95rem;
    max-width: 780px;
    line-height: 1.5;
    margin-bottom: 0;
}

/* Minimalist Stepper */
.stepper-wrap {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.85rem 1.5rem;
    margin-bottom: 1.75rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.step-item {
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.step-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.78rem;
    border: 1.5px solid #CBD5E1;
    background: #F8FAFC;
    color: #64748B;
    transition: all 0.2s ease;
}

.step-circle.active {
    background: #0F172A;
    color: #FFFFFF;
    border-color: #0F172A;
}

.step-circle.done {
    background: #10B981;
    color: #FFFFFF;
    border-color: #10B981;
}

.step-label {
    font-size: 0.76rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.step-label.active {
    color: #0F172A;
}

.step-line {
    flex: 1;
    height: 1.5px;
    background: #E2E8F0;
    margin: 0 1rem;
}

.step-line.done {
    background: #10B981;
}

/* Minimalist Cards */
.minimal-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.15rem 1.35rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.minimal-card:hover {
    border-color: #CBD5E1;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
}

.minimal-card.leader {
    border: 1.5px solid #FCD34D;
    background: #FFFDF5;
}

.minimal-card-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: #0F172A;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.minimal-card-meta {
    font-size: 0.86rem;
    color: #475467;
    line-height: 1.45;
    margin-top: 0.35rem;
}

/* Minimal Badges */
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.15rem 0.55rem;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
}

.badge-leader {
    background: #FEF3C7;
    color: #92400E;
    border: 1px solid #FDE68A;
}

.badge-member {
    background: #EFF6FF;
    color: #1E40AF;
    border: 1px solid #DBEAFE;
}

.badge-skill {
    background: #F1F5F9;
    color: #334155;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    border-radius: 6px;
    padding: 0.15rem 0.5rem;
}

/* Minimal Metric Box */
.metric-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.15rem 1rem;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.metric-val {
    font-size: 1.85rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: #0F172A;
}

.metric-lbl {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-top: 0.2rem;
}

/* Form Styles */
div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.35rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

/* Clean Button Styling */
button[kind="primary"] {
    background-color: #0F172A !important;
    color: #FFFFFF !important;
    border-color: #0F172A !important;
    border-radius: 8px !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #334155 !important;
    border-color: #E2E8F0 !important;
    border-radius: 8px !important;
}
</style>""", unsafe_allow_html=True)


def init_session():
    """Ensure local session variables exist."""
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "selected_team_idx" not in st.session_state:
        st.session_state.selected_team_idx = 0
    if "participant_role_choice" not in st.session_state:
        st.session_state.participant_role_choice = "Member"


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


def participant_card(i, p):
    name = p.get("name", "Unnamed")
    bio = p.get("bio", "") or "No bio provided"
    github = p.get("github", "")
    is_leader = p.get("role") == "leader"
    badge_cls = "badge-leader" if is_leader else "badge-member"
    role_badge = f'<span class="badge-pill {badge_cls}">{"👑 Leader" if is_leader else "🙋 Member"}</span>'
    idea = p.get("project_idea", "")
    idea_html = f'<div style="margin-top:0.4rem;color:#B45309;font-size:0.85rem;font-weight:500;"><b>💡 Project Idea:</b> {idea}</div>' if is_leader and idea else ""
    github_html = f'<span style="margin-left:0.6rem;font-size:0.8rem;color:#0284C7;">🔗 {github}</span>' if github else ""

    c1, c2 = st.columns([6, 1])
    with c1:
        card_cls = "minimal-card leader" if is_leader else "minimal-card"
        html_card = (
            f'<div class="{card_cls}">'
            f'<div class="minimal-card-title"><span>👤 {name}</span>{role_badge}{github_html}</div>'
            f'<div class="minimal-card-meta">{bio}</div>'
            f'{idea_html}'
            f'</div>'
        )
        st.markdown(html_card, unsafe_allow_html=True)
    with c2:
        if st.button("✕ Remove", key=f"remove_btn_{i}_{name}", use_container_width=True):
            remove_participant_from_storage(i)
            st.rerun()


init_session()

# Minimalist Header with Live Pulse Indicator
st.markdown(
    '<div class="minimal-hero">'
    '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">'
    '<div class="minimal-pill"><span class="live-pulse"></span><span>Live Multi-User Sync</span></div>'
    '<div style="font-size:0.75rem;color:#64748B;font-family:\'JetBrains Mono\',monospace;">Auto-refresh active · All changes sync in real-time</div>'
    '</div>'
    '<div class="minimal-title">HackOps Launchpad</div>'
    '<div class="minimal-sub">Pair solo hackathon leaders and participants into balanced 4-person squads with complementary skillsets and instant 48-hour execution plans.</div>'
    '</div>',
    unsafe_allow_html=True
)

stepper(st.session_state.step)

# Sidebar Controls
with st.sidebar:
    st.markdown("### 🚀 HackOps")
    st.caption("Minimalist AI Hackathon Team Builder")
    
    st.markdown("💾 **Storage:** Persistent JSON")
    st.caption("Participant pool and project matches are saved in real-time.")

    st.divider()
    if st.button("↻ Reset to Initial Seed", use_container_width=True):
        reset_storage()
        st.session_state.step = 1
        st.session_state.selected_team_idx = 0
        st.rerun()

    st.markdown("---")
    st.markdown("#### 🏆 Judge Rubric Alignment")
    st.caption("• 30% Tech & AI Depth\n• 30% Live Working Demo\n• 20% UX & Polish\n• 20% Pitch & Storytelling")


# Auto-refreshing Live Fragment for Participants & Projects Display
@st.fragment(run_every="2s")
def render_live_participants_view():
    """Live fragment that auto-polls persistent storage every 2 seconds without reloading the page."""
    storage_data = load_storage()
    participants = storage_data.get("participants", [])
    leaders = [p for p in participants if p.get("role") == "leader"]
    members = [p for p in participants if p.get("role") != "leader"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total in Pool", len(participants))
    col2.metric("Project Leaders", len(leaders))
    col3.metric("Solo Members", len(members))

    st.markdown("### 💡 Pitched Projects")
    if leaders:
        for leader in leaders:
            card_html = (
                f'<div class="minimal-card leader">'
                f'<div class="minimal-card-title">🚀 {leader.get("project_idea", "")[:120]}...</div>'
                f'<div class="minimal-card-meta"><span style="color:#B45309;">👑 Leader: <b>{leader.get("name", "Unknown")}</b></span> — {leader.get("bio", "")}</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("No projects yet. Add a **Leader** below with their hackathon project idea.")

    st.markdown("### 👥 Stored Participant Pool")
    if not participants:
        st.info("No participants stored. Add a Leader and Members below.")
    else:
        for i, p in enumerate(participants):
            participant_card(i, p)


# STEP 1 — PARTICIPANTS & PITCHES
if st.session_state.step == 1:
    st.markdown("## 01 — Projects & Solo Hacker Pool")
    st.write("Add hackers to the shared live pool. Any participant can pitch a **Leader Project Idea**, and our system automatically matches them with **3 complementary Members**.")
    
    # Render the auto-updating live view
    render_live_participants_view()

    st.divider()
    st.markdown("### ＋ Add Participant / Pitch")
    role_choice = st.radio("Are you pitching a Project or joining as a Member?", ["Member", "Leader"], horizontal=True, key="participant_role_choice")

    with st.form("participant_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name or Handle *", placeholder="e.g. Sara Chen")
        with c2:
            github = st.text_input("GitHub URL (optional)", placeholder="https://github.com/sarachen")
        bio = st.text_area("Messy Bio / Technical Skills *", height=90,
                           placeholder="e.g. Frontend developer who loves React, Next.js, and clean UI design. 2 years experience.")
        idea = ""
        if role_choice == "Leader":
            st.markdown("---")
            idea = st.text_area(
                "Hackathon Project Idea & MVP Vision *", height=110,
                placeholder="Example: Build an AI-powered resume analyzer that scans resumes against job descriptions, identifies skill gaps, and suggests ATS optimizations."
            )
        add = st.form_submit_button("＋ Submit to Live Pool", type="primary", use_container_width=True)

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
            add_participant_to_storage(participant)
            st.success(f"✨ {name.strip()} added successfully.")
            st.rerun()

    st.divider()
    curr_data = load_storage()
    curr_participants = curr_data.get("participants", [])
    curr_leaders = [p for p in curr_participants if p.get("role") == "leader"]
    curr_members = [p for p in curr_participants if p.get("role") != "leader"]

    ready = len(curr_leaders) >= 1 and len(curr_members) >= TEAM_SIZE_MEMBERS
    c1, _ = st.columns([1, 1])
    with c1:
        if st.button("⚡ Continue to AI Matcher →", type="primary", disabled=not ready, use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    if not curr_leaders:
        st.warning("⚠️ Add at least one Leader with a project idea to proceed.")
    elif len(curr_members) < TEAM_SIZE_MEMBERS:
        n = TEAM_SIZE_MEMBERS - len(curr_members)
        st.warning(f"⚠️ Need {n} more Member{'s' if n != 1 else ''} to assemble a 4-person squad.")

# STEP 2 — AI MATCH
elif st.session_state.step == 2:
    st.markdown("## 02 — Autonomous AI Squad Matching")
    st.write("The engine decomposes each Leader's project into core MVP pillars, performs FAISS vector search, and enforces complementary role balancing to form balanced 4-person squads.")

    stored_data = load_storage()
    saved_result = stored_data.get("result")

    if not saved_result:
        st.markdown(
            '<div class="minimal-card">'
            '<div class="minimal-card-title">🚀 Ready to Assemble Balanced Squads?</div>'
            '<div class="minimal-card-meta">This workflow executes bio parsing, capability breakdown, dense embedding search, complementary role optimization, and 48-hour sprint roadmap generation.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        
        if st.button("⚡ Run AI Squad Matching", type="primary", use_container_width=True):
            stage = "validating participants"
            try:
                participants = stored_data.get("participants", [])
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
                result_payload = {
                    "teams": teams,
                    "leftover_members": member_pool,
                    "skipped_projects": skipped_projects,
                }
                save_result_to_storage(result_payload, step=2)
                status.success("✨ AI squad matching successfully completed!")
                st.rerun()
            except Exception as exc:
                st.error(f"Error while {stage}: {exc}")
    else:
        teams = saved_result.get("teams", [])
        leftover = saved_result.get("leftover_members", [])

        if not teams:
            st.warning("No squads could be formed. Add more Members and try again.")
        else:
            st.success(f"✨ Successfully assembled {len(teams)} balanced 4-person squad{'s' if len(teams) != 1 else ''}!")
            for t_idx, t in enumerate(teams):
                leader = t["team"][0]
                squad_header = (
                    f'<div class="minimal-card leader">'
                    f'<div class="minimal-card-title">👑 Squad #{t_idx+1}: {t["project"].get("summary", "Project")[:100]}...</div>'
                    f'<div class="minimal-card-meta"><b>Leader:</b> {leader.get("name")} · <b>MVP Goal:</b> {t["project"].get("mvp_goal", "")}</div>'
                    f'</div>'
                )
                st.markdown(squad_header, unsafe_allow_html=True)
                
                cols = st.columns(4)
                for c_idx, member in enumerate(t["team"]):
                    with cols[c_idx]:
                        is_lead = c_idx == 0
                        card_cls = "minimal-card leader" if is_lead else "minimal-card"
                        role_str = member.get("assigned_role") or member.get("primary_role", "Team Member")
                        skills_str = " · ".join(member.get("skills", [])[:4])
                        member_html = (
                            f'<div class="{card_cls}" style="min-height:200px;">'
                            f'<div style="font-size:0.75rem;color:#64748B;font-weight:700;">#0{c_idx+1}</div>'
                            f'<div style="font-weight:800;font-size:1.05rem;color:#0F172A;margin-top:0.2rem;">{member.get("name")}</div>'
                            f'<div style="color:#0284C7;font-size:0.8rem;font-weight:700;margin:0.25rem 0;">{role_str}</div>'
                            f'<div style="font-size:0.75rem;color:#475467;line-height:1.4;">{member.get("selection_reason", "")}</div>'
                            f'<div style="margin-top:0.5rem;font-size:0.72rem;color:#0284C7;">{skills_str}</div>'
                            f'</div>'
                        )
                        st.markdown(member_html, unsafe_allow_html=True)
                st.divider()

        if leftover:
            names = ", ".join(m.get("name", "Hacker") for m in leftover)
            st.info(f"💡 **Remaining in pool:** {names} are available to form additional squads.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Re-configure Participants", use_container_width=True):
                save_result_to_storage(None, step=1)
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
    
    stored_data = load_storage()
    saved_result = stored_data.get("result") or {}
    teams = saved_result.get("teams", [])

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
            m1_html = f'<div class="metric-box"><div class="metric-val">{balance.get("overall_score", 0):.0f}/100</div><div class="metric-lbl">Overall Squad Fit</div></div>'
            st.markdown(m1_html, unsafe_allow_html=True)
        with c2:
            m2_html = f'<div class="metric-box"><div class="metric-val" style="color:#10B981;">{balance.get("coverage_score", 0):.0f}%</div><div class="metric-lbl">Capability Coverage</div></div>'
            st.markdown(m2_html, unsafe_allow_html=True)
        with c3:
            m3_html = f'<div class="metric-box"><div class="metric-val" style="color:#6366F1;">{balance.get("role_diversity_score", 0):.0f}%</div><div class="metric-lbl">Role Diversity</div></div>'
            st.markdown(m3_html, unsafe_allow_html=True)

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

    stored_data = load_storage()
    saved_result = stored_data.get("result") or {}
    teams = saved_result.get("teams", [])

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

        proj_header = (
            f'<div class="minimal-card leader">'
            f'<div class="minimal-card-title">🚀 {project.get("summary", "Hackathon Project")}</div>'
            f'<div class="minimal-card-meta"><b>MVP Goal:</b> {project.get("mvp_goal", "Not specified")}</div>'
            f'</div>'
        )
        st.markdown(proj_header, unsafe_allow_html=True)

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
                        deliv = f"<br><span style='color:#64748B;font-size:0.8rem;'>🎯 Deliverable: {task.get('deliverable')}</span>" if task.get("deliverable") else ""
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
                save_result_to_storage(None, step=1)
                st.session_state.step = 1
                st.rerun()

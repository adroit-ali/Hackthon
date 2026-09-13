# 🚀 HackOps — Minimalist AI Squad Launchpad (Light Mode)

> **An AI launch tool where hackers simply paste their messy bio or GitHub link, and the system automatically pairs them into a balanced 4-person squad matched to a project idea—then immediately hands them a complete 48-hour plan to build it.**

---

## 🎯 The Problem

Solo hackathon participants waste critical opening hours struggling to find compatible teammates, often ending up in unbalanced groups—like **four backend coders with no UI or pitch lead**—that ultimately fail to deliver a working demo.

## ⚡ Our Solution

An intelligent AI launch platform designed with a clean **Minimalist Light Mode UI**:
1. **Persistent Real-Time Sync**: Automatically seeds default hackathon participants once and persists all participant additions, deletions, and match states across concurrent users in real time.
2. **Parses Messy Bios**: Extracts structured roles, technical skills, experience level, and superpowers from natural language descriptions or GitHub profiles.
3. **Analyzes Project Needs**: Decomposes submitted hackathon ideas into essential technical and operational capabilities required for a working MVP.
4. **Vectorizes & Indexes Profiles**: Converts participant profiles into dense semantic embeddings and stores them in a local FAISS index for similarity retrieval.
5. **Balances the 4-Person Squad**: Combines vector retrieval with complementary role-filtering logic (1 Leader + 3 distinct functional roles) to prevent overlapping stacks.
6. **Evaluates Team Coverage**: Analyzes collective capability coverage (0–100%), role diversity (0–100%), highlights gaps, and calculates an overall team-fit score.
7. **Generates a 48-Hour Sprint Roadmap**: Produces a time-boxed execution schedule with individual task ownership, milestone deliverables, and a demo-day preparation checklist.

---

## 🏗️ Architecture & Project Structure

```text
HackOps/
├── .streamlit/
│   └── config.toml          # Streamlit theme (Minimalist light mode)
├── data/
│   └── hackops_storage.json # Persistent JSON data store (pre-seeded automatically)
├── .env.example             # Environment variable template (GROQ_API_KEY)
├── .gitignore               # Python and environment ignores
├── requirements.txt         # Minimal, high-compatibility dependencies
├── storage.py               # Real-time JSON persistence & live sync engine
├── prompts.py               # Prompt templates for profile parsing, analysis & sprint plans
├── profile_parser.py        # Messy bio extraction (Groq + local heuristic fallback)
├── project_analyzer.py      # Project requirement & capability decomposition
├── vector_store.py          # Sentence embeddings & FAISS semantic vector search
├── team_matcher.py          # Complementary 4-person squad optimization solver
├── team_balance.py          # Capability coverage, role diversity & gap scoring
├── sprint_planner.py        # 48-hour timeboxed roadmap & demo checklist generator
├── mock_data.py             # Preloaded hackathon projects & varied candidate pool
├── utils.py                 # Input validation, profile sanitation & JSON helpers
├── app.py                   # Main Streamlit app with Minimalist Light Mode
└── README.md                # Project documentation
```

---

## 🚀 Setup & Local Execution

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Groq API Key (Optional)

Copy `.env.example` to `.env` and add your Groq API key (if omitted, HackOps will run smoothly using its built-in local inference engine):

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Streamlit Application

```bash
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push this repository to your GitHub account:
   ```bash
   git add .
   git commit -m "feat: HackOps Minimalist Light Mode AI Launchpad"
   git push origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and create a **New app**.
3. Select your repository and set `app.py` as the **Main file path**.
4. Click **Deploy!**

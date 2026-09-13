/**
 * HackOps - AI Squad & 48-Hour Launchpad
 * Modern, high-performance team matcher and sprint execution engine
 */

// Initial State and Mock Data
const DEFAULT_PROJECTS = [
  {
    id: "proj-1",
    title: "AI Resume & ATS Copilot",
    summary: "Build an AI-powered resume assistant for job seekers that analyzes resume PDFs against job descriptions, identifies skill gaps, optimizes ATS keywords, and provides an instant compatibility score with personalized interview talking points.",
    mvpGoal: "Working Streamlit/React web demo where users upload a resume, paste a JD, and receive instant AI analysis with exportable ATS improvements.",
    track: "AI / Productivity",
    leaderName: "Ali Raza",
    leaderBio: "CS student focused on Python, machine learning, LLM applications and FastAPI. I like working on the AI backend and prompt engineering.",
    leaderGithub: "https://github.com/aliraza-ai",
    capabilities: ["AI / LLM", "Backend APIs", "Frontend UI", "Product / Pitch"],
    requiredRoles: ["AI / ML Engineer", "Frontend Developer", "Backend Engineer", "Product / Pitch Lead"]
  },
  {
    id: "proj-2",
    title: "EcoPulse - Satellite Carbon Tracker",
    summary: "A decentralized real-time deforestation and carbon credit verification platform utilizing Copernicus satellite imagery and smart contracts for transparent corporate climate pledges.",
    mvpGoal: "Interactive map visualization showing forest loss heatmaps alongside mock on-chain carbon offset attestations.",
    track: "Climate & Web3",
    leaderName: "Zara Khan",
    leaderBio: "Full-stack developer with React, Node.js and geospatial mapping experience. I enjoy building visual web apps.",
    leaderGithub: "https://github.com/zarakhan-dev",
    capabilities: ["Geospatial / Data", "Frontend UI", "Smart Contracts", "Product / Pitch"],
    requiredRoles: ["Frontend Developer", "Data Scientist", "Backend / Web3", "UI/UX Designer"]
  },
  {
    id: "proj-3",
    title: "MedVoice Triage Copilot",
    summary: "An ambient emergency voice agent that listens to 911/ER calls, transcribes medical symptoms in real-time, highlights high-risk triage flags, and automatically drafts patient intake charts.",
    mvpGoal: "Live microphone streaming dashboard that detects vital symptoms, categorizes urgency (Red/Yellow/Green), and prepares clinical handoff notes.",
    track: "HealthTech & Audio AI",
    leaderName: "Ahmed Farooq",
    leaderBio: "Backend engineer comfortable with Python, FastAPI, WebSockets and audio streaming. Built real-time APIs.",
    leaderGithub: "https://github.com/ahmed-backend",
    capabilities: ["Audio / NLP", "Real-time APIs", "Clinical UI/UX", "Demo Pitch"],
    requiredRoles: ["Backend / Realtime", "AI / Speech", "Frontend Engineer", "UI/UX & Pitch"]
  }
];

const DEFAULT_MEMBERS = [
  {
    id: "mem-1",
    name: "Sara Chen",
    bio: "Frontend developer who loves React, Tailwind, Next.js and responsive glassmorphism interfaces. Built multiple hackathon-winning UIs and enjoy rapid prototyping.",
    github: "https://github.com/sarachen-ui",
    role: "member",
    primaryRole: "Frontend Developer",
    skills: ["React", "Next.js", "TypeScript", "Tailwind CSS", "UI/UX", "Figma"],
    experienceLevel: "advanced",
    superpower: "Pixel-perfect fast UI builds & micro-interactions"
  },
  {
    id: "mem-2",
    name: "Hina Malik",
    bio: "Product designer and UI/UX strategist with Figma expertise. Can create user journeys, wireframes, and high-converting presentation slide decks for judges.",
    github: "https://github.com/hinamalik",
    role: "member",
    primaryRole: "UI/UX & Pitch Lead",
    skills: ["Figma", "UI/UX Design", "Pitch Deck", "Product Strategy", "Storytelling", "User Research"],
    experienceLevel: "advanced",
    superpower: "Compelling pitch narratives & sleek judge demos"
  },
  {
    id: "mem-3",
    name: "Hamza Tariq",
    bio: "DevOps and cloud engineer. Comfortable with Docker, GitHub Actions, FastAPI, Redis, and deploying scalable MVPs within minutes on cloud platforms.",
    github: "https://github.com/hamzatariq-ops",
    role: "member",
    primaryRole: "DevOps & Cloud Engineer",
    skills: ["Docker", "FastAPI", "Python", "Cloud Hosting", "CI/CD", "Redis"],
    experienceLevel: "intermediate",
    superpower: "Zero-friction live deployment & reliable backend uptime"
  },
  {
    id: "mem-4",
    name: "Usman Ghani",
    bio: "Data science and ML student with Python, pandas, scikit-learn, LangChain, and vector embeddings. Experienced in cleaning messy data and building RAG pipelines.",
    github: "https://github.com/usman-data",
    role: "member",
    primaryRole: "AI / Data Scientist",
    skills: ["Python", "Machine Learning", "LangChain", "Vector DBs", "Pandas", "NLP"],
    experienceLevel: "intermediate",
    superpower: "RAG architectures & semantic search indexing"
  },
  {
    id: "mem-5",
    name: "Ayesha Noor",
    bio: "Technical writer and product evangelist. Skilled in creating interactive demo scripts, API docs, system architecture diagrams, and clear value props for non-technical judges.",
    github: "https://github.com/ayeshanoor",
    role: "member",
    primaryRole: "Product & Presentation Lead",
    skills: ["Product Management", "Technical Writing", "Presentation", "Demo Scripts", "System Diagrams"],
    experienceLevel: "intermediate",
    superpower: "Clarifying complex tech into winning 3-minute pitches"
  },
  {
    id: "mem-6",
    name: "Bilal Hassan",
    bio: "Full-stack engineer with React, Node.js, PostgreSQL, WebSockets and REST APIs. Love connecting complex frontends with secure backend logic.",
    github: "https://github.com/bilalhassan",
    role: "member",
    primaryRole: "Full-stack Engineer",
    skills: ["React", "Node.js", "PostgreSQL", "WebSockets", "REST APIs", "TypeScript"],
    experienceLevel: "advanced",
    superpower: "End-to-end full-stack feature delivery under pressure"
  },
  {
    id: "mem-7",
    name: "Fatima Zahra",
    bio: "Mobile and Frontend specialist. Experience with React Native, modern CSS animations, state management, and creating snappy mobile-first interfaces.",
    github: "https://github.com/fatimazahra",
    role: "member",
    primaryRole: "Frontend Developer",
    skills: ["React", "React Native", "CSS Animations", "Redux", "Responsive Design"],
    experienceLevel: "intermediate",
    superpower: "Snappy mobile-first responsiveness"
  },
  {
    id: "mem-8",
    name: "Daniyal Shah",
    bio: "Backend and AI specialist. Familiar with PyTorch, Groq APIs, Ollama, vector search, and high-concurrency microservices in Go and Python.",
    github: "https://github.com/daniyalshah",
    role: "member",
    primaryRole: "AI / Backend Engineer",
    skills: ["Python", "Go", "LLM APIs", "FAISS", "Vector DBs", "Docker"],
    experienceLevel: "advanced",
    superpower: "Ultra-fast LLM API pipelines and structured data extraction"
  }
];

// App State
let state = {
  currentTab: "projects",
  projects: JSON.parse(localStorage.getItem("hackops_projects")) || DEFAULT_PROJECTS,
  participants: JSON.parse(localStorage.getItem("hackops_members")) || DEFAULT_MEMBERS,
  matchedSquads: JSON.parse(localStorage.getItem("hackops_squads")) || [],
  selectedSquadIdx: 0,
  apiKey: localStorage.getItem("hackops_groq_key") || "",
  kanbanState: {}
};

// Skill Taxonomy & Keywords Dictionary
const SKILL_KEYWORDS = {
  "AI / Machine Learning": ["ai", "machine learning", "ml", "llm", "langchain", "prompt", "nlp", "pytorch", "tensorflow", "openai", "groq", "transformers", "vector", "embeddings", "rag", "huggingface"],
  "Frontend Development": ["frontend", "react", "next.js", "vue", "javascript", "typescript", "tailwind", "html", "css", "svelte", "ui", "responsive", "web", "dom"],
  "Backend & APIs": ["backend", "python", "fastapi", "flask", "node", "node.js", "express", "django", "rest", "api", "graphql", "sql", "postgresql", "mongodb", "database", "orm"],
  "UI/UX & Design": ["ui/ux", "figma", "wireframe", "prototype", "design", "user flow", "user research", "product design", "adobe", "canva", "mockup"],
  "Cloud & DevOps": ["docker", "kubernetes", "cloud", "aws", "gcp", "azure", "ci/cd", "git", "linux", "deployment", "server", "devops", "redis"],
  "Product & Pitch": ["pitch", "presentation", "demo", "storytelling", "product management", "technical writer", "research", "business", "deck", "judge"]
};

// Heuristic Profile Parser
function parseRawBio(name, rawBio, githubUrl = "") {
  const clean = (rawBio + " " + githubUrl).toLowerCase();
  const detectedSkills = [];
  const roleScores = {
    "Frontend Developer": 0,
    "Backend Engineer": 0,
    "AI / ML Engineer": 0,
    "UI/UX Designer": 0,
    "DevOps Engineer": 0,
    "Product / Pitch Lead": 0
  };

  // Scan skills
  for (const [category, keywords] of Object.entries(SKILL_KEYWORDS)) {
    keywords.forEach(kw => {
      const regex = new RegExp(`\\b${kw.replace(".", "\\.")}\\b`, "i");
      if (regex.test(clean)) {
        if (!detectedSkills.includes(kw)) {
          detectedSkills.push(kw.charAt(0).toUpperCase() + kw.slice(1));
        }
        if (category.includes("AI")) roleScores["AI / ML Engineer"] += 2;
        if (category.includes("Frontend")) roleScores["Frontend Developer"] += 2;
        if (category.includes("Backend")) roleScores["Backend Engineer"] += 2;
        if (category.includes("Design")) roleScores["UI/UX Designer"] += 2;
        if (category.includes("Cloud")) roleScores["DevOps Engineer"] += 2;
        if (category.includes("Product")) roleScores["Product / Pitch Lead"] += 2;
      }
    });
  }

  // Determine top role
  let bestRole = "Full-stack Developer";
  let maxScore = 0;
  for (const [r, score] of Object.entries(roleScores)) {
    if (score > maxScore) {
      maxScore = score;
      bestRole = r;
    }
  }

  // Determine Experience Level
  let exp = "intermediate";
  if (/senior|lead|years|advanced|architect|expert/i.test(clean)) {
    exp = "advanced";
  } else if (/student|beginner|junior|learner|learning|new to/i.test(clean)) {
    exp = "beginner";
  }

  // Superpower summary
  let superpower = "Cross-functional feature implementation";
  if (bestRole.includes("Frontend")) superpower = "Snappy UI layouts and smooth component rendering";
  else if (bestRole.includes("AI")) superpower = "Model inference, prompt engineering and RAG pipelines";
  else if (bestRole.includes("Backend")) superpower = "Scalable API design and reliable data contracts";
  else if (bestRole.includes("Design")) superpower = "High-polish visual wireframing & presentation decks";
  else if (bestRole.includes("DevOps")) superpower = "Rapid containerization and zero-downtime deployment";
  else if (bestRole.includes("Pitch")) superpower = "High-impact narrative design and demo storytelling";

  return {
    name: name || "Hackathon Contender",
    bio: rawBio,
    github: githubUrl,
    primaryRole: bestRole,
    skills: detectedSkills.length > 0 ? detectedSkills.slice(0, 8) : ["Problem Solving", "Rapid Prototyping", "JavaScript", "Python"],
    experienceLevel: exp,
    superpower: superpower
  };
}

// Team Balancer & Matching Solver
function runSquadMatching() {
  if (state.projects.length === 0) {
    showToast("Please create at least one project first.", "warning");
    return;
  }
  if (state.participants.length < 3) {
    showToast("Need at least 3 participants in the pool to form a team.", "warning");
    return;
  }

  const squads = [];
  let availablePool = [...state.participants];

  // For each project, recruit a complementary squad of 3 members + 1 Leader
  state.projects.forEach(project => {
    if (availablePool.length < 3) return;

    // Leader is the primary anchor
    const leader = {
      name: project.leaderName,
      bio: project.leaderBio,
      github: project.leaderGithub,
      role: "leader",
      primaryRole: "Team Leader & Architect",
      assignedRole: "Team Leader & Project Owner",
      skills: ["Leadership", "System Architecture", "Hackathon Strategy"],
      experienceLevel: "advanced",
      selectionReason: "Project founder — owns the problem statement, product vision and core requirements.",
      superpower: "Product vision and team synchronization"
    };

    // Candidate scoring relative to project requirements
    const scoredCandidates = availablePool.map(cand => {
      let score = 50;
      const candText = (cand.bio + " " + cand.skills.join(" ") + " " + cand.primaryRole).toLowerCase();

      // Check capabilities
      project.capabilities.forEach(cap => {
        const words = cap.toLowerCase().split(/[\s/]+/);
        words.forEach(w => {
          if (w.length > 2 && candText.includes(w)) score += 15;
        });
      });

      // Experience weighting
      if (cand.experienceLevel === "advanced") score += 10;
      if (cand.experienceLevel === "intermediate") score += 5;

      return { ...cand, matchScore: score };
    });

    // Complementary Constraint Selection: Pick 3 distinct roles to prevent 4 backends
    scoredCandidates.sort((a, b) => b.matchScore - a.matchScore);

    const chosenMembers = [];
    const roleCategoriesCovered = new Set();

    // Pass 1: pick top matching distinct roles
    for (const cand of scoredCandidates) {
      if (chosenMembers.length === 3) break;
      const roleCategory = cand.primaryRole.split(" ")[0]; // e.g. "Frontend", "Backend", "AI", "UI/UX"
      if (!roleCategoriesCovered.has(roleCategory) || chosenMembers.length >= 2) {
        roleCategoriesCovered.add(roleCategory);
        chosenMembers.push(cand);
      }
    }

    // Pass 2: fill remaining spots if strict diversity not met
    if (chosenMembers.length < 3) {
      for (const cand of scoredCandidates) {
        if (chosenMembers.length === 3) break;
        if (!chosenMembers.some(c => c.id === cand.id)) {
          chosenMembers.push(cand);
        }
      }
    }

    // Assign tactical roles and specific selection reasons
    const squadMembers = chosenMembers.map((m, idx) => {
      let assignedRole = m.primaryRole;
      let reason = `Selected for strong ${m.skills.slice(0, 3).join(", ")} capabilities matching the project's ${project.track} focus.`;
      
      if (m.primaryRole.includes("Frontend") || m.primaryRole.includes("UI")) {
        assignedRole = "Lead Frontend & User Experience";
        reason = "Owns all client-side UI, component workflows, and responsive demo presentation.";
      } else if (m.primaryRole.includes("AI") || m.primaryRole.includes("Data")) {
        assignedRole = "Lead AI / Pipeline Engineer";
        reason = "Owns LLM prompts, embeddings vector search, and core intelligent data inference.";
      } else if (m.primaryRole.includes("Backend") || m.primaryRole.includes("DevOps")) {
        assignedRole = "Core API & Cloud Infrastructure";
        reason = "Owns FastAPI / Node backend endpoints, database persistence, and cloud staging.";
      } else if (m.primaryRole.includes("Pitch") || m.primaryRole.includes("Design")) {
        assignedRole = "Product Pitch & UI Strategist";
        reason = "Owns judge presentation deck, live demo script, and user onboarding flow.";
      }

      return {
        ...m,
        assignedRole,
        selectionReason: reason
      };
    });

    // Remove chosen from pool
    const chosenIds = new Set(squadMembers.map(m => m.id));
    availablePool = availablePool.filter(m => !chosenIds.has(m.id));

    // Full 4-person squad
    const fullSquad = [leader, ...squadMembers];

    // Compute balance evaluation
    const balance = evaluateSquadBalance(fullSquad, project);

    // Generate 48-hour launch roadmap
    const sprintPlan = generateSprintRoadmap(fullSquad, project);

    squads.push({
      project,
      team: fullSquad,
      balance,
      sprintPlan
    });
  });

  state.matchedSquads = squads;
  state.selectedSquadIdx = 0;
  localStorage.setItem("hackops_squads", JSON.stringify(squads));

  showToast(`Successfully assembled ${squads.length} balanced 4-person squads!`, "success");
  switchTab("matcher");
}

// Squad Balance Evaluator
function evaluateSquadBalance(squad, project) {
  const allSkills = squad.flatMap(m => m.skills.map(s => s.toLowerCase()));
  const allRoles = squad.map(m => m.assignedRole || m.primaryRole);

  // 1. Capability Coverage
  const capabilityScores = project.capabilities.map(cap => {
    const keywords = SKILL_KEYWORDS[cap] || [cap.toLowerCase()];
    const matches = squad.filter(m => {
      const text = (m.bio + " " + m.skills.join(" ") + " " + m.primaryRole).toLowerCase();
      return keywords.some(kw => text.includes(kw.toLowerCase()));
    }).length;

    let score = 40;
    if (matches === 1) score = 75;
    if (matches >= 2) score = 95;

    return {
      name: cap,
      matches,
      score
    };
  });

  const avgCoverage = Math.round(capabilityScores.reduce((acc, c) => acc + c.score, 0) / capabilityScores.length);

  // 2. Role Diversity
  const uniqueRoles = new Set(allRoles.map(r => r.split(" ")[0])).size;
  const roleDiversityScore = Math.min(100, Math.round((uniqueRoles / 4) * 100));

  // 3. Synergy & Experience Mix
  const expValues = squad.map(m => m.experienceLevel === "advanced" ? 1.1 : m.experienceLevel === "intermediate" ? 1.0 : 0.85);
  const expAvg = expValues.reduce((a, b) => a + b, 0) / expValues.length;

  const overallScore = Math.min(99, Math.round((avgCoverage * 0.5 + roleDiversityScore * 0.35 + 85 * 0.15) * (expAvg / 1.05)));

  // Strengths & Gaps
  const strengths = [];
  const gaps = [];

  if (squad.some(m => m.primaryRole.includes("Frontend") || m.primaryRole.includes("UI"))) {
    strengths.push("Dedicated UI/Frontend lead ensures demo looks stunning to judges.");
  } else {
    gaps.push("No dedicated Frontend specialist — consider using pre-built UI components.");
  }

  if (squad.some(m => m.primaryRole.includes("Backend") || m.primaryRole.includes("DevOps") || m.primaryRole.includes("Cloud"))) {
    strengths.push("Strong backend and API infrastructure foundation.");
  } else {
    gaps.push("Missing dedicated DevOps engineer — recommend deploying on serverless platforms.");
  }

  if (squad.some(m => m.primaryRole.includes("Pitch") || m.primaryRole.includes("Design") || m.primaryRole.includes("Product"))) {
    strengths.push("High-caliber pitch deck & demo storytelling coverage.");
  } else {
    strengths.push("Full technical squad with direct end-to-end coding capabilities.");
  }

  return {
    overallScore,
    coverageScore: avgCoverage,
    roleDiversityScore,
    capabilityScores,
    strengths,
    gaps
  };
}

// 48-Hour Sprint Roadmap Generator
function generateSprintRoadmap(squad, project) {
  const leader = squad[0];
  const mem1 = squad[1] || { name: "Frontend Lead" };
  const mem2 = squad[2] || { name: "Backend Lead" };
  const mem3 = squad[3] || { name: "Pitch / QA Lead" };

  return {
    phases: [
      {
        id: "phase-1",
        title: "Phase 1: Inception & Architecture",
        timebox: "Hours 0 – 6",
        goal: "Lock down MVP scope, GitHub repo, system architecture, API schema contracts, and UI wireframes.",
        tasks: [
          { id: "t1", title: "Initialize Git repository, branch protection & CI deploy pipeline", owner: mem2.name, status: "done", deliverable: "Live staging URL placeholder" },
          { id: "t2", title: "Draft high-fidelity Figma UI wireframes & user journey flow", owner: mem1.name, status: "done", deliverable: "Approved 3-screen Figma flow" },
          { id: "t3", title: "Define OpenAPI/JSON data contracts & DB models", owner: leader.name, status: "doing", deliverable: "swagger.json / mock API response" },
          { id: "t4", title: "Formulate judge value proposition & competitive differentiation narrative", owner: mem3.name, status: "todo", deliverable: "1-page pitch thesis" }
        ]
      },
      {
        id: "phase-2",
        title: "Phase 2: Core MVP Build & AI Integrations",
        timebox: "Hours 6 – 24",
        goal: "Build the core functional engine, AI prompts/pipelines, and connect frontend to live backend APIs.",
        tasks: [
          { id: "t5", title: "Develop core AI prompt orchestration, parsing, and error-handling", owner: leader.name, status: "doing", deliverable: "Working LLM inference endpoint" },
          { id: "t6", title: "Build responsive UI screens, state management, and file upload components", owner: mem1.name, status: "todo", deliverable: "Interactive frontend interface" },
          { id: "t7", title: "Implement backend REST endpoints, authentication & vector store index", owner: mem2.name, status: "todo", deliverable: "FastAPI server running with tests" },
          { id: "t8", title: "Draft judge slide deck (Problem, Solution, Market, Tech Stack)", owner: mem3.name, status: "todo", deliverable: "Draft 8-slide presentation" }
        ]
      },
      {
        id: "phase-3",
        title: "Phase 3: Polish, Edge Cases & UI Wrap",
        timebox: "Hours 24 – 38",
        goal: "End-to-end integration testing, polish animations, handle failure edge cases, and lock features.",
        tasks: [
          { id: "t9", title: "Full end-to-end integration test of happy path with mock datasets", owner: mem2.name, status: "todo", deliverable: "Zero critical bugs during live test" },
          { id: "t10", title: "UI micro-interactions, loading spinners, glassmorphic toast notifications", owner: mem1.name, status: "todo", deliverable: "Polished responsive UX" },
          { id: "t11", title: "Record backup 2-minute product demo video (in case of live wifi issues)", owner: mem3.name, status: "todo", deliverable: "1080p MP4 recording" },
          { id: "t12", title: "Feature freeze & code clean-up; update README with architecture diagrams", owner: leader.name, status: "todo", deliverable: "Comprehensive GitHub documentation" }
        ]
      },
      {
        id: "phase-4",
        title: "Phase 4: Pitch Deck, Demo Video & Submission",
        timebox: "Hours 38 – 48",
        goal: "Rehearse live 3-minute pitch, finalize Devpost submission, and verify live demo URLs.",
        tasks: [
          { id: "t13", title: "Conduct 3 dry-run pitch rehearsals with timed 3-minute stopwatch", owner: mem3.name, status: "todo", deliverable: "Pitch completed in under 2:45" },
          { id: "t14", title: "Prepare live demo sandbox with pre-loaded realistic data", owner: leader.name, status: "todo", deliverable: "1-click instant demo preset" },
          { id: "t15", title: "Complete Devpost project submission with screenshots, tags & live link", owner: mem1.name, status: "todo", deliverable: "Confirmed hackathon submission" }
        ]
      }
    ],
    demoChecklist: [
      { text: "Live URL opens in under 2 seconds on incognito browser window", checked: true },
      { text: "Demo dataset pre-loaded so judges don't see empty screens", checked: true },
      { text: "Backup 1080p demo video uploaded to YouTube (unlisted)", checked: false },
      { text: "Clear 3-sentence hook explaining the problem in plain English", checked: true },
      { text: "Public GitHub repository contains clear README with architecture flowchart", checked: false }
    ]
  };
}

// UI Render Functions
function renderStats() {
  document.getElementById("stat-projects").textContent = state.projects.length;
  document.getElementById("stat-hackers").textContent = state.participants.length;
  document.getElementById("stat-squads").textContent = state.matchedSquads.length;
  const balanceScore = state.matchedSquads.length > 0 
    ? Math.round(state.matchedSquads.reduce((a, s) => a + s.balance.overallScore, 0) / state.matchedSquads.length) + "%"
    : "94%";
  document.getElementById("stat-balance").textContent = balanceScore;
}

function renderProjects() {
  const container = document.getElementById("projects-grid");
  if (!container) return;

  container.innerHTML = state.projects.map((proj, idx) => `
    <div class="project-card">
      <div>
        <div class="project-header">
          <span class="badge badge-leader">👑 Led by ${proj.leaderName}</span>
          <span class="badge badge-cyan">${proj.track}</span>
        </div>
        <h3 class="project-title" style="margin-top: 0.75rem;">${proj.title}</h3>
        <p class="project-desc">${proj.summary}</p>
        <div style="margin-top: 0.85rem; font-size: 0.82rem; color: var(--accent-emerald);">
          <b>🎯 MVP Target:</b> ${proj.mvpGoal}
        </div>
      </div>
      <div>
        <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem; font-weight: 700;">
          Required Capabilities
        </div>
        <div class="project-capabilities">
          ${proj.capabilities.map(c => `<span class="badge badge-skill">${c}</span>`).join("")}
        </div>
        <div style="margin-top: 1.25rem; display: flex; gap: 0.5rem;">
          <button class="btn btn-secondary btn-sm" onclick="findMatchesForProject('${proj.id}')" style="flex: 1;">
            🔍 View Top Candidates
          </button>
          <button class="btn btn-danger btn-sm" onclick="deleteProject('${proj.id}')" title="Delete project">
            ✕
          </button>
        </div>
      </div>
    </div>
  `).join("");
}

function renderMembers() {
  const container = document.getElementById("members-grid");
  if (!container) return;

  container.innerHTML = state.participants.map((mem) => {
    const initials = mem.name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase();
    return `
      <div class="member-card">
        <div class="member-card-top">
          <div class="member-identity">
            <div class="member-avatar">${initials}</div>
            <div>
              <div class="member-name">${mem.name}</div>
              <div class="member-role">${mem.primaryRole}</div>
            </div>
          </div>
          <span class="badge ${mem.experienceLevel === 'advanced' ? 'badge-success' : 'badge-cyan'}">
            ${mem.experienceLevel}
          </span>
        </div>
        <p class="member-bio">${mem.bio}</p>
        <div style="font-size: 0.78rem; color: var(--accent-cyan);">
          ⚡ <b>Superpower:</b> ${mem.superpower}
        </div>
        <div class="member-skills">
          ${mem.skills.map(s => `<span class="badge badge-skill">${s}</span>`).join("")}
        </div>
        <div style="margin-top: auto; padding-top: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
          ${mem.github ? `<a href="${mem.github}" target="_blank" style="color: var(--text-muted); font-size: 0.8rem; text-decoration: none;">🔗 GitHub</a>` : `<span></span>`}
          <button class="btn btn-danger btn-sm" onclick="deleteMember('${mem.id}')" style="padding: 0.2rem 0.6rem;">
            Remove
          </button>
        </div>
      </div>
    `;
  }).join("");
}

function renderSquads() {
  const container = document.getElementById("squads-container");
  if (!container) return;

  if (state.matchedSquads.length === 0) {
    container.innerHTML = `
      <div class="card" style="text-align: center; padding: 3.5rem 1.5rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
        <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem;">No Squads Formed Yet</h3>
        <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 1.5rem;">
          Click the "Launch AI Team Match" button to let the semantic balancing engine automatically assemble optimal 4-person squads.
        </p>
        <button class="btn btn-primary btn-lg" onclick="runSquadMatching()">
          🚀 Run AI Squad Matcher
        </button>
      </div>
    `;
    return;
  }

  // Render squad selector buttons if multiple squads
  const squadNavHtml = state.matchedSquads.length > 1 ? `
    <div style="display: flex; gap: 0.75rem; overflow-x: auto; margin-bottom: 1.5rem; padding-bottom: 0.5rem;">
      ${state.matchedSquads.map((s, idx) => `
        <button class="btn ${idx === state.selectedSquadIdx ? 'btn-primary' : 'btn-secondary'} btn-sm" onclick="selectSquad(${idx})">
          👑 ${s.project.title.slice(0, 24)}... (${s.balance.overallScore}% Fit)
        </button>
      `).join("")}
    </div>
  ` : "";

  const current = state.matchedSquads[state.selectedSquadIdx] || state.matchedSquads[0];
  const { project, team, balance } = current;

  container.innerHTML = `
    ${squadNavHtml}
    
    <div class="squad-banner">
      <div class="squad-header">
        <div>
          <span class="badge badge-leader" style="margin-bottom: 0.5rem;">
            👑 Squad #${state.selectedSquadIdx + 1} · Led by ${project.leaderName}
          </span>
          <h2 style="font-size: 1.6rem; font-weight: 800;">${project.title}</h2>
          <p style="color: var(--text-secondary); font-size: 0.9rem; max-width: 750px; margin-top: 0.35rem;">
            ${project.summary}
          </p>
        </div>
        <div>
          <button class="btn btn-emerald btn-lg" onclick="switchTab('launchpad')">
            ⚡ Open 48h Launchpad →
          </button>
        </div>
      </div>

      <div class="squad-score-grid">
        <div class="score-box">
          <div class="score-value high">${balance.overallScore}/100</div>
          <div class="score-label">Overall Squad Fit</div>
        </div>
        <div class="score-box">
          <div class="score-value high">${balance.coverageScore}%</div>
          <div class="score-label">Capability Coverage</div>
        </div>
        <div class="score-box">
          <div class="score-value high">${balance.roleDiversityScore}%</div>
          <div class="score-label">Role Diversity</div>
        </div>
        <div class="score-box">
          <div class="score-value medium">4 / 4</div>
          <div class="score-label">Full Squad Roster</div>
        </div>
      </div>
    </div>

    <!-- 4-Person Squad Cards -->
    <div style="margin-bottom: 2rem;">
      <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
        👥 Assembled 4-Person Roster
      </h3>
      <div class="squad-roster">
        ${team.map((m, idx) => `
          <div class="roster-card ${idx === 0 ? 'leader-roster' : ''}">
            <div>
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                <span class="badge ${idx === 0 ? 'badge-leader' : 'badge-member'}">
                  ${idx === 0 ? '👑 Leader' : `🙋 Member #${idx}`}
                </span>
                <span style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-muted);">
                  #0${idx + 1}
                </span>
              </div>
              <h4 style="font-size: 1.1rem; font-weight: 800;">${m.name}</h4>
              <div class="roster-assigned-role">${m.assignedRole || m.primaryRole}</div>
              <p class="roster-reason">${m.selectionReason}</p>
            </div>
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.35rem; font-weight: 600;">
                Core Skills
              </div>
              <div style="display: flex; flex-wrap: wrap; gap: 0.3rem;">
                ${m.skills.slice(0, 5).map(s => `<span class="badge badge-skill">${s}</span>`).join("")}
              </div>
            </div>
          </div>
        `).join("")}
      </div>
    </div>

    <!-- Balance & Capability Breakdown Grid -->
    <div class="grid-2">
      <div class="card">
        <h3 class="card-title">
          📊 Capability Coverage Breakdown
        </h3>
        <div class="balance-bars" style="margin-top: 1.25rem;">
          ${balance.capabilityScores.map((cap, i) => {
            const colors = ['emerald', 'cyan', 'indigo', 'amber'];
            const color = colors[i % colors.length];
            return `
              <div class="bar-item">
                <div class="bar-labels">
                  <span>${cap.name}</span>
                  <span style="font-family: var(--font-mono);">${cap.matches} contributor${cap.matches !== 1 ? 's' : ''} (${cap.score}%)</span>
                </div>
                <div class="bar-track">
                  <div class="bar-fill ${color}" style="width: ${cap.score}%;"></div>
                </div>
              </div>
            `;
          }).join("")}
        </div>
      </div>

      <div class="card">
        <h3 class="card-title">
          🎯 Squad Synergy & Gap Analysis
        </h3>
        <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
          <div>
            <div style="font-size: 0.82rem; font-weight: 700; color: var(--accent-emerald); margin-bottom: 0.35rem;">
              ✅ KEY STRENGTHS
            </div>
            ${balance.strengths.map(s => `
              <div style="font-size: 0.86rem; color: var(--text-secondary); background: rgba(16, 185, 129, 0.08); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); margin-bottom: 0.4rem; border-left: 3px solid var(--accent-emerald);">
                ${s}
              </div>
            `).join("")}
          </div>

          ${balance.gaps.length > 0 ? `
            <div>
              <div style="font-size: 0.82rem; font-weight: 700; color: var(--accent-amber); margin-bottom: 0.35rem;">
                ⚠️ OPPORTUNITY AREAS / GAPS
              </div>
              ${balance.gaps.map(g => `
                <div style="font-size: 0.86rem; color: var(--text-secondary); background: rgba(245, 158, 11, 0.08); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); margin-bottom: 0.4rem; border-left: 3px solid var(--accent-amber);">
                  ${g}
                </div>
              `).join("")}
            </div>
          ` : `
            <div style="font-size: 0.86rem; color: var(--accent-emerald); background: rgba(16, 185, 129, 0.08); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm);">
              ✨ Excellent balanced distribution with zero major skill gaps detected!
            </div>
          `}
        </div>
      </div>
    </div>
  `;
}

function renderLaunchpad() {
  const container = document.getElementById("launchpad-container");
  if (!container) return;

  if (state.matchedSquads.length === 0) {
    container.innerHTML = `
      <div class="card" style="text-align: center; padding: 3.5rem 1.5rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
        <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem;">Build Squads First</h3>
        <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 1.5rem;">
          To view the 48-hour launch plan, run the AI Squad Matcher to pair project leaders with balanced teammates.
        </p>
        <button class="btn btn-primary" onclick="runSquadMatching()">
          Run AI Matcher
        </button>
      </div>
    `;
    return;
  }

  const current = state.matchedSquads[state.selectedSquadIdx] || state.matchedSquads[0];
  const { project, sprintPlan, team } = current;

  container.innerHTML = `
    <div class="squad-banner" style="margin-bottom: 2rem;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
        <div>
          <span class="badge badge-emerald" style="margin-bottom: 0.5rem;">🚀 48-Hour Execution Roadmap</span>
          <h2 style="font-size: 1.6rem; font-weight: 800;">${project.title}</h2>
          <p style="color: var(--text-secondary); font-size: 0.9rem;">
            Lead: <b>${project.leaderName}</b> · Team: ${team.slice(1).map(m => m.name).join(", ")}
          </p>
        </div>
        <div style="display: flex; gap: 0.75rem;">
          <button class="btn btn-secondary btn-sm" onclick="exportSquadJSON()">
            📥 Download JSON Plan
          </button>
          <button class="btn btn-cyan btn-sm" onclick="exportMarkdownRoadmap()">
            📄 Copy Markdown
          </button>
        </div>
      </div>
    </div>

    <div class="grid-sidebar">
      <!-- Left: Phase Accordion Timeline -->
      <div>
        <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 1rem;">
          ⏱ 4-Phase Roadmap
        </h3>
        <div class="phase-timeline">
          ${sprintPlan.phases.map((phase, pIdx) => `
            <div class="phase-card ${pIdx === 0 ? 'open' : ''}" id="phase-card-${phase.id}">
              <div class="phase-card-header" onclick="togglePhaseCard('${phase.id}')">
                <div>
                  <div style="font-weight: 700; font-size: 0.95rem;">${phase.title}</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem;">${phase.goal}</div>
                </div>
                <div class="phase-badge-time">${phase.timebox}</div>
              </div>
              <div class="phase-tasks" id="tasks-${phase.id}">
                ${phase.tasks.map(t => `
                  <div class="task-item">
                    <input type="checkbox" class="task-checkbox" ${t.status === 'done' ? 'checked' : ''} onchange="toggleTaskStatus('${phase.id}', '${t.id}', this.checked)">
                    <div class="task-content">
                      <div class="task-title" style="${t.status === 'done' ? 'text-decoration: line-through; opacity: 0.6;' : ''}">
                        ${t.title}
                        <span class="task-owner-pill">👤 ${t.owner}</span>
                      </div>
                      <div class="task-deliverable">
                        🎯 <b>Deliverable:</b> ${t.deliverable}
                      </div>
                    </div>
                  </div>
                `).join("")}
              </div>
            </div>
          `).join("")}
        </div>
      </div>

      <!-- Right: Demo Day Checklist & Judging Alignment -->
      <div style="display: flex; flex-direction: column; gap: 1.5rem;">
        <div class="card">
          <h3 class="card-title">
            🎤 Demo-Day Submission Checklist
          </h3>
          <p style="font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 1rem;">
            Crucial verification steps to maximize judging score during the final 3-minute presentation.
          </p>
          <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            ${sprintPlan.demoChecklist.map((item, idx) => `
              <label style="display: flex; align-items: flex-start; gap: 0.75rem; font-size: 0.88rem; cursor: pointer;">
                <input type="checkbox" class="task-checkbox" ${item.checked ? 'checked' : ''} onchange="toggleChecklist(${idx}, this.checked)">
                <span style="${item.checked ? 'color: var(--text-primary); font-weight: 600;' : 'color: var(--text-secondary);'}">
                  ${item.text}
                </span>
              </label>
            `).join("")}
          </div>
        </div>

        <div class="card">
          <h3 class="card-title">
            🏆 Judge Rubric Alignment
          </h3>
          <div style="display: flex; flex-direction: column; gap: 0.85rem; margin-top: 1rem;">
            <div style="font-size: 0.84rem;">
              <b>💡 Innovation & Technical Depth (30%):</b>
              <div style="color: var(--text-secondary);">Clear AI value-add and architectural elegance over trivial wrappers.</div>
            </div>
            <div style="font-size: 0.84rem;">
              <b>🚀 Working Demo Execution (30%):</b>
              <div style="color: var(--text-secondary);">Live user interaction flow without relying on static mock screenshots.</div>
            </div>
            <div style="font-size: 0.84rem;">
              <b>🎨 UX & Visual Polish (20%):</b>
              <div style="color: var(--text-secondary);">Intuitive glassmorphism interface and responsive feedback loops.</div>
            </div>
            <div style="font-size: 0.84rem;">
              <b>🎤 Presentation & Business Impact (20%):</b>
              <div style="color: var(--text-secondary);">Memorable 3-minute pitch answering 'Why now?' and realistic viability.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Interactivity & Actions
function switchTab(tabId) {
  state.currentTab = tabId;
  document.querySelectorAll(".nav-tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabId);
  });
  document.querySelectorAll(".tab-content").forEach(el => {
    el.style.display = el.id === `tab-${tabId}` ? "block" : "none";
  });

  // Update stepper
  const stepMap = { "projects": 1, "members": 2, "matcher": 3, "launchpad": 4 };
  const currentStep = stepMap[tabId] || 1;
  document.querySelectorAll(".step-node").forEach((node, i) => {
    const idx = i + 1;
    node.classList.remove("active", "completed");
    if (idx === currentStep) node.classList.add("active");
    if (idx < currentStep) node.classList.add("completed");
  });

  if (tabId === "projects") renderProjects();
  if (tabId === "members") renderMembers();
  if (tabId === "matcher") renderSquads();
  if (tabId === "launchpad") renderLaunchpad();

  renderStats();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function selectSquad(idx) {
  state.selectedSquadIdx = idx;
  renderSquads();
}

function togglePhaseCard(phaseId) {
  const card = document.getElementById(`phase-card-${phaseId}`);
  if (card) {
    card.classList.toggle("open");
  }
}

function toggleTaskStatus(phaseId, taskId, isDone) {
  const current = state.matchedSquads[state.selectedSquadIdx];
  if (!current) return;
  const phase = current.sprintPlan.phases.find(p => p.id === phaseId);
  if (phase) {
    const task = phase.tasks.find(t => t.id === taskId);
    if (task) {
      task.status = isDone ? "done" : "todo";
      localStorage.setItem("hackops_squads", JSON.stringify(state.matchedSquads));
      renderLaunchpad();
    }
  }
}

function toggleChecklist(idx, isChecked) {
  const current = state.matchedSquads[state.selectedSquadIdx];
  if (current && current.sprintPlan.demoChecklist[idx]) {
    current.sprintPlan.demoChecklist[idx].checked = isChecked;
    localStorage.setItem("hackops_squads", JSON.stringify(state.matchedSquads));
  }
}

// Modal Handlers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("open");
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("open");
  }
}

// Add Participant Form Submit
function handleAddParticipant(e) {
  e.preventDefault();
  const name = document.getElementById("part-name").value.trim();
  const github = document.getElementById("part-github").value.trim();
  const bio = document.getElementById("part-bio").value.trim();
  const roleType = document.querySelector('input[name="participant-role"]:checked').value;
  const projectIdea = document.getElementById("part-idea") ? document.getElementById("part-idea").value.trim() : "";

  if (!name) {
    showToast("Please enter a name.", "error");
    return;
  }
  if (!bio && !github) {
    showToast("Please provide a bio or GitHub URL.", "error");
    return;
  }

  // Parse bio
  const parsed = parseRawBio(name, bio, github);

  if (roleType === "leader") {
    if (!projectIdea) {
      showToast("As a Project Leader, please provide your project idea.", "error");
      return;
    }
    // Create new project
    const newProject = {
      id: "proj-" + Date.now(),
      title: projectIdea.slice(0, 45) + (projectIdea.length > 45 ? "..." : ""),
      summary: projectIdea,
      mvpGoal: "Functional hackathon MVP demo with clear value proposition.",
      track: "AI & Innovation",
      leaderName: name,
      leaderBio: bio,
      leaderGithub: github,
      capabilities: ["AI / ML", "Frontend UI", "Backend APIs", "Product Pitch"],
      requiredRoles: ["AI Engineer", "Frontend Lead", "Backend Lead", "UI/UX & Pitch"]
    };
    state.projects.unshift(newProject);
    localStorage.setItem("hackops_projects", JSON.stringify(state.projects));
    showToast(`Project Leader ${name} and new project pitched!`, "success");
  } else {
    const newMember = {
      id: "mem-" + Date.now(),
      ...parsed,
      role: "member"
    };
    state.participants.unshift(newMember);
    localStorage.setItem("hackops_members", JSON.stringify(state.participants));
    showToast(`Member ${name} added to the candidate pool!`, "success");
  }

  closeModal("modal-add-participant");
  e.target.reset();
  renderProjects();
  renderMembers();
  renderStats();
}

// Add Project Form Submit
function handleAddProject(e) {
  e.preventDefault();
  const title = document.getElementById("new-proj-title").value.trim();
  const summary = document.getElementById("new-proj-desc").value.trim();
  const mvpGoal = document.getElementById("new-proj-goal").value.trim();
  const track = document.getElementById("new-proj-track").value.trim();
  const leaderName = document.getElementById("new-proj-leader").value.trim();
  const leaderBio = document.getElementById("new-proj-leader-bio").value.trim();

  if (!title || !summary || !leaderName) {
    showToast("Please fill in the required project fields.", "error");
    return;
  }

  const newProject = {
    id: "proj-" + Date.now(),
    title,
    summary,
    mvpGoal: mvpGoal || "Working hackathon demo ready for live judging.",
    track: track || "General AI",
    leaderName,
    leaderBio: leaderBio || "Project Creator and Team Lead",
    leaderGithub: "",
    capabilities: ["AI / ML", "Frontend UI", "Backend APIs", "Product / Pitch"],
    requiredRoles: ["Frontend Lead", "Backend Lead", "AI Specialist", "Product & Pitch"]
  };

  state.projects.unshift(newProject);
  localStorage.setItem("hackops_projects", JSON.stringify(state.projects));
  closeModal("modal-add-project");
  e.target.reset();
  renderProjects();
  renderStats();
  showToast(`New Project "${title}" pitched successfully!`, "success");
}

function deleteProject(id) {
  state.projects = state.projects.filter(p => p.id !== id);
  localStorage.setItem("hackops_projects", JSON.stringify(state.projects));
  renderProjects();
  renderStats();
  showToast("Project removed.", "info");
}

function deleteMember(id) {
  state.participants = state.participants.filter(m => m.id !== id);
  localStorage.setItem("hackops_members", JSON.stringify(state.participants));
  renderMembers();
  renderStats();
  showToast("Member removed from pool.", "info");
}

function findMatchesForProject(projId) {
  const proj = state.projects.find(p => p.id === projId);
  if (!proj) return;
  runSquadMatching();
}

function exportSquadJSON() {
  const current = state.matchedSquads[state.selectedSquadIdx];
  if (!current) return;
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(current, null, 2));
  const downloadAnchor = document.createElement("a");
  downloadAnchor.setAttribute("href", dataStr);
  downloadAnchor.setAttribute("download", `hackops_squad_${current.project.leaderName.replace(/\s+/g, '_')}.json`);
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();
  showToast("Downloaded squad plan as JSON.", "success");
}

function exportMarkdownRoadmap() {
  const current = state.matchedSquads[state.selectedSquadIdx];
  if (!current) return;
  const { project, team, sprintPlan } = current;

  let md = `# 🚀 HackOps Launch Plan: ${project.title}\n\n`;
  md += `**Leader:** ${project.leaderName}\n`;
  md += `**MVP Goal:** ${project.mvpGoal}\n\n`;
  md += `## 👥 Squad Roster\n`;
  team.forEach((m, i) => {
    md += `- **#0${i + 1} ${m.name}** (${m.assignedRole || m.primaryRole}): ${m.superpower || m.selectionReason}\n`;
  });
  md += `\n## ⏱ 48-Hour Execution Roadmap\n\n`;
  sprintPlan.phases.forEach(p => {
    md += `### ${p.title} (${p.timebox})\n`;
    md += `*Goal:* ${p.goal}\n\n`;
    p.tasks.forEach(t => {
      md += `- [${t.status === 'done' ? 'x' : ' '}] **${t.title}** (Owner: ${t.owner}) — *Deliverable:* ${t.deliverable}\n`;
    });
    md += `\n`;
  });

  navigator.clipboard.writeText(md).then(() => {
    showToast("Roadmap markdown copied to clipboard!", "success");
  });
}

function resetAllData() {
  if (confirm("Reset to default demo projects and hacker pool?")) {
    localStorage.removeItem("hackops_projects");
    localStorage.removeItem("hackops_members");
    localStorage.removeItem("hackops_squads");
    state.projects = [...DEFAULT_PROJECTS];
    state.participants = [...DEFAULT_MEMBERS];
    state.matchedSquads = [];
    state.selectedSquadIdx = 0;
    renderProjects();
    renderMembers();
    renderSquads();
    renderLaunchpad();
    renderStats();
    showToast("Reset to default demo state.", "info");
  }
}

// Toast System
function showToast(message, type = "info") {
  const container = document.getElementById("toast-container") || createToastContainer();
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span style="font-size: 1.1rem;">
      ${type === 'success' ? '✅' : type === 'error' ? '❌' : type === 'warning' ? '⚠️' : 'ℹ️'}
    </span>
    <span style="font-size: 0.88rem; font-weight: 600;">${message}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function createToastContainer() {
  const c = document.createElement("div");
  c.id = "toast-container";
  c.className = "toast-container";
  document.body.appendChild(c);
  return c;
}

// Real-time Bio Preview for Modal
function handleBioInputChange() {
  const bio = document.getElementById("part-bio")?.value || "";
  const name = document.getElementById("part-name")?.value || "Hacker";
  const previewBox = document.getElementById("bio-parse-preview");
  if (!previewBox) return;

  if (bio.trim().length > 10) {
    const parsed = parseRawBio(name, bio);
    previewBox.style.display = "block";
    previewBox.innerHTML = `
      <div style="font-size: 0.78rem; font-weight: 700; color: var(--accent-cyan); margin-bottom: 0.35rem;">
        🤖 AI LIVE PROFILE PARSER PREVIEW
      </div>
      <div style="font-size: 0.85rem; margin-bottom: 0.25rem;">
        <b>Primary Role:</b> <span class="badge badge-member">${parsed.primaryRole}</span>
        <span class="badge badge-success" style="margin-left: 0.35rem;">${parsed.experienceLevel}</span>
      </div>
      <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.35rem;">
        <b>Superpower:</b> ${parsed.superpower}
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 0.3rem;">
        ${parsed.skills.map(s => `<span class="badge badge-skill">${s}</span>`).join("")}
      </div>
    `;
  } else {
    previewBox.style.display = "none";
  }
}

// Event Listeners Initialization
document.addEventListener("DOMContentLoaded", () => {
  // Navigation Tabs
  document.querySelectorAll(".nav-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  // Step Nodes
  document.querySelectorAll(".step-node").forEach(node => {
    node.addEventListener("click", () => {
      const step = node.dataset.step;
      const tabMap = { "1": "projects", "2": "members", "3": "matcher", "4": "launchpad" };
      if (tabMap[step]) switchTab(tabMap[step]);
    });
  });

  // Form Submits
  const formPart = document.getElementById("form-add-participant");
  if (formPart) formPart.addEventListener("submit", handleAddParticipant);

  const formProj = document.getElementById("form-add-project");
  if (formProj) formProj.addEventListener("submit", handleAddProject);

  // Dynamic Radio toggle for leader vs member
  const roleRadios = document.querySelectorAll('input[name="participant-role"]');
  roleRadios.forEach(r => {
    r.addEventListener("change", (e) => {
      const ideaBox = document.getElementById("leader-idea-field");
      if (ideaBox) {
        ideaBox.style.display = e.target.value === "leader" ? "block" : "none";
      }
    });
  });

  // Bio live parser input
  const bioInput = document.getElementById("part-bio");
  if (bioInput) {
    bioInput.addEventListener("input", handleBioInputChange);
  }

  // Initial renders
  renderStats();
  renderProjects();
  renderMembers();
  renderSquads();
  renderLaunchpad();
});

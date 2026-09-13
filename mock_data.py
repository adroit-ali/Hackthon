"""
Mock hackathon data for HackOps demo and testing.
Provides diverse participant profiles across technical and product domains.
"""

MOCK_PARTICIPANTS = [
    {
        "name": "Ali Raza",
        "bio": "I am a CS student focused on Python, machine learning, LLM prompt pipelines, LangChain, and FastAPI backends. Built several AI assistants and REST APIs. I love handling the AI logic and model integration in hackathons.",
        "github": "https://github.com/aliraza-ai"
    },
    {
        "name": "Sara Chen",
        "bio": "Frontend developer who loves React, Next.js, TypeScript, Tailwind CSS, and glassmorphic modern UI design. I have built multiple interactive dashboards and enjoy turning ideas into smooth user experiences.",
        "github": "https://github.com/sarachen-ui"
    },
    {
        "name": "Ahmed Farooq",
        "bio": "Backend engineer comfortable with Python, FastAPI, PostgreSQL, Redis, Docker, and REST API architecture. I enjoy connecting services, handling database schemas, and making reliable backends.",
        "github": "https://github.com/ahmed-backend"
    },
    {
        "name": "Hina Malik",
        "bio": "Product and UI/UX designer with Figma mastery. I design user journeys, wireframes, and presentation decks. I also excel at pitching to judges, storytelling, and structuring demo day scripts.",
        "github": "https://github.com/hinamalik"
    },
    {
        "name": "Usman Ghani",
        "bio": "Data science student experienced in Python, pandas, scikit-learn, vector embeddings, and RAG search. Comfortable cleaning messy datasets and evaluating model accuracy.",
        "github": "https://github.com/usman-data"
    },
    {
        "name": "Zara Khan",
        "bio": "Full-stack developer with React, Node.js, Express, and PostgreSQL experience. I like full-stack integration work, state management, and quick debugging under time pressure.",
        "github": "https://github.com/zarakhan-dev"
    },
    {
        "name": "Hamza Tariq",
        "bio": "Cloud and DevOps engineer. Comfortable with Docker, GitHub Actions, Linux, cloud hosting, and deploying web applications within minutes to ensure zero downtime during judging.",
        "github": "https://github.com/hamzatariq-ops"
    },
    {
        "name": "Ayesha Noor",
        "bio": "Technical writer and product researcher. Skilled in creating interactive demo scripts, API docs, system architecture diagrams, and communicating complex technical value to non-technical judges.",
        "github": "https://github.com/ayeshanoor"
    }
]

MOCK_PROJECT = """
Build an AI-powered resume and interview copilot for students. A user uploads a resume PDF and pastes a target job description. The platform semantically compares the resume against the job requirements, identifies missing ATS keywords, highlights technical skill gaps, provides a match percentage score, and automatically drafts custom interview talking points. The MVP should have a responsive web interface and be ready for live demo day.
"""

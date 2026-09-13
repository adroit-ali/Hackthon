# ⚡ Modern Streamlit Starter Application

A production-ready, feature-rich Streamlit starter kit with interactive analytics, customizable charts, glassmorphic UI components, and state management.

---

## 🚀 Features

- **Executive Dashboard**: KPI metric cards with deltas, dynamic revenue curves, and donut breakdown charts.
- **Deep-Dive Analytics**: Multi-variable scatter plots, regional comparisons, and status distribution bars using Plotly.
- **Data Explorer**: Real-time multi-filter and keyword search, CSV export, and custom CSV uploader.
- **Interactive Forms & Session State**: Input validation, dynamic toasts/alerts, and real-time state manipulation.
- **Polished Dark Theme**: Styled with modern typography and sleek glassmorphism via custom CSS and `.streamlit/config.toml`.

---

## 🛠️ Getting Started

### 1. Prerequisites
Make sure Python (3.9+) is installed on your system.

### 2. Set Up Virtual Environment (Recommended)

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`.

---

## 📂 Project Structure

```
├── .streamlit/
│   └── config.toml      # Theme & server configuration
├── app.py               # Main Streamlit application entry point
├── requirements.txt     # Python package dependencies
└── README.md            # Quickstart documentation
```

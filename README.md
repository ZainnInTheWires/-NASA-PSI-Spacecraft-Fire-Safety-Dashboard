# -NASA-PSI-Spacecraft-Fire-Safety-Dashboard
SI-Powered Analytics &amp; Predictive Flammability Decision Support System
# 🛰️ NASA PSI Spacecraft Fire Safety Dashboard

An interactive, AI-assisted decision support dashboard built on NASA's **Physical Science Informatics (PSI)** combustion database. It helps mission planners, engineers, and researchers explore spacecraft fire safety risks across different exploration habitats — Moon, ISS, Mars, and EVA spacesuits.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Live Demo

👉 **[Launch the Dashboard](https://nasapsifiresafetydashboard.streamlit.app/)**

No installation required — just open the link in any browser.

---

## ✨ Features

| Tab | What it does |
|---|---|
| 🎯 **Mission Risk Matrix** | Ranks NASA PSI investigations by flammability risk for a selected habitat. Includes radar comparison against Earth baseline. |
| 🔥 **Physics & What-If Simulator** | Interactive sliders for O₂ %, pressure, airflow, gravity regime, and fuel type. Predicts flame geometry and spread rate. |
| 🔬 **Hardware Rigs & Fuels** | Breakdown of CIR, MDCA, MSG, and Cygnus rigs; findings from BASS, Saffire, FLEX, and CFI experiments. |
| 🚨 **Detection & Suppression** | SAME, DAFT, and FLEX insights on smoke detection, lunar dust false alarms, and fine water mist extinguishers. |
| 🤖 **Safety AI & Spin-offs** | Rule-based decision support chatbot + terrestrial technology spin-offs. |

### 🌍 Habitat Presets
- 🌙 **Moon Base / Pressurized Rover** — 32% O₂, 10.2 psi
- 🛰️ **ISS / Spacecraft Station** — 21% O₂, 14.7 psi
- 👩‍🚀 **Spacesuit EVA Profile** — 100% O₂, 4.3 psi
- 🔴 **Martian Surface Habitat** — 21% O₂, 7.0 psi
- ⚙️ **Custom Mission Profile** — user-defined

---

## 🖥️ Run Locally

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/nasa-fire-safety-dashboard.git
cd nasa-fire-safety-dashboard

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
streamlit run app.py

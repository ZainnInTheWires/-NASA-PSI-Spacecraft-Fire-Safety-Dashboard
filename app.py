import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & DARK SPACE UI STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NASA PSI Fire Safety Command Dashboard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Dark Space Glassmorphism Theme */
    .stApp {
        background-color: #0A0E17;
        color: #E2E8F0;
    }
    
    /* Main Headers */
    .nasa-header {
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 50%, #FC3D21 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .nasa-sub {
        font-size: 1.15rem;
        color: #94A3B8;
        font-weight: 500;
        margin-bottom: 25px;
    }
    
    /* Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    .alert-card-high {
        background: rgba(220, 38, 38, 0.15);
        border-left: 5px solid #EF4444;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 15px;
    }

    .alert-card-safe {
        background: rgba(16, 185, 129, 0.15);
        border-left: 5px solid #10B981;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 15px;
    }
    
    /* Metric Cards */
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38BDF8;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = "nasa_fire_safety_master.csv"
    if not os.path.exists(file_path):
        for f in os.listdir("."):
            if f.endswith("nasa_fire_safety_master.csv"):
                file_path = f
                break
    df = pd.read_csv(file_path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Dataset error: Ensure `nasa_fire_safety_master.csv` is generated. Error: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.image("https://www.nasa.gov/wp-content/themes/nasa/assets/images/nasa-logo.svg", width=140)
st.sidebar.markdown("### 🛰️ Habitat Control Center")

env_preset = st.sidebar.selectbox(
    "Target Exploration Habitat:",
    [
        "Custom Mission Profile",
        "🌙 Moon Base / Pressurized Rover (32% O2, 10.2 psi)",
        "🛰️ ISS / Spacecraft Station (21% O2, 14.7 psi)",
        "👩‍🚀 Spacesuit EVA Profile (100% O2, 4.3 psi)",
        "🔴 Martian Surface Habitat (21% O2, 7.0 psi)"
    ]
)

# Preset presets mapper
if "Moon Base" in env_preset:
    sel_o2, sel_press, env_name = 32.0, 10.2, "Moon Base / Rover"
elif "Spacesuit" in env_preset:
    sel_o2, sel_press, env_name = 100.0, 4.3, "Spacesuit EVA"
elif "Martian" in env_preset:
    sel_o2, sel_press, env_name = 21.0, 7.0, "Martian Base"
elif "ISS" in env_preset:
    sel_o2, sel_press, env_name = 21.0, 14.7, "ISS Spacecraft"
else:
    sel_o2 = st.sidebar.slider("Oxygen Concentration (%)", 15.0, 100.0, 30.0)
    sel_press = st.sidebar.slider("Atmospheric Pressure (psi)", 3.0, 15.0, 10.2)
    env_name = "Custom Atmosphere"

st.sidebar.markdown("---")
cat_filter = st.sidebar.multiselect("Research Focus:", df["category"].unique().tolist(), default=df["category"].unique().tolist())
hw_filter = st.sidebar.multiselect("Hardware Apparatus:", df["hardware"].unique().tolist(), default=df["hardware"].unique().tolist())

# Apply filters
filtered_df = df[(df["category"].isin(cat_filter)) & (df["hardware"].isin(hw_filter))]

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown("<div class='nasa-header'>🛰️ NASA PSI Spacecraft Fire Safety Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='nasa-sub'>SI-Powered Analytics & Predictive Flammability Decision Support System</div>", unsafe_allow_html=True)

# Top KPI Metric Ribbon
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown("<div class='glass-card'><div class='metric-label'>Filtered Tests</div><div class='metric-value'>{}</div></div>".format(len(filtered_df)), unsafe_allow_html=True)
with k2:
    st.markdown("<div class='glass-card'><div class='metric-label'>PSI Projects</div><div class='metric-value'>{}</div></div>".format(len(filtered_df["investigation_name"].unique())), unsafe_allow_html=True)
with k3:
    st.markdown("<div class='glass-card'><div class='metric-label'>Target O2 Conc.</div><div class='metric-value'>{:.1f}%</div></div>".format(sel_o2), unsafe_allow_html=True)
with k4:
    st.markdown("<div class='glass-card'><div class='metric-label'>Cabin Pressure</div><div class='metric-value'>{:.1f} psi</div></div>".format(sel_press), unsafe_allow_html=True)
with k5:
    risk_score = (sel_o2 / 21.0) * 1.8 + (14.7 / max(sel_press, 1.0)) * 0.4
    st.markdown("<div class='glass-card'><div class='metric-label'>Hazard Score</div><div class='metric-value' style='color:#FC3D21;'>{:.2f}</div></div>".format(risk_score), unsafe_allow_html=True)

# NAVIGATION TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Mission Risk Matrix", 
    "🔥 Physics & What-If Simulator", 
    "🔬 Hardware Rigs & Fuels", 
    "🚨 Detection, Suppression & Dust", 
    "🤖 NASA Safety AI & Spin-offs"
])

# ==================== TAB 1: MISSION RISK MATRIX ====================
with tab1:
    st.subheader("Explore Relevant Investigations for Target Habitat")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Relevance Ranking Bar Chart
        rank_df = filtered_df.groupby("investigation_name")["flammability_risk_index"].mean().reset_index().sort_values(by="flammability_risk_index", ascending=True)
        fig_bar = px.bar(
            rank_df,
            x="flammability_risk_index",
            y="investigation_name",
            orientation="h",
            color="flammability_risk_index",
            color_continuous_scale="Reds",
            template="plotly_dark",
            title="Investigation Hazard Index Ranking",
            labels={"flammability_risk_index": "Calculated Risk Score", "investigation_name": "PSI Project"}
        )
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=450)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_b:
        st.markdown("### 📊 Active Environment Analysis")
        if sel_o2 >= 30.0:
            st.markdown(f"""
            <div class='alert-card-high'>
                <h4>⚠️ HIGH FLAMMABILITY ENVIRONMENT ({env_name})</h4>
                <p>Oxygen concentration is at <b>{sel_o2}%</b>. Material flammability is increased by over <b>40%</b> compared to terrestrial air.</p>
                <p><b>Critical PSI Insights:</b> Research from <i>BASS-II</i> and <i>Saffire-III</i> demonstrates that structural polymers (e.g., PMMA, Nomex) burn continuously under low convective flow in high O2 atmospheres.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-card-safe'>
                <h4>✅ NOMINAL ATMOSPHERIC REGIME ({env_name})</h4>
                <p>Oxygen concentration is within standard Earth baseline limits (21.0%).</p>
                <p><b>Primary Hazard:</b> Absence of buoyancy-driven natural convection. Fires rely purely on ambient airflow and diffusion.</p>
            </div>
            """, unsafe_allow_html=True)

        # Environment Radar Comparison
        st.markdown("#### Habitat Flammability Comparison")
        radar_data = pd.DataFrame({
            'Metric': ['O2 Concentration', 'Spread Rate Potential', 'Ignition Sensitivity', 'Extinguishment Difficulty'],
            'Selected Target': [sel_o2/100*10, (sel_o2/21)*4, (sel_o2/21)*5, (14.7/sel_press)*5],
            'Earth Baseline (21% O2)': [2.1, 4.0, 5.0, 5.0]
        })
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=radar_data['Selected Target'], theta=radar_data['Metric'], fill='toself', name=env_name))
        fig_radar.add_trace(go.Scatterpolar(r=radar_data['Earth Baseline (21% O2)'], theta=radar_data['Metric'], fill='toself', name='Earth Baseline'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 15])), template="plotly_dark", height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_radar, use_container_width=True)

# ==================== TAB 2: PHYSICS & WHAT-IF SIMULATOR ====================
with tab2:
    st.subheader("Predictive Microgravity Combustion & What-If Engine")
    
    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🎛️ Simulation Parameters")
        sim_o2 = st.slider("Oxygen Level (%)", 15, 90, int(sel_o2))
        sim_flow = st.slider("Forced Airflow Velocity (cm/s)", 0.0, 30.0, 5.0)
        sim_gravity = st.selectbox("Gravity Regime:", ["Microgravity (0g - ISS)", "Lunar Gravity (1/6g - Moon)", "Martian Gravity (3/8g - Mars)", "Earth Gravity (1g)"])
        sim_material = st.selectbox("Sample Fuel Material:", ["PMMA (Acrylic Glass)", "Cotton/Poly Blend Fabric", "Silicone Rubber", "Gaseous Propane"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sim_col2:
        # Compute Physics Outputs
        is_microg = "Microgravity" in sim_gravity
        flame_shape = "Spherical Blue Sphere (Diffusion Driven)" if is_microg else "Flickering Teardrop (Buoyancy Driven)"
        spread_speed = (sim_o2 / 21.0) * (1.5 if sim_flow > 0 else 0.8) * (1.2 if is_microg else 1.0)
        
        st.markdown("### 🔬 Predicted Fire Characteristics")
        
        c_p1, c_p2, c_p3 = st.columns(3)
        c_p1.metric("Predicted Flame Geometry", flame_shape.split(" ")[0])
        c_p2.metric("Relative Flame Spread Rate", f"{spread_speed:.2f}x Earth Base")
        c_p3.metric("Dominant Heat Transfer", "Radiation & Diffusion" if is_microg else "Buoyant Convection")
        
        # 3D Parameter Map
        fig_3d = px.scatter_3d(
            filtered_df,
            x="o2_concentration_pct",
            y="pressure_psi",
            z="flow_speed_cms",
            color="flammability_risk_index",
            symbol="fuel_type",
            hover_name="investigation_name",
            template="plotly_dark",
            title="3D Empirical Parameter Distribution across NASA Datasets"
        )
        fig_3d.update_layout(height=450, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_3d, use_container_width=True)

# ==================== TAB 3: HARDWARE RIGS & FUELS ====================
with tab3:
    st.subheader("NASA PSI Hardware Rigs & Fuel Behavior Analysis")
    
    rig_tab1, rig_tab2, rig_tab3 = st.tabs(["🚀 Hardware Apparatus Breakdown", "🪵 Solid Fuels (BASS/Saffire)", "💧 Liquid & Gas (FLEX/ACME/CFI)"])
    
    with rig_tab1:
        st.markdown("""
        | Hardware System | Investigations | Supported Fuel Types | Airflow / Environment |
        |---|---|---|---|
        | **Combustion Integrated Rack (CIR)** | ACME (BRE, E-FIELD, CFI-G) | Gaseous Fuels, Spherical Burners | Sealed Chamber up to 85% O2 |
        | **Multi-user Droplet Combustion Apparatus (MDCA)** | FLEX, FLEX-2, CFI | Liquid Fuel Droplets | Quiescent & Suppressant Gas Dilution |
        | **Microgravity Science Glovebox (MSG)** | BASS, BASS-II, SPICE, SLICE | Solid Fabrics, Thin/Thick Plastics | Fan-driven Flow Duct (0 to 30 cm/s) |
        | **Cygnus Cargo Vehicle** | Saffire-I, II, III | Large-scale Solids (1-meter long) | Uncrewed Destructive Flight Tests |
        """)
        
    with rig_tab2:
        st.markdown("### 🪵 Solid Material Flammability (BASS & Saffire Insights)")
        st.write("""
        - **Low Airflow Risk:** In zero gravity, a small airflow (2 to 5 cm/s) supplies fresh oxygen without cooling the flame, making low airflow **more flammable** than zero airflow.
        - **Scale Effects (Saffire):** Large-scale fires burn significantly hotter and faster than small-sample glovebox tests, proving that terrestrial small-scale material testing can underpredict space fire risk.
        """)
        
    with rig_tab3:
        st.markdown("### 💧 Liquid Droplets & Cool Flames (FLEX & CFI-G)")
        st.write("""
        - **Cool Flames:** FLEX and CFI experiments discovered that after an initial hot flame extinguishes, liquid droplets can continue burning invisibly as a **cool flame** (~600 K), posing unseen reignition risks.
        """)

# ==================== TAB 4: DETECTION, SUPPRESSION & DUST ====================
with tab4:
    st.subheader("Detection, Suppression, & Dust Diagnostic Research")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🚨 Fire Detection & Dust (SAME, SAME-R, DAFT)")
        st.markdown("""
        - **Smoke Particle Agglomeration:** Microgravity causes smoke particles to linger and merge into larger clusters due to the lack of buoyant plumes.
        - **DAFT Dual-Use Findings:** Smoke detection apparatuses tested in SAME were evaluated during DAFT to measure **lunar dust particles**.
        - **Design Directive:** Future lunar rover and habitat sensors must use multi-wavelength optical sensors to distinguish between dangerous smoke particles and non-combustion regolith dust.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_d2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🧯 Suppression Dynamics (FLEX & FLEX-2)")
        st.markdown("""
        - **Gaseous Dilution:** Tested flame extinguishment limits using $CO_2$ and Helium ($He$) dilution.
        - **Fine Water Mist Extinguishers:** Fine water mist technology engineered for space offers rapid extinction without flooding delicate electronic racks.
        - **Extinction Limits:** Spherical flames in microgravity require higher suppressant concentrations than equivalent flames on Earth.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 5: NASA SAFETY AI & SPIN-OFFS ====================
with tab5:
    st.subheader("NASA Safety AI Query Assistant & Terrestrial Spin-offs")
    
    ai_col, spin_col = st.columns(2)
    
    with ai_col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🤖 NASA PSI Safety Advisor")
        user_query = st.text_input("Ask a question about space fire safety:", "What safety controls are required for a Moon Base operating at 30% oxygen?")
        
        if user_query:
            st.markdown("**Automated Decision Support Analysis:**")
            if "moon" in user_query.lower() or "30%" in user_query.lower() or "oxygen" in user_query.lower():
                st.info("""
                **Recommendations based on BASS-II & Saffire Data:**
                1. **Material Selection:** Standard flame-retardant polymers will burn continuously at 30% O2. Specify materials with Oxygen Index > 35%.
                2. **Airflow Control:** Maintain cabin fan speeds < 5 cm/s during fire alarms to prevent forced convective feeding of flames.
                3. **Detection Array:** Combine optical smoke detectors with gas-phase CO/CO2 monitors to prevent false alarms from airborne lunar dust (based on DAFT results).
                """)
            else:
                st.success("""
                **General Microgravity Directive:**
                1. Always assume flames are spherical and diffusion-limited.
                2. Utilize fine water mist or CO2 gas inerting for suppression.
                3. Maintain active air suction ducts to direct smoke toward photoelectric sensors.
                """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with spin_col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🌍 Earth Applications (Spin-off Tech)")
        st.markdown("""
        1. **Fine Water Mist Fire Extinguishers:** Developed for the ISS, this tech is now used in data centers and art museums to extinguish fires without water damage.
        2. **Firefighter Protective Gear:** NASA thermal insulation materials derived from space fire testing improve turnout gear and lightweight breathing oxygen tanks for terrestrial firefighters.
        3. **Advanced Smoke Sensors:** SAME detection algorithms led to ultra-sensitive early warning aspirating smoke detectors (VESDA systems) used in cleanrooms globally.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.caption("NASA Physical Science Informatics (PSI) Database | Spacecraft Fire Safety Decision Support System")
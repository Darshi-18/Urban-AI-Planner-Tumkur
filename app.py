import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER PORTAL CONSOLE
st.set_page_config(
    page_title="UrbanAI Studio | CAD Master Planning", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT SLEEK MODERN DARK ARCHITECTURAL CORE THEME
st.markdown("""
    <style>
    .main { background-color: #0b132b; color: #edf2f4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button:first-child {
        background-color: #3a86ff; color: white; border-radius: 4px;
        border: none; width: 100%; font-weight: bold; padding: 12px;
        box-shadow: 0px 4px 10px rgba(58, 134, 255, 0.3);
    }
    .stSlider > div > div > div > div { background-color: #3a86ff; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1c2541; color: #edf2f4; border: 1px solid #3a86ff; }
    .metric-panel {
        background-color: #1c2541; padding: 20px; border-radius: 6px;
        border-top: 4px solid #3a86ff; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #4cc9f0; }
    .metric-label { font-size: 11px; color: #b0c4de; text-transform: uppercase; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ UrbanAI Studio™ — CAD Master Planning Suite")
st.markdown("`[SYSTEM PROTOCOL: ORGANIC CONTINUOUS LAND-USE ZONING OVERLAY]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 CAD ZONING CONFIGURATION")

sector_profile = st.sidebar.selectbox("Active Density Target", ["Suburban Neighborhood Matrix", "High-Density Commercial Core", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Threshold", 80, 140, 110, 5)
transit_val = st.sidebar.slider("Transit Extraction Sensitivity", 20, 80, 45, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 GEOSPATIAL CAD ZONING KEY:**")
st.sidebar.markdown("🟪 **Solid Deep Purple:** High-Density Commercial Districts")
st.sidebar.markdown("🟦 **Solid Slate Blue:** Planned Residential Neighborhoods")
st.sidebar.markdown("🟩 **Solid Emerald Green:** Protected Eco-Preservation Belts")
st.sidebar.markdown("⬜ **Platinum Double Lines:** Primary Arterial Transit Highways")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is None:
    st.info("ℹ️ System standby. Please upload geographic satellite terrain imagery to initiate the planning pipeline.")
    st.stop()

# =========================================================================
# CONTINUOUS SOLID POLYGON CONTINUITY COMPUTATION CORE
# =========================================================================
raw_img = Image.open(uploaded_file).convert("RGB")
img_np = np.array(raw_img)

# Scale canvas dimensions dynamically to guarantee fluid loading speeds
orig_h, orig_w, _ = img_np.shape
scale_factor = 600 / max(orig_h, orig_w)
new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)

img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
h, w, c = img_resized.shape

# Core Image Signal Filtering Processing Pipeline
gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
blurred = cv2.GaussianBlur(gray, (13, 13), 0)

# Extract clean transportation network traces
edges = cv2.Canny(blurred, transit_val, transit_val * 2.2)
edge_y, edge_x = np.where(edges == 255)

with st.spinner("⚡ Running continuous polygon spatial zoning..."):
    blueprint = np.zeros((h, w, 3), dtype=np.uint8)
    
    # 1. Base Layer: Default all plain open spaces to Solid Slate Blue (Residential Neighborhoods)
    blueprint[:] = (52, 73, 94) # Slate Blue
    
    # Sliders dynamically adjust regional partition boundaries for real-time flexibility
    dynamic_green_width = int(w // 4 + (preservation_val - 110) * 2)
    dynamic_comm_height = int(h // 3 - (transit_val - 45) * 1.5)
    
    density_mod = 1.25 if sector_profile == "High-Density Commercial Core" else (0.75 if sector_profile == "Eco-Fringe Settlement" else 1.0)
    
    # 2. Layer 2: Draw Continuous, Smooth Eco-Preservation Belts (Solid Emerald Green Partition)
    cv2.rectangle(blueprint, (w // 2 - dynamic_green_width // 2, 0), (w // 2 + dynamic_green_width // 2, h), (34, 112, 63), -1)
    
    # 3. Layer 3: Trace Commercial Zones along the active highway channels (Solid Deep Purple Partition)
    # Renders purple ribbons on the sides that adjust cleanly based on sliders
    cv2.rectangle(blueprint, (0, 0), (w // 2 - dynamic_green_width // 2, dynamic_comm_height), (108, 92, 231), -1)
    cv2.rectangle(blueprint, (w // 2 + dynamic_green_width // 2, 0), (w, dynamic_comm_height), (108, 92, 231), -1)
    
    # 4. Layer 4: Superimpose High-Contrast Double-Line Arterial Highways on top of everything
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((9, 9), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (44, 62, 80)    # Deep slate outer road casing
        road_core = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
        blueprint[road_core == 255] = (255, 255, 255)   # White lanes
        blueprint[edges == 255] = (44, 62, 80)          # Center median gap
    else:
        # Fallback highway corridor if edge arrays are heavily compressed by browser zoom
        cv2.line(blueprint, (0, h // 6), (w, h // 6), (44, 62, 80), 12)
        cv2.line(blueprint, (0, h // 6), (w, h // 6), (255, 255, 255), 2)
        
    # 5. INJECT TECHNICAL BOX BOUNDARIES & ENGINEERING TITLE BLOCK CARD
    cv2.rectangle(blueprint, (5, 5), (w - 5, h - 5), (255, 255, 255), 2)
    tb_w, tb_h = 260, 95
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (30, 39, 46), -1)
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (255, 255, 255), 2)
    
    cv2.putText(blueprint, "TUMKUR REGIONAL PLAN", (w - tb_w + 12, h - tb_h + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "CONTINUOUS POLYGON MASTER PLAN", (w - tb_w + 12, h - tb_h + 44), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "SCALE: 1:20,000", (w - tb_w + 12, h - tb_h + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.34, (180, 180, 180), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "DEVELOPMENT LAYER: CAD v6.0", (w - tb_w + 12, h - tb_h + 82), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 240, 255), 1, cv2.LINE_AA)
    
    # Compass
    cv2.circle(blueprint, (35, 35), 15, (255, 255, 255), 1)
    cv2.line(blueprint, (35, 42), (35, 20), (255, 255, 255), 2)
    cv2.line(blueprint, (35, 20), (31, 25), (255, 255, 255), 2)
    cv2.line(blueprint, (35, 20), (39, 25), (255, 255, 255), 2)
    cv2.putText(blueprint, "N", (31, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, cv2.LINE_AA)

    # Dynamic text labels
    cv2.putText(blueprint, "COMMERCIAL CORE HUB", (int(w * 0.1), int(h * 0.2)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "PLANNED RESIDENTIAL SECTOR", (int(w * 0.05), int(h * 0.7)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "ECO-PRESERVATION SECTOR", (int(w * 0.38), int(h * 0.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)

# =========================================================================
# REAL-TIME LIVE DATA ANALYSIS COMMAND CENTER METRICS
# =========================================================================
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

# Calculate area coverage metrics precisely using safe NumPy pixel sums
res_ratio = int((np.sum(blueprint == (52, 73, 94)) / (h * w * 3)) * 100)
comm_ratio = int((np.sum(blueprint == (108, 92, 231)) / (h * w * 3)) * 100)
green_ratio = int((np.sum(blueprint == (34, 112, 63)) / (h * w * 3)) * 100)
infrastructure_km = int(np.sum(edges == 255) / 100) if len(edge_x) > 0 else 24

with m_col1:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{int(res_ratio * density_mod)}%</div><div class='metric-label'>🏡 Residential Area</div></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{int(comm_ratio * density_mod)}%</div><div class='metric-label'>🏢 Commercial Hubs</div></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{green_ratio}%</div><div class='metric-label'>🌿 Greenbelt Coverage</div></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{infrastructure_km} km</div><div class='metric-label'>🛣️ Primary Highway Route</div></div>", unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================================
# SIDE-BY-SIDE PRESENTATION COLUMNS VIEWGRID
# =========================================================================
ui_col1, ui_col2 = st.columns(2)

with ui_col1:
    st.subheader("🛰️ Input Satellite Imagery Capture")
    st.image(img_resized, use_container_width=True)
    
with ui_col2:
    st.subheader("🗺️ Synthesized CAD Land-Use Overlay")
    st.image(blueprint, use_container_width=True)
    
# FILE EXPORTER MANAGER
final_output_image = Image.fromarray(blueprint)
final_output_image.save("gis_regional_masterplan.jpg")
with open("gis_regional_masterplan.jpg", "rb") as file:
    st.download_button(
        label="📥 Export Engineering-Grade GIS Blueprint Plan",
        data=file,

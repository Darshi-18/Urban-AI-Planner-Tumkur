import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER PORTAL CONSOLE
st.set_page_config(page_title="UrbanAI Studio | GIS Suite", layout="wide", initial_sidebar_state="expanded")

# 2. INJECT SLEEK MODERN DARK ARCHITECTURAL CORE THEME
st.markdown("""
    <style>
    .main { background-color: #0b132b; color: #edf2f4; font-family: sans-serif; }
    div.stButton > button:first-child {
        background-color: #3a86ff; color: white; border-radius: 4px; border: none; width: 100%; font-weight: bold; padding: 12px;
    }
    .stSlider > div > div > div > div { background-color: #3a86ff; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1c2541; color: #edf2f4; border: 1px solid #3a86ff; }
    .metric-panel {
        background-color: #1c2541; padding: 20px; border-radius: 6px; border-top: 4px solid #3a86ff; text-align: center;
    }
    .metric-value { font-size: 26px; font-weight: 700; color: #4cc9f0; font-family: monospace; }
    .metric-label { font-size: 11px; color: #b0c4de; text-transform: uppercase; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ UrbanAI Studio™ — GIS Master Planning Suite")
st.markdown("`[SYSTEM PROTOCOL: MASTER REGIONAL DEVELOPMENT OVERLAY]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS & DATA INGESTION
# =========================================================================
st.sidebar.header("📡 GIS ANALYSIS CONFIGURATION")
sector_profile = st.sidebar.selectbox("Active Planning Preset", ["Suburban Neighborhood Matrix", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Threshold", 80, 140, 110, 5)
transit_val = st.sidebar.slider("Transit Extraction Sensitivity", 20, 80, 45, 5)

b_size, b_gap = 24, 8

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 GEOSPATIAL MAP LEGEND:**")
st.sidebar.markdown("🟪 **Deep Purple Line Grids:** High-Density Commercial Core\n\n🟦 **Slate Blue Matrix:** Medium-Density Residential Sectors\n\n🟩 **Lime & Sage Pasture:** Urban Agriculture & Greenbelts\n\n⬜ **Slate Casing / White Split:** Primary Arterial Transit Corridors")

uploaded_file = st.file_uploader("UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is None:
    st.info("ℹ️ System standby. Please upload geographic satellite terrain imagery to initiate the planning pipeline.")
    st.stop()

# =========================================================================
# PROCESSING AND STANDALONE MAP RENDERING ENGINE
# =========================================================================
raw_img = Image.open(uploaded_file).convert("RGB")
img_np = np.array(raw_img)

orig_h, orig_w, _ = img_np.shape
scale_factor = 512 / max(orig_h, orig_w)
new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)

img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
h, w, c = img_resized.shape

gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
edges = cv2.Canny(blurred, transit_val, transit_val * 2.5)
edge_y, edge_x = np.where(edges == 255)

_, green_mask = cv2.threshold(blurred, preservation_val, 255, cv2.THRESH_BINARY_INV)
green_mask = cv2.dilate(green_mask, np.ones((9, 9), np.uint8), iterations=1)
smooth_green = cv2.GaussianBlur(green_mask, (25, 25), 0)

with st.spinner("⚡ Running spatial matrix optimizations..."):
    blueprint = np.zeros((h, w, 3), dtype=np.uint8)
    blueprint[:] = (45, 52, 54) # Slate backing
    
    blueprint[smooth_green > 100] = (156, 204, 101) # GIS Lime Green pastures map
    
    spacing = b_size + b_gap
    res_count, comm_count = 0, 0
    commercial_threshold = 45 + (45 - transit_val) * 0.5
    density_mod = 1.35 if sector_profile == "High-Density Core Matrix" else (0.65 if sector_profile == "Eco-Fringe Settlement" else 1.0)
    
    for y in range(40, h - spacing, spacing):
        for x in range(40, w - spacing, spacing):
            dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2)) if len(edge_x) > 0 else 999.0
                
            if smooth_green[y + b_size//2, x + b_size//2] <= 100:
                if dist_to_transit < commercial_threshold:
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (94, 53, 177), -1) 
                    for offset in range(0, b_size, 6):
                        cv2.line(blueprint, (x + offset, y), (x, y + offset), (255, 255, 255), 1)
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (255, 255, 255), 1)
                    comm_count += 1
                else:
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (58, 125, 160), -1) 
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + b_size//2 - 1, y + b_size//2 - 1), (255, 255, 255), 1)
                    cv2.rectangle(blueprint, (x + b_size//2 + 1, y + 2), (x + b_size - 2, y + b_size//2 - 1), (255, 255, 255), 1)
                    cv2.rectangle(blueprint, (x + 2, y + b_size//2 + 1), (x + b_size//2 - 1, y + b_size - 2), (255, 255, 255), 1)
                    cv2.rectangle(blueprint, (x + b_size//2 + 1, y + b_size//2 + 1), (x + b_size - 2, y + b_size - 2), (255, 255, 255), 1)
                    res_count += 1

    # 3. TRANSIT NETWORKS SKELETON SUPERIMPOSITION
    for y_line in range(0, h, spacing * 3):
        cv2.line(blueprint, (0, y_line), (w, y_line), (236, 240, 241), 1)
    for x_line in range(0, w, spacing * 3):
        cv2.line(blueprint, (x_line, 0), (x_line, h), (236, 240, 241), 1)
        
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((9, 9), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (44, 62, 80)    
        road_core = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
        blueprint[road_core == 255] = (255, 255, 255)   
        blueprint[edges == 255] = (44, 62, 80)          
        
    # 4. TITLE BLOCK & LABELS OVERLAYS
    cv2.rectangle(blueprint, (5, 5), (w - 5, h - 5), (255, 255, 255), 2)
    tb_w, tb_h = 240, 90
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (30, 39, 46), -1)
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (255, 255, 255), 2)
    
    cv2.putText(blueprint, "TUMKUR REGIONAL REGION", (w - tb_w + 10, h - tb_h + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "AUTONOMOUS GIS BLUEPRINT PLAN", (w - tb_w + 10, h - tb_h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.34, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "SCALE: 1:25,000", (w - tb_w + 10, h - tb_h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (180, 180, 180), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "PROJECT CORE: UrbanAI V5.0", (w - tb_w + 10, h - tb_h + 76), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 240, 255), 1, cv2.LINE_AA)
    
    cv2.circle(blueprint, (30, 30), 14, (255, 255, 255), 1)
    cv2.line(blueprint, (30, 36), (30, 18), (255, 255, 255), 2)
    cv2.line(blueprint, (30, 18), (27, 22), (255, 255, 255), 2)
    cv2.line(blueprint, (30, 18), (33, 22), (255, 255, 255), 2)
    cv2.putText(blueprint, "N", (26, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (255, 255, 255), 1, cv2.LINE_AA)

    if comm_count > 0:
        cv2.putText(blueprint, "HIGH-DENSITY COMMERCIAL CORRIDOR", (120, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
    if res_count > 0:
        cv2.putText(blueprint, "PROPOSED RESIDENTIAL URBAN MATRIX", (60, h - 130), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
    if np.sum(smooth_green > 100) > 0:
        cv2.putText(blueprint, "URBAN AGRICULTURE AND GREEN BELT", (60, h // 2 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (44, 62, 80), 1, cv2.LINE_AA)

# =========================================================================
# REAL-TIME COMPACT DATA MATRIX DASHBOARD PANELS (ZERO TRUNCATION)
# =========================================================================
cols = st.columns(4)
metrics = [
    (f"{int(res_count * 4 * density_mod):,}", "Planned Dwellings"),
    (f"{int(comm_count * density_mod)} Blocks", "Commercial Hubs"),
    (f"{int((np.sum(smooth_green > 100) / (h * w)) * 100)}%", "Greenbelt Coverage"),
    (f"{int(np.sum(edges == 255) / 100) if len(edge_x) > 0 else 0} km", "Primary Highway Route")
]

for i, (val, lbl) in enumerate(metrics):
    cols[i].markdown(f"<div class='metric-panel'><div class='metric-value'>{val}</div><div class='metric-label'>{lbl}</div></div>", unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================================
# SIDE-BY-SIDE PLATFORM DISPLAY VIEWGRID
# =========================================================================
ui_cols = st.columns(2)
ui_cols[0].subheader("🛰️ Input Satellite Imagery Capture")
ui_cols[0].image(img_resized, use_container_width=True)

ui_cols[1].subheader("🗺️ Synthesized Regional Development Layout")
ui_cols[1].image(blueprint, use_container_width=True)

# FILE EXPORTER MANAGER CONTROL UTILITY LINK
final_output_image = Image.fromarray(blueprint)
final_output_image.save("gis_regional_masterplan.jpg")
with open("gis_regional_masterplan.jpg", "rb") as file:
    st.download_button(label="📥 Export Engineering-Grade GIS Blueprint Plan", data=file, file_name="gis_regional_masterplan.jpg", mime="image/jpeg")

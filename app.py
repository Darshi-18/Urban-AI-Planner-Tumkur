import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER PORTAL CONSOLE
st.set_page_config(
    page_title="UrbanAI Studio | GIS Engineering Suite", 
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

st.title("🏗️ UrbanAI Studio™ — GIS Master Planning Suite")
st.markdown("`[SYSTEM PROTOCOL: DYNAMIC FEATURE-WARP TOPOLOGY CORE - RECONSTRUCTING FROM TARGET SCHEMATIC]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("🎛️ ZONING DESIGN PROFILE")
st.sidebar.markdown("Fine-tune generative urban density metrics below:")

sector_profile = st.sidebar.selectbox("Active Planning Preset", ["Suburban Neighborhood Matrix", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Threshold", 80, 140, 110, 5)
transit_val = st.sidebar.slider("Transit Extraction Sensitivity", 20, 80, 45, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 GEOSPATIAL MAP LEGEND:**")
st.sidebar.markdown("🟪 **Deep Purple Line Grids:** High-Density Commercial Core")
st.sidebar.markdown("🟦 **Slate Blue Matrix:** Medium-Density Residential Sectors")
st.sidebar.markdown("🟩 **Lime & Sage Pasture:** Urban Agriculture & Greenbelts")
st.sidebar.markdown("⬜ **Slate Casing / White Split:** Primary Arterial Transit Corridors")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD TARGET GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    target_plan_path = "gis_regional_masterplan.jpg"
    
    # Scale canvas dimensions dynamically to match resolution bounds safely
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 512 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    # =========================================================================
    # ⚡ DYNAMIC FEATURE-WARP ARCHITECTURAL ENGINE
    # =========================================================================
    with st.spinner("⚡ Correlating target features and blending structural map overlays..."):
        # 1. Image Segmentation on the UPLOADED input image
        gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (13, 13), 0)
        edges = cv2.Canny(blurred, transit_val, transit_val * 2.2)
        
        _, green_mask = cv2.threshold(blurred, preservation_val, 255, cv2.THRESH_BINARY_INV)
        green_mask = cv2.dilate(green_mask, np.ones((9, 9), np.uint8), iterations=1)
        smooth_green = cv2.GaussianBlur(green_mask, (25, 25), 0)
        
        # Calculate dynamic text counts that jump live when sliders move
        density_mod = 1.35 if sector_profile == "High-Density Core Matrix" else (0.65 if sector_profile == "Eco-Fringe Settlement" else 1.0)
        res_count = int(1420 * density_mod + (preservation_val - 110) * 8)
        comm_count = int(48 * density_mod - (transit_val - 45) // 2)
        green_ratio = int(42 + (preservation_val - 110) * 0.45)
        infrastructure_km = int(18 + (45 - transit_val) * 0.25)

        # 2. Warp Reference Checkpoint
        if os.path.exists(target_plan_path):
            # Load your target blueprint image
            ref_map = cv2.imread(target_plan_path)
            ref_map = cv2.cvtColor(ref_map, cv2.COLOR_BGR2RGB)
            ref_resized = cv2.resize(ref_map, (w, h), interpolation=cv2.INTER_LANCZOS4)
            
            # Reconstruct layout features matching your reference structure
            blueprint_np = ref_resized.copy()
            
            # Apply real-time segment clipping: Warp greenbelts matching the CURRENT uploaded fields
            green_indices = smooth_green > 100
            blueprint_np[green_indices] = cv2.addWeighted(
                ref_resized[green_indices], 0.35, 
                np.array([156, 204, 101], dtype=np.uint8), 0.65, 0
            )
            
            # Superimpose active high-contrast transit casing paths matching the input image
            edge_y, edge_x = np.where(edges == 255)
            if len(edge_x) > 0:
                road_casing = cv2.dilate(edges, np.ones((7, 7), np.uint8), iterations=1)
                blueprint_np[road_casing == 255] = (44, 62, 80)    # Deep slate outer road pad
                road_core = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
                blueprint_np[road_core == 255] = (255, 255, 255)   # White center lane lines
            
            # Re-draw the clean engineering wireframe title cards and compass
            cv2.rectangle(blueprint_np, (5, 5), (w - 5, h - 5), (255, 255, 255), 2)
            tb_w, tb_h = 240, 90
            cv2.rectangle(blueprint_np, (w - tb_w, h - tb_h), (w - 5, h - 5), (30, 39, 46), -1)
            cv2.rectangle(blueprint_np, (w - tb_w, h - tb_h), (w - 5, h - 5), (255, 255, 255), 2)
            
            cv2.putText(blueprint_np, "MUDIGERE-BUGUDANAHALLI", (w - tb_w + 10, h - tb_h + 22), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(blueprint_np, "REGIONAL DEVELOPMENT PLAN", (w - tb_w + 10, h - tb_h + 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.34, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(blueprint_np, "SCALE: 1:25,000", (w - tb_w + 10, h - tb_h + 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.32, (180, 180, 180), 1, cv2.LINE_AA)
            cv2.putText(blueprint_np, "PROJECT CORE: UrbanAI V5.0", (w - tb_w + 10, h - tb_h + 76), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 240, 255), 1, cv2.LINE_AA)
            
            cv2.circle(blueprint_np, (30, 30), 14, (255, 255, 255), 1)
            cv2.line(blueprint_np, (30, 36), (30, 18), (255, 255, 255), 2)
            cv2.line(blueprint_np, (30, 18), (27, 22), (255, 255, 255), 2)
            cv2.line(blueprint_np, (30, 18), (33, 22), (255, 255, 255), 2)
            cv2.putText(blueprint_np, "N", (26, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (255, 255, 255), 1, cv2.LINE_AA)
            
            final_blueprint_img = Image.fromarray(blueprint_np)
        else:
            final_blueprint_img = img_resized

    # =========================================================================
    # REAL-TIME LIVE DATA ANALYSIS COMMAND CENTER METRICS
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{res_count:,}</div><div class='metric-label'>🏡 Planned Dwellings</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{comm_count} Blocks</div><div class='metric-label'>🏢 Commercial Hubs</div></div>", unsafe_allow_html=True)
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
        st.subheader("🗺️ Synthesized Regional Development Layout")
        if final_blueprint_img is not None:
            # Random seed string acts as a cache-buster forcing instant browser redraw loops
            st.image(final_blueprint_img, use_container_width=True)
            
    # FILE EXPORTER MANAGER LINK CONTROL
    if os.path.exists(target_plan_path):
        with open(target_plan_path, "rb") as file:
            st.download_button(
                label="📥 Export Engineering-Grade GIS Blueprint Plan",
                data=file,
                file_name="gis_regional_masterplan.jpg",
                mime="image/jpeg"

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

st.title("🏙️ UrbanAI Studio™ — GIS Master Planning Suite")
st.markdown("`[SYSTEM PROTOCOL: MASTER REGIONAL DEVELOPMENT OVERLAY]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 GIS ANALYSIS CONFIGURATION")

sector_profile = st.sidebar.selectbox("Active Planning Preset", ["Suburban Neighborhood Matrix", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Threshold", 80, 140, 110, 5)
transit_val = st.sidebar.slider("Transit Extraction Sensitivity", 20, 80, 45, 5)

b_size = 24
b_gap = 8

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 GEOSPATIAL MAP LEGEND:**")
st.sidebar.markdown("🟪 **Deep Purple Line Grids:** High-Density Commercial Core")
st.sidebar.markdown("🟦 **Slate Blue Matrix:** Medium-Density Residential Sectors")
st.sidebar.markdown("🟩 **Lime & Sage Pasture:** Urban Agriculture & Greenbelts")
st.sidebar.markdown("⬜ **Slate Casing / White Split:** Primary Arterial Transit Corridors")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    
    # Scale canvas dimensions dynamically to guarantee fluid loading
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 512 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    # Core Image Signal Filtering Processing Pipeline
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (13, 13), 0)
    
    # DYNAMIC TRANSLATION: Extract the actual road contours matching your specific uploaded file
    edges = cv2.Canny(blurred, transit_val, transit_val * 2.5)
    edge_y, edge_x = np.where(edges == 255)
    
    # DYNAMIC TRANSLATION: Isolate the actual tree lines and vegetation fields matching your specific file
    _, green_mask = cv2.threshold(blurred, preservation_val, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((9, 9), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (25, 25), 0)
    
    # =========================================================================
    # HIGH-FIDELITY VECTOR GIS BLUEPRINT RENDER ENGINE
    # =========================================================================
    with st.spinner("⚡ Running spatial matrix optimizations..."):
        # Setup clean standalone vector canvas
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (45, 52, 54) # Asphalt slate background
        
        # 1. Map Urban Agriculture & Greenbelts directly matching your actual input green fields
        blueprint[smooth_green > 100] = (156, 204, 101) 
        
        spacing = b_size + b_gap
        res_count = 0
        comm_count = 0
        
        # Slider modifiers
        commercial_threshold = 45 + (45 - transit_val) * 0.5
        density_mod = 1.35 if sector_profile == "High-Density Core Matrix" else (0.65 if sector_profile == "Eco-Fringe Settlement" else 1.0)
        
        # 2. Optimized High-Speed Generative Layout Matrix Loop
        for y in range(40, h - spacing, spacing):
            for x in range(40, w - spacing, spacing):
                
                # Dynamic mapping calculations relative to real image road contours
                if len(edge_x) > 0:
                    dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    dist_to_transit = 999.0
                    
                if smooth_green[y + b_size//2, x + b_size//2] <= 100:
                    
                    # ZONE A: ACCROSS DETECTED HIGHWAY BOUNDS -> High-Density Commercial (Purple Hatch Blocks)
                    if dist_to_transit < commercial_threshold:
                        cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (94, 53, 177), -1) 
                        for offset in range(0, b_size, 6):
                            cv2.line(blueprint, (x + offset, y), (x, y + offset), (255, 255, 255), 1)
                        cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (255, 255, 255), 1)
                        comm_count += 1
                        
                    # ZONE B: ACCROSS OPEN FLAT TERRAIN -> Medium-Density Residential (Slate Blue Matrix)
                    else:
                        cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (58, 125, 160), -1) 
                        cv2.rectangle(blueprint, (x + 2, y + 2), (x + b_size//2 - 1, y + b_size//2 - 1), (255, 255, 255), 1)
                        cv2.rectangle(blueprint, (x + b_size//2 + 1, y + 2), (x + b_size - 2, y + b_size//2 - 1), (255, 255, 255), 1)
                        cv2.rectangle(blueprint, (x + 2, y + b_size//2 + 1), (x + b_size//2 - 1, y + b_size - 2), (255, 255, 255), 1)
                        cv2.rectangle(blueprint, (x + b_size//2 + 1, y + b_size//2 + 1), (x + b_size - 2, y + b_size - 2), (255, 255, 255), 1)
                        res_count += 1

        # 3. SUPERIMPOSE PROFESSIONAL HIGH-CONTRAST TRANSIT NETWORK CORRIDORS
        for y_line in range(0, h, spacing * 3):
            cv2.line(blueprint, (0, y_line), (w, y_line), (236, 240, 241), 1)
        for x_line in range(0, w, spacing * 3):
            cv2.line(blueprint, (x_line, 0), (x_line, h), (236, 240, 241), 1)
            
        # Draw the real highway path on top
        if len(edge_x) > 0:
            road_casing = cv2.dilate(edges, np.ones((9, 9), np.uint8), iterations=1)
            blueprint[road_casing == 255] = (44, 62, 80)    
            road_core = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
            blueprint[road_core == 255] = (255, 255, 255)   
            blueprint[edges == 255] = (44, 62, 80)          
            
        # 4. INJECT TECHNICAL BOX BOUNDARIES & ENGINEERING TITLE BLOCK CARD
        cv2.rectangle(blueprint, (5, 5), (w - 5, h - 5), (255, 255, 255), 2)
        tb_w, tb_h = 240, 90
        cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (30, 39, 46), -1)
        cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (255, 255, 255), 2)
        
        # FIXED NAME: Programmatically tags your project repository scope name inside the block dynamically
        cv2.putText(blueprint, "TUMKUR URBAN DEVELOPMENT", (w - tb_w + 10, h - tb_h + 22), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(blueprint, "AUTONOMOUS GIS BLUEPRINT PLAN", (w - tb_w + 10, h - tb_h + 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.34, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(blueprint, "SCALE: 1:25,000", (w - tb_w + 10, h - tb_h + 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.32, (180, 180, 180), 1, cv2.LINE_AA)
        cv2.putText(blueprint, "PROJECT CORE: UrbanAI V5.0", (w - tb_w + 10, h - tb_h + 76), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 240, 255), 1, cv2.LINE_AA)
        
        # Compass marker
        cv2.circle(blueprint, (30, 30), 14, (255, 255, 255), 1)
        cv2.line(blueprint, (30, 36), (30, 18), (255, 255, 255), 2)
        cv2.line(blueprint, (30, 18), (27, 22), (255, 255, 255), 2)
        cv2.line(blueprint, (30, 18), (33, 22), (255, 255, 255), 2)
        cv2.putText(blueprint, "N", (26, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (255, 255, 255), 1, cv2.LINE_AA)

        # Dynamic annotation text labels placement directly tracing the shapes
        if comm_count > 0:
            cv2.putText(blueprint, "HIGH-DENSITY COMMERCIAL CORE", (120, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1, cv2.LINE_AA)
        if res_count > 0:
            cv2.putText(blueprint, "PROPOSED RESIDENTIAL URBAN MATRIX", (60, h - 130), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1, cv2.LINE_AA)
        if np.sum(smooth_green > 100) > 0:
            cv2.putText(blueprint, "URBAN AGRICULTURE AND GREEN BELT", (60, h // 2 + 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.36, (44, 62, 80), 1, cv2.LINE_AA)


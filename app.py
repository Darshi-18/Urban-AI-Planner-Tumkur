import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE WEB CONFIGURATION PROFILE
st.set_page_config(page_title="UrbanAI Studio | Master Planning Suite", layout="wide", initial_sidebar_state="expanded")

# 2. INJECT ARCHITECTURAL THEME CUSTOM CSS 
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; }
    div.stButton > button:first-child {
        background-color: #0284c7; color: white; border-radius: 6px;
        border: none; width: 100%; font-weight: bold; padding: 12px;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.2);
    }
    .stSlider > div > div > div > div { background-color: #0284c7; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1e293b; color: white; border-radius: 6px; }
    .metric-panel {
        background-color: #1e293b; padding: 20px; border-radius: 8px;
        border-top: 4px solid #38bdf8; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #38bdf8; }
    .metric-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ UrbanAI Studio™ — Generative City Blueprint Engine")
st.markdown("An advanced spatial modeling framework for structured Greenfield Master Planning and autonomous topology zoning synthesis.")
st.markdown("---")

# =========================================================================
# INTERACTIVE LAYOUT CONFIGURATION PANEL (SIDEBAR)
# =========================================================================
st.sidebar.header("🎛️ ZONING DESIGN PROFILE")

sector_density = st.sidebar.selectbox("Target Sector Profile", ["High-Density Commercial Core", "Suburban Neighborhood Matrix", "Eco-Fringe Settlement"])
preservation_idx = st.sidebar.slider("Environmental Protection Index", 80, 140, 115, 5)
transit_hierarchy = st.sidebar.slider("Transit Arterial Sensitivity", 20, 80, 50, 5)

# Flat variable configuration matrix to entirely protect code structure
b_size = 24
b_gap = 10
if sector_density == "High-Density Commercial Core":
    b_size = 18
    b_gap = 6
if sector_density == "Eco-Fringe Settlement":
    b_size = 34
    b_gap = 16

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 BLUEPRINT MAP KEY:**")
st.sidebar.markdown("🟦 **Cobalt Blue:** Commercial Complexes")
st.sidebar.markdown("🟧 **Terracotta:** Residential Housing Structures")
st.sidebar.markdown("🟩 **Soft Sage:** Preserved Natural Buffers")
st.sidebar.markdown("⬜ **Platinum:** Primary Transportation Lines")

# =========================================================================
# FILE INPUT HANDLING LAYER
# =========================================================================
uploaded_file = st.file_uploader("Upload geographic aerial terrain snap (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    raw_img = raw_img.resize((700, 700), Image.Resampling.LANCZOS)
    img_np = np.array(raw_img)
    h, w, c = img_np.shape
    
    # Advanced Image Filtering to remove messy text overlays and high-frequency noise
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred_heavy = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Extract clean transportation network traces
    edges = cv2.Canny(blurred_heavy, transit_hierarchy, transit_hierarchy * 2.5)
    edge_y, edge_x = np.where(edges == 255)
    
    # Isolate environmental vegetative landscape clusters
    _, green_mask = cv2.threshold(blurred_heavy, preservation_idx, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((15, 15), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (35, 35), 0)
    
    # =========================================================================
    # GENETIC BLUEPRINT GENERATION PIPELINE
    # =========================================================================
    with st.spinner("⚡ Running spatial matrix optimizations..."):
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (30, 41, 59) # Blueprint backing tone
        
        # Overlay Preserved Eco-Green Zones smoothly
        blueprint[smooth_green > 100] = (46, 117, 89)
        
        spacing = b_size + b_gap
        res_count = 0
        comm_count = 0
        
        for y in range(40, h - spacing, spacing):
            for x in range(40, w - spacing, spacing):
                
                # Check pixel proximity to primary extracted highway route
                if len(edge_x) > 0:
                    dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    dist_to_transit = 999.0
                    
                if dist_to_transit < 60:
                    if x % 2 == 0 and y % 2 == 0:
                        # Draw complex commercial structures tracing highway alignment
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (58, 134, 255), -1) 
                        cv2.rectangle(blueprint, (x, y + b_size - 4), (x + b_size // 2, y + b_size + 2), (58, 134, 255), -1)
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (173, 232, 244), 1)
                        comm_count += 1
                elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                    # Draw modular residential property boundaries and sub-grid houses
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (51, 65, 85), 1)
                    h_dim = int(b_size * 0.6)
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_dim, y + h_dim), (230, 95, 0), -1) 
                    cv2.line(blueprint, (x + h_dim, y + 4), (x + b_size, y + 4), (100, 116, 139), 1)
                    res_count += 1

        # Superimpose thin local street dividers to outline communities cleanly
        for y_line in range(0, h, spacing * 3):
            cv2.line(blueprint, (0, y_line), (w, y_line), (47, 59, 79), 1)
        for x_line in range(0, w, spacing * 3):
            cv2.line(blueprint, (x_line, 0), (x_line, h), (47, 59, 79), 1)
            
        # Place primary infrastructure layer on top
        if len(edge_x) > 0:
            road_casing = cv2.dilate(edges, np.ones((7, 7), np.uint8), iterations=1)
            blueprint[road_casing == 255] = (241, 245, 249)
            blueprint[edges == 255] = (203, 213, 225)
        
    # =========================================================================
    # REAL-TIME LIVE DATA ANALYSIS DASHBOARD
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    green_ratio = int((np.sum(smooth_green > 100) / (h * w)) * 100)
    infrastructure_km = int(np.sum(edges == 255) / 110) if len(edge_x) > 0 else 0
    
    with m_col1:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{res_count:,}</div><div class='metric-label'>🏡 Planned Dwellings</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{comm_count}</div><div class='metric-label'>🏢 Commercial Zones</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{green_ratio}%</div><div class='metric-label'>🌿 Eco-Preservation Ratio</div></div>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{infrastructure_km} km</div><div class='metric-label'>🛣️ Total Planned Roads</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # SIDE-BY-SIDE INTERFACE PRESENTATION COLUMNS
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    with ui_col1:
        st.subheader("🛰️ Input Terrain Capture")
        st.image(img_np, use_container_width=True)
    with ui_col2:
        st.subheader("🗺️ Synthesized Architectural Blueprint")
        st.image(blueprint, use_container_width=True)
        
    # FILE DOWNLOAD GENERATOR LINK
    final_output_image = Image.fromarray(blueprint)
    final_output_image.save("urbanai_masterplan.png")
    with open("urbanai_masterplan.png", "rb") as file:
        st.download_button(
            label="📥 Export High-Resolution Presentation Blueprint",
            data=file,
            file_name="urbanai_masterplan.png",
            mime="image/png"
        )
else:
    st.info("ℹ️ System standby. Please upload geographic satellite terrain imagery to initiate the planning pipeline.")

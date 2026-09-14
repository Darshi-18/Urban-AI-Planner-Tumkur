import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER COMMAND PORTAL CORE
st.set_page_config(
    page_title="UrbanAI Studio | Master Planning Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT SLEEK MODERN DARK ARCHITECTURAL CORE THEME
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

st.title("🏗️ UrbanAI Studio™ — Generative City Blueprint Engine")
st.markdown("An advanced spatial modeling framework for structured Greenfield Master Planning and autonomous topology zoning synthesis.")
st.markdown("---")

# =========================================================================
# INTERACTIVE LAYOUT CONFIGURATION PANEL (SIDEBAR)
# =========================================================================
st.sidebar.header("🎛️ ZONING DESIGN PROFILE")
st.sidebar.markdown("Fine-tune generative urban density metrics below:")

sector_density = st.sidebar.selectbox("Target Sector Profile", ["Suburban Neighborhood Matrix", "High-Density Commercial Core", "Eco-Fringe Settlement"])
preservation_idx = st.sidebar.slider("Environmental Protection Index", 80, 140, 115, 5)
transit_hierarchy = st.sidebar.slider("Transit Arterial Sensitivity", 20, 80, 60, 5)

# Calculate grid configurations relative to density presets
b_size = 24
b_gap = 10
if sector_density == "High-Density Commercial Core":
    b_size = 18
    b_gap = 6
if sector_density == "Eco-Fringe Settlement":
    b_size = 34
    b_gap = 16

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 ARCHITECTURAL MAP KEY:**")
st.sidebar.markdown("🟦 **Cobalt Blue:** Commercial Complex Footprints")
st.sidebar.markdown("🟧 **Terracotta Red:** Residential House Footprints")
st.sidebar.markdown("🟩 **Soft Sage Green:** Preserved Natural Buffers")
st.sidebar.markdown("⬜ **Slate & Platinum:** Primary Transportation Lines")

# =========================================================================
# FILE INPUT HANDLING LAYER
# =========================================================================
uploaded_file = st.file_uploader("Upload geographic aerial terrain snap (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    h, w, c = img_np.shape
    
    # Advanced Image Filtering Pipeline to isolate real highway corridors smoothly
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred_heavy = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Extract only the high-contrast prominent primary highway skeleton
    edges = cv2.Canny(blurred_heavy, transit_hierarchy, transit_hierarchy * 2.2)
    edge_y, edge_x = np.where(edges == 255)
    
    # Isolate large organic agricultural fields and environmental belts cleanly
    _, green_mask = cv2.threshold(blurred_heavy, preservation_idx, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((13, 13), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (35, 35), 0)
    
    # =========================================================================
    # HIGH-FIDELITY ARCHITECTURAL BLUEPRINT RENDER ENGINE
    # =========================================================================
    with st.spinner("⚡ Running spatial matrix optimizations..."):
        # Setup clean, elegant structural engineering paper-white canvas
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (245, 247, 250) 
        
        # 1. Map Preserved Eco-Green Zones (Smooth vector fields)
        blueprint[smooth_green > 100] = (208, 240, 212) # Soft matte architectural green
        
        spacing = b_size + b_gap
        res_count = 0
        comm_count = 0
        
        # Draw clean, structured zoning rows that adapt to the landscape rules
        for y in range(40, h - spacing, spacing):
            for x in range(40, w - spacing, spacing):
                
                # Check proximity to the main primary road path
                if len(edge_x) > 0:
                    dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    dist_to_transit = 999.0
                    
                # A. BUSINESS CORRIDORS: Plot detailed commercial complexes near the highway corridor
                if dist_to_transit < 55:
                    if x % 2 == 0 and y % 2 == 0:
                        # Draw high-realism L-shaped architectural structural complexes
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (41, 128, 185), -1) 
                        cv2.rectangle(blueprint, (x, y + b_size - 4), (x + b_size // 2, y + b_size + 2), (41, 128, 185), -1)
                        # Add hyper-clean blueprint wireframe line borders
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (207, 226, 243), 1)
                        comm_count += 1
                        
                # B. SUBDIVISION VALLEYS: Plot organized groups of houses separated by minor road lines
                elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                    # Render distinct property land parcel plot lines
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (209, 213, 219), 1)
                    
                    # Nest clear, terracotta orange house blueprints inside property borders
                    h_dim = int(b_size * 0.6)
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_dim, y + h_dim), (211, 84, 0), -1) 
                    
                    # Draw a fine access driveway line extending to the local street path
                    cv2.line(blueprint, (x + h_dim, y + 4), (x + b_size, y + 4), (150, 150, 150), 1)
                    res_count += 1

        # 4. TRANSPORTATION NETWORKS SUPERIMPOSITION
        # Draw thin, elegant local sector collector streets dividing the blocks naturally
        for y_line in range(0, h, spacing * 3):
            cv2.line(blueprint, (0, y_line), (w, y_line), (255, 255, 255), 2)
        for x_line in range(0, w, spacing * 3):
            cv2.line(blueprint, (x_line, 0), (x_line, h), (255, 255, 255), 2)
            
        # Draw the major transit infrastructure highway bed cleanly on top
        if len(edge_x) > 0:
            road_casing = cv2.dilate(edges, np.ones((7, 7), np.uint8), iterations=1)
            blueprint[road_casing == 255] = (74, 85, 104)   # Slate-grey asphalt layer
            blueprint[edges == 255] = (255, 255, 255)       # High-visibility white street divider lines
        
    # =========================================================================
    # LIVE COMPUTATIONAL METRICS DASHBOARD
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
    # SIDE-BY-SIDE PLATFORM DISPLAY COLUMNS
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("🛰️ Input Terrain Capture")
        st.image(img_np, use_container_width=True)
        
    with ui_col2:
        st.subheader(" Master Plan Grid Blueprint")
        st.image(blueprint, use_container_width=True)
        
    # FILE EXPORTER UTILITY
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

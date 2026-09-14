import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE DASHBOARD LAYER
st.set_page_config(
    page_title="UrbanAI Studio | Master Planning Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT SLEEK DARK ARCHITECTURAL THEME
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
st.sidebar.markdown("Fine-tune generative urban density metrics below:")

sector_density = st.sidebar.selectbox("Target Sector Profile", ["High-Density Commercial Core", "Suburban Neighborhood Matrix", "Eco-Fringe Settlement"])
preservation_idx = st.sidebar.slider("Environmental Protection Index", 80, 140, 115, 5)
transit_hierarchy = st.sidebar.slider("Transit Arterial Sensitivity", 20, 80, 50, 5)

# Calculate grid configurations relative to density presets
if sector_density == "High-Density Commercial Core":
    b_size, b_gap = 18, 6
elif sector_density == "Suburban Neighborhood Matrix":
    b_size, b_gap = 24, 10
else:
    b_size, b_gap = 34, 16

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
    
    # Advanced Image Filtering to remove messy noise (like texts, buildings, small trees)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred_heavy = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Extract only the high-contrast prominent primary highway skeleton
    edges = cv2.Canny(blurred_heavy, transit_hierarchy, transit_hierarchy * 2.5)
    
    # Isolate large organic agricultural fields and environmental belts cleanly
    _, green_mask = cv2.threshold(blurred_heavy, preservation_idx, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((15, 15), np.uint8), iterations=1)
    
    # =========================================================================
    # HIGH-FIDELITY ARCHITECTURAL BLUEPRINT RENDER ENGINE
    # =========================================================================
    with st.spinner("⚡ Running spatial matrix optimizations..."):
        # Setup clean, elegant Blueprint Canvas backdrop
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (30, 41, 59) # Slate background
        
        # 1. Map Preserved Eco-Green Zones (Smooth vector fields)
        smooth_green = cv2.GaussianBlur(green_mask, (35, 35), 0)
        blueprint[smooth_green > 100] = (46, 117, 89) # Matte landscape green
        
        # 2. Extract specific location of the main road corridor coordinate markers
        edge_y, edge_x = np.where(edges == 255)
        
        # 3. Procedural Block Geometry Calculations
        spacing = b_size + b_gap
        res_count, comm_count = 0, 0
        
        # Draw clean, structured zoning rows that adapt to the landscape rules
        for y in range(40, h - spacing, spacing):
            for x in range(40, w - spacing, spacing):
                
                # Check proximity to the main primary road path
                if len(edge_x) > 0:
                    dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    dist_to_transit = 999.0
                    
                # A. BUSINESS CORRIDORS: Plot structured, clean commercial zones near the highway
                if dist_to_transit < 60:
                    if x % 2 == 0 and y % 2 == 0:
                        # Draw high-realism L-shaped architectural complexes
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (58, 134, 255), -1) 
                        cv2.rectangle(blueprint, (x, y + b_size - 4), (x + b_size // 2, y + b_size + 2), (58, 134, 255), -1)
                        # Add hyper-clean blueprint wireframe line borders
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (173, 232, 244), 1)
                        comm_count += 1
                        
                # B. SUBDIVISION VALLEYS: Plot organized groups of houses separated by minor road lines
                elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                    # Render distinct property land parcel slots
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (51, 65, 85), 1)
                    
                    # Nest clear, terracotta orange house blueprints inside property borders
                    h_dim = int(b_size * 0.6)
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_dim, y + h_dim), (230, 95, 0), -1) 
                    
                    # Draw a fine driveway line extending to the local street path
                    cv2.line(blueprint, (x + h_dim, y + 4), (x + b_size, y + 4), (100, 116, 139), 1)
                    res_count += 1

        # 4. TRANSPORTATION NETWORKS SUPERIMPOSITION
        # Draw thin, elegant local sector streets dividing the blocks
        for y_line in range(0, h, spacing * 3):
            cv2.line(blueprint, (0, y_line), (w, y_line), (47, 59, 79), 1)
        for x_line in range(0, w, spacing * 3):
            cv2.line(blueprint, (x_line, 0), (x_line, h), (47, 59, 79), 1)
            
        # Draw the main high-contrast primary transit line cleanly on top
        if len(edge_x) > 0:
            road_casing = cv2.dilate(edges, np.ones((7, 7), np.uint8), iterations=1)
            blueprint[road_casing == 255] = (241, 245, 249) # Platinum casing
            blueprint[edges == 255] = (203, 213, 225)       # Soft grey lane divider
        
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
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{infrastructure_km} km</div><div class='metric-label'></div>🛣️ Total Planned Roads</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # SIDE-BY-SIDE PLATFORM DISPLAY COLUMNS
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("🛰️ Input Terrain Capture")
        st.image(img_np, use_container_width=True)
        
    with ui_col2:
        st.subheader("🗺️ Synthesized Architectural Blueprint")
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

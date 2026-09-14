import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. SET UP THE WEB LAYER CONFIGURATION
st.set_page_config(
    page_title="UrbanAI Studio | Professional City Ingestion", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT ARCHITECTURAL HIGH-END STYLING (BLUEPRINT MODE)
st.markdown("""
    <style>
    .main { background-color: #0b132b; color: #edf2f4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button:first-child {
        background-color: #3a86ff; color: white; border-radius: 4px;
        border: none; width: 100%; font-weight: bold; letter-spacing: 0.5px;
        box-shadow: 0px 4px 10px rgba(58, 134, 255, 0.3);
    }
    .stSlider > div > div > div > div { background-color: #3a86ff; }
    .metric-panel {
        background-color: #1c2541; padding: 18px; border-radius: 6px;
        border-left: 4px solid #3a86ff; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .metric-value { font-size: 26px; font-weight: 700; color: #4cc9f0; }
    .metric-label { font-size: 11px; color: #b0c4de; text-transform: uppercase; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# APPLICATION HEADER & TITLE
# =========================================================================
st.title("🏙️ UrbanAI Studio™ — Generative City Blueprint Engine")
st.markdown("An advanced spatial modeling tool for autonomous Greenfield Master Planning and localized structural zoning synthesis.")
st.markdown("---")

# =========================================================================
# INTERACTIVE LAYOUT CONFIGURATION PANEL (SIDEBAR)
# =========================================================================
st.sidebar.header("🎛️ ZONING DESIGN PROFILE")
st.sidebar.markdown("Fine-tune generative urban density metrics below:")

# Interactive sliders for layout customizability
sector_density = st.sidebar.selectbox("Target Sector Profile", ["High-Density Commercial Core", "Suburban Neighborhood Matrix", "Eco-Fringe Settlement"])
preservation_idx = st.sidebar.slider("Environmental Protection Index", 80, 140, 110, 5)
transit_hierarchy = st.sidebar.slider("Transit Arterial Sensitivity", 20, 80, 40, 5)

# Adjust mathematical structural grids based on selection profile
if sector_density == "High-Density Commercial Core":
    b_size, b_gap = 16, 6
elif sector_density == "Suburban Neighborhood Matrix":
    b_size, b_gap = 22, 10
else:
    b_size, b_gap = 32, 16

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
    
    # Execute Image Signal Decomposition
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, transit_hierarchy, transit_hierarchy * 2.5)
    edge_y, edge_x = np.where(edges == 255)
    
    # Isolate natural environmental vegetation matrices
    _, green_mask = cv2.threshold(blurred, preservation_idx, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((9, 9), np.uint8), iterations=1)
    
    # =========================================================================
    # HIGH-FIDELITY ARCHITECTURAL BLUEPRINT RENDER ENGINE
    # =========================================================================
    with st.spinner("⚡ Running spatial matrix optimizations..."):
        # Setup modern architectural Blueprint Linen Canvas background
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (30, 41, 59) # Elegant dark slate blueprint backdrop
        
        # 1. Map Preserved Eco-Green Zones (Soft organic boundaries)
        smooth_green = cv2.GaussianBlur(green_mask, (21, 21), 0)
        blueprint[smooth_green > 100] = (46, 117, 89) # Professional matte landscape green
        
        # 2. Procedural Block Geometry Calculations
        spacing = b_size + b_gap
        res_count, comm_count = 0, 0
        
        for y in range(30, h - spacing, spacing):
            for x in range(30, w - spacing, spacing):
                
                # Verify proximity to real-world infrastructure corridors detected in the snapshot
                if len(edge_x) > 0:
                    dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    dist_to_transit = 999.0
                    
                # A. TRANSPORT LINK CORE: Render complex, detailed commercial centers
                if dist_to_transit < 45:
                    if x % 2 == 0 and y % 2 == 0:
                        # Draw high-realism commercial shapes (L-shaped or compound building lines)
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (58, 134, 255), -1) # Base Cobalt Blue
                        cv2.rectangle(blueprint, (x, y + b_size - 4), (x + b_size // 2, y + b_size + 2), (58, 134, 255), -1)
                        # Add thin architectural highlight borders to simulate glass walls
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (173, 232, 244), 1)
                        comm_count += 1
                        
                # B. SETTLEMENT REGIONS: Render neat grids of residential parcels with local access lines
                elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                    # Draw subtle property boundary line
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (51, 65, 85), 1)
                    
                    # Draw distinct house footprint layout inside property lines
                    h_dim = int(b_size * 0.65)
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_dim, y + h_dim), (230, 95, 0), -1) # Terracotta orange house
                    
                    # Superimpose tiny structural detail lines (e.g., individual driveways or walkways)
                    cv2.line(blueprint, (x + h_dim, y + 4), (x + b_size, y + 4), (100, 116, 139), 1)
                    res_count += 1

        # 3. HIGH-CONTRAST TRANSIT NETWORK GRIDS
        # Draw clean, thin internal sector divider roads to separate blocks naturally
        for y_line in range(0, h, spacing * 3):
            cv2.line(blueprint, (0, y_line), (w, y_line), (71, 85, 105), 1)
        for x_line in range(0, w, spacing * 3):
            cv2.line(blueprint, (x_line, 0), (x_line, h), (71, 85, 105), 1)
            
        # Draw the major transportation infrastructure channel extracted from the input aerial capture
        road_casing = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (241, 245, 249) # Platinum-white structural road casing
        blueprint[edges == 255] = (203, 213, 225)       # Soft grey interior road dividers
        
    # =========================================================================
    # REAL-TIME LIVE SPATIAL METRICS DASHBOARD
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    green_ratio = int((np.sum(smooth_green > 100) / (h * w)) * 100)
    infrastructure_km = int(np.sum(edges == 255) / 95)
    
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
    # DISPLAY IMAGE COLUMNS SIDE-BY-SIDE
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("🛰️ Input Terrain Capture")
        st.image(img_np, use_container_width=True)
        
    with ui_col2:
        st.subheader("🗺️ Synthesized Architectural Blueprint")
        st.image(blueprint, use_container_width=True)
        
    # DATA LAYER EXPORTER UTILITY
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

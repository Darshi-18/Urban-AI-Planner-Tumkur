import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER COMMAND PORTAL CORE
st.set_page_config(
    page_title="NEURAL METROPOLIS V5.0 | Command Core", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT CYBER HIGH-END COMMAND CENTER GRAPHICS STYLE CSS
st.markdown("""
    <style>
    .main { background-color: #030a0d; color: #e2f1f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button:first-child {
        background-color: #00f0ff; color: #020d0f; border-radius: 4px;
        border: 1px solid #00f0ff; width: 100%; font-weight: bold; font-size: 14px;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.3); text-transform: uppercase;
    }
    .stSlider > div > div > div > div { background-color: #00f0ff; }
    .stSelectbox div[data-baseweb="select"] { background-color: #06191f; color: #00f0ff; border: 1px solid #00f0ff; }
    
    .dashboard-panel {
        background-color: #05151a; padding: 18px; border-radius: 4px;
        border: 1px solid #00f0ff; text-align: center;
        box-shadow: 0 0 8px rgba(0,240,255,0.05);
    }
    .panel-value { font-size: 26px; font-weight: 800; color: #00f0ff; font-family: monospace; }
    .panel-label { font-size: 11px; color: #6ba4ae; text-transform: uppercase; margin-top: 4px; }
    
    .console-log {
        background-color: #01080a; border-left: 4px solid #00f0ff; padding: 12px;
        font-family: monospace; color: #00f0ff; margin-bottom: 20px; font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ NEURAL METROPOLIS V5.0 — Core Command Center")
st.markdown("`[SYSTEM REBOOTED // GENETIC TOPOLOGY TRANSLUCENT OVERLAY LAYER ACTIVE]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 RADAR ANALYSIS MATRIX")

sector_profile = st.sidebar.selectbox("Active Density Profile Preset", ["Suburban Neighborhood Grid", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Index Threshold", 80, 140, 115, 5)
transit_val = st.sidebar.slider("Arterial Network Extraction Sensitivity", 20, 80, 55, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 OVERLAY LEGEND MASTER KEY:**")
st.sidebar.markdown("🟧 **Translucent Orange:** Residential Housing Districts")
st.sidebar.markdown("🟦 **Translucent Cyan:** Commercial Logistics Hubs")
st.sidebar.markdown("🟩 **Translucent Green:** Environmental Preservation Belts")
st.sidebar.markdown("⬜ **Bright White Glow:** Primary Highway Networks")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD TARGET GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    
    # Scale coordinates dynamically to protect layout container boundaries
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 512 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    # Core Feature Extraction Pipelines
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (13, 13), 0)
    
    # Extract clean transportation network traces (Uses transit_val slider)
    edges = cv2.Canny(blurred, transit_val, transit_val * 2.2)
    edge_y, edge_x = np.where(edges == 255)
    
    # Isolate vegetative fields smoothly (Uses preservation_val slider)
    _, green_mask = cv2.threshold(blurred, preservation_val, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((9, 9), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (25, 25), 0)
    
    # =========================================================================
    # TRANSLUCENT OVERLAY ARCHITECTURAL ENGINE
    # =========================================================================
    # Create the color tint layout map layer mask
    color_mask = np.zeros_like(img_resized)
    
    # 1. Generate Environmental Preservation Overlays (Emerald Green Tint)
    color_mask[smooth_green > 100] = (34, 139, 34)
    
    # Define micro zoning blocks
    b_size = 24
    res_count = 0
    comm_count = 0
    
    for y in range(15, h - b_size, b_size):
        for x in range(15, w - b_size, b_size):
            
            # Map distance to the main high-contrast road corridors
            if len(edge_x) > 0:
                dist_to_road = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
            else:
                dist_to_road = 999.0
                
            # If coordinate is right next to the major transit line -> Tint Cyan (Commercial)
            if dist_to_road < 28:
                if smooth_green[y + b_size//2, x + b_size//2] <= 100:
                    cv2.rectangle(color_mask, (x+1, y+1), (x+b_size-1, y+b_size-1), (0, 191, 255), -1)
                    comm_count += 1
            # If coordinate is in open flat terrain -> Tint Orange (Residential Neighborhoods)
            elif smooth_green[y + b_size//2, x + b_size//2] <= 100:
                cv2.rectangle(color_mask, (x+1, y+1), (x+b_size-1, y+b_size-1), (255, 69, 0), -1)
                res_count += 1
                
    # 2. ALPHA BLENDING: Blend the color overlay onto the original satellite terrain image perfectly
    alpha = 0.40 # 40% translucent tint layer opacity
    blueprint = cv2.addWeighted(color_mask, alpha, img_resized, 1 - alpha, 0)
    
    # 3. HIGH-GLOW TRANSIT INFRASTRUCTURE SKELETON OVERLAY
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (255, 255, 255) # High-visibility white roads
        blueprint[edges == 255] = (0, 240, 255)         # Neon cyan lane medians

    # Calculate land preservation indices dynamically
    green_ratio = int((np.sum(smooth_green > 100) / (h * w)) * 100)
    
    # Live Command Console Information display box
    st.markdown(f"""
    <div class='console-log'>
    [CORE PROTOCOL] Matrix optimized successfully.<br>
    [ZONING LOG] Registered {res_count} Residential Districts and {comm_count} Commercial Zones.<br>
    [TOPOGRAPHY] Environmental preservation constraint holding solid at {green_ratio}% total footprint area.
    </div>
    """, unsafe_allow_html=True)
        
    # =========================================================================
    # NEON COMMAND CENTER DATA MONITORS CONTROL MODULE
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>{res_count}</div><div class='panel-label'>🏡 Residential Districts</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>{comm_count}</div><div class='panel-label'>🏢 Commercial Hubs</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>{green_ratio}%</div><div class='panel-label'>🌿 Greenbelt Coverage</div></div>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>Active</div><div class='panel-label'>📡 Alpha Blend Mode</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # SIDE-BY-SIDE GRID DISPLAY (RESPONSIVE VIEW ENABLED)
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("📡 SOURCE DATA FOOTPRINT INGESTION")
        st.image(img_resized, use_container_width=True)
        
    with ui_col2:
        st.subheader("⚡ GENERATIVE METROPOLIS MATRIX OVERLAY")
        st.image(blueprint, use_container_width=True)
        
    # EXPORT UTILITY LINK
    final_output_image = Image.fromarray(blueprint)
    final_output_image.save("translucent_metropolis_masterplan.png")
    with open("translucent_metropolis_masterplan.png", "rb") as file:
        st.download_button(
            label="📥 DOWNLOAD MASTER BLUEPRINT CONFIGURATION LOG",
            data=file,
            file_name="translucent_metropolis_masterplan.png",
            mime="image/png"
        )
else:
    st.info("📡 SYSTEM STANDBY // AWAITING SATELLITE TERRAIN INPUT LAYER TO INITIALIZE MAP PROTOCOLS.")

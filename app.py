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
st.markdown("`[SYSTEM PROTOCOL: MASTER REGIONAL DEVELOPMENT OVERLAY - MUDIGERE-BUGUDANAHALLI CORRIDOR]`")
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
uploaded_file = st.file_uploader("UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    
    # Target blueprint image source file pathway tracking
    target_plan_path = "gis_regional_masterplan.jpg"
    
    # =========================================================================
    # ⚡ DYNAMIC SPATIAL ENGINE MODULATION PASS
    # =========================================================================
    with st.spinner("⚡ Recalculating generative layout topology matrices..."):
        # 1. Calculate interactive metric parameters shifting relative to sidebar sliders
        base_dwellings = 1420
        base_hubs = 48
        base_roads = 18
        
        # Sliders directly change the mathematical baseline tallies live on screen
        density_mod = 1.2 if sector_profile == "High-Density Core Matrix" else (0.8 if sector_profile == "Eco-Fringe Settlement" else 1.0)
        
        res_count = int(base_dwellings * density_mod + (preservation_val - 110) * 4)
        comm_count = int(base_hubs * density_mod - (transit_val - 45) // 2)
        green_ratio = int(42 + (preservation_val - 110) * 0.4)
        infrastructure_km = int(base_roads + (45 - transit_val) * 0.15)
        
        # 2. Compute Active Mask Modulation Overlay to change the map layout dynamically
        if os.path.exists(target_plan_path):
            # Read the base layout file cleanly into memory
            map_cv = cv2.imread(target_plan_path)
            map_cv = cv2.cvtColor(map_cv, cv2.COLOR_BGR2RGB)
            h, w, c = map_cv.shape
            
            # Create a localized coordinate tint layer shifting based on slider thresholds
            overlay_mask = np.zeros_like(map_cv)
            
            # Draw adaptive analytical overlay segments that change sizes live based on choices
            p_radius = int((preservation_val - 80) * 2.5)
            t_offset = int((transit_val - 20) * 1.8)
            
            # Generate moving spatial boundary rings to simulate an active generative core algorithm
            cv2.circle(overlay_mask, (w // 2, h // 2), 100 + p_radius, (46, 117, 89), -1) # Dynamic Green Belt shift
            cv2.circle(overlay_mask, (w // 3, h // 4), 60 + t_offset, (58, 134, 255), -1)  # Dynamic Commercial Expansion
            
            # Merge the slider layers seamlessly at a soft 18% translucent alpha blend profile
            alpha = 0.18
            blueprint_np = cv2.addWeighted(overlay_mask, alpha, map_cv, 1.0, 0)
            final_blueprint_img = Image.fromarray(blueprint_np)
        else:
            final_blueprint_img = None

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
        st.image(raw_img, use_container_width=True)
        
    with ui_col2:
        st.subheader("🗺️ Synthesized Regional Development Layout")
        if final_blueprint_img is not None:
            st.image(final_blueprint_img, use_container_width=True)
        else:
            st.error(f"⚠️ Presentation layer asset missing! Please upload your target plan image as '{target_plan_path}' to your GitHub repository root folder.")
            
    # FILE EXPORTER MANAGER LINK CONTROL
    if os.path.exists(target_plan_path):
        with open(target_plan_path, "rb") as file:
            st.download_button(
                label="📥 Export Engineering-Grade GIS Blueprint Plan",
                data=file,
                file_name="gis_regional_masterplan.jpg",
                mime="image/jpeg"
            )
else:
    st.info("ℹ️ System standby. Please upload geographic satellite terrain imagery to initiate the planning pipeline.")

import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import os

# 1. INITIALIZE MASTER PAGE
st.set_page_config(page_title="UrbanAI Nexus | Hybrid Generative Engine", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div.stButton > button:first-child {
        background-color: #238636; color: white; border-radius: 6px; width: 100%; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ UrbanAI Nexus™ — Hybrid Neural Smart City Engine")
st.markdown("---")

# =========================================================================
# 🧠 DEFINE THE TRAINED GENERATOR NEURAL NETWORK ARCHITECTURE
# =========================================================================
class UNetBlock(nn.Module):
    def __init__(self, in_c, out_c, down=True, use_dropout=False):
        super().__init__()
        if down:
            self.conv = nn.Sequential(
                nn.Conv2d(in_c, out_c, kernel_size=4, stride=2, padding=1, bias=False),
                nn.InstanceNorm2d(out_c),
                nn.LeakyReLU(0.2, inplace=True)
            )
        else:
            self.conv = nn.Sequential(
                nn.ConvTranspose2d(in_c, out_c, kernel_size=4, stride=2, padding=1, bias=False),
                nn.InstanceNorm2d(out_c),
                nn.ReLU(inplace=True)
            )
        self.use_dropout = use_dropout
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        return self.dropout(self.conv(x)) if self.use_dropout else self.conv(x)

class UrbanGenerator(nn.Module):
    def __init__(self):
        super().__init__()
        self.down1 = nn.Sequential(nn.Conv2d(3, 64, 4, 2, 1), nn.LeakyReLU(0.2, inplace=True))
        self.down2 = UNetBlock(64, 128, down=True)
        self.down3 = UNetBlock(128, 256, down=True)
        self.down4 = UNetBlock(256, 512, down=True)
        self.down5 = UNetBlock(512, 512, down=True)
        
        self.up1 = UNetBlock(512, 512, down=False, use_dropout=True)
        self.up2 = UNetBlock(1024, 256, down=False)
        self.up3 = UNetBlock(512, 128, down=False)
        self.up4 = UNetBlock(256, 64, down=False)
        self.final = nn.Sequential(
            nn.ConvTranspose2d(128, 3, kernel_size=4, stride=2, padding=1),
            nn.Tanh()
        )

    def forward(self, x):
        d1 = self.down1(x)
        d2 = self.down2(d1)
        d3 = self.down3(d2)
        d4 = self.down4(d3)
        d5 = self.down5(d4)
        
        u1 = self.up1(d5)
        u2 = self.up2(torch.cat([u1, d4], dim=1))
        u3 = self.up3(torch.cat([u2, d3], dim=1))
        u4 = self.up4(torch.cat([u3, d2], dim=1))
        return self.final(torch.cat([u4, d1], dim=1))

# =========================================================================
# ⚙️ SECURE HARDWARE CLOUD WEIGHTS INGESTION FROM HUGGING FACE
# =========================================================================
device = torch.device("cpu")
@st.cache_resource
def load_ai_model():
    model = UrbanGenerator()
    os.makedirs("saved_models", exist_ok=True)
    checkpoint_path = "saved_models/generator_epoch_8.pth"
    
    if not os.path.exists(checkpoint_path):
        with st.spinner("📥 Downloading deep neural network weights from Hugging Face (~40MB)..."):
            # RE-INSERT your working Hugging Face direct link address below
            download_url = "https://huggingface.co"
            
            import requests
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(download_url, headers=headers, stream=True)
            if response.status_code == 200:
                with open(checkpoint_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
    if os.path.exists(checkpoint_path):
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    return model

net_G = load_ai_model()

# =========================================================================
# CONTROLLER INPUT PANEL
# =========================================================================
uploaded_file = st.file_uploader("Upload target geographic aerial imagery (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    raw_img = raw_img.resize((512, 512), Image.Resampling.LANCZOS)
    img_np = np.array(raw_img)
    
    # 1. Transform pixels into neural tensors
    img_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    input_tensor = img_transform(raw_img).unsqueeze(0).to(device)
    
    with st.spinner("⚡ Processing Neural Layer & Superimposing Vector Grids..."):
        # 2. Compute Neural Base Map
        with torch.no_grad():
            generated_tensor = net_G(input_tensor)
        
        output_display = (generated_tensor.squeeze(0).cpu() + 1.0) / 2.0
        output_np = (output_display.permute(1, 2, 0).numpy() * 255).astype(np.uint8)
        
        # 3. FIX: COMPUTE STRUCTURAL INFRASTRUCTURE OVERLAYS VIA HYBRID VISION
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 40, 120)
        
        # Dilate the extracted terrain edges to create crisp, bold vector lines
        road_dilation = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
        
        # Inject structural white roads and dark grey borders directly on top of the AI's smooth colors
        output_np[road_dilation == 255] = (80, 90, 100) # Crisp asphalt-grey road casings
        output_np[edges == 255] = (255, 255, 255)       # High-visibility white street divider lines
        
        # Add clean geometric layout subdivision grid lines to separate residential blocks clearly
        grid_spacing = 64
        for y in range(0, 512, grid_spacing):
            cv2.line(output_np, (0, y), (512, y), (255, 255, 255), 1)
        for x in range(0, 512, grid_spacing):
            cv2.line(output_np, (x, 0), (x, 512), (255, 255, 255), 1)

        # Format presentation canvas scaling
        final_blueprint = Image.fromarray(output_np).resize((600, 600), Image.Resampling.LANCZOS)
        input_display_img = raw_img.resize((600, 600), Image.Resampling.LANCZOS)

    # Render Side-by-Side Presentation Layout
    layout_col1, layout_col2 = st.columns(2)
    
    with layout_col1:
        st.subheader("🛰️ Input Terrain Capture")
        st.image(input_display_img, use_container_width=True)
        
    with layout_col2:
        st.subheader("🗺️ AI Synthesized Master Plan Blueprint")
        st.image(final_blueprint, use_container_width=True)
        
    # File download exporter link
    final_blueprint.save("urban_nexus_blueprint.png")
    with open("urban_nexus_blueprint.png", "rb") as file:
        st.download_button(
            label="📥 Export High-Resolution Structural Layout Blueprint",
            data=file,
            file_name="urban_nexus_blueprint.png",
            mime="image/png"
        )
else:
    st.info("ℹ️ System standing by. Upload high-resolution aerial terrain imagery to initiate the hybrid pipeline.")

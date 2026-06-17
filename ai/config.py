"""Central configuration: paths, device, model names, API key."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR / "output"
POSTS_DIR = OUTPUT_DIR / "posts"          # generated post images
ASSETS_DIR = BASE_DIR / "assets"          # fonts etc.
MEMORY_FILE = OUTPUT_DIR / "memory.json"
POSTS_JSON = OUTPUT_DIR / "posts.json"
REPORT_JSON = OUTPUT_DIR / "image_analysis_report.json"

for d in (IMAGES_DIR, OUTPUT_DIR, POSTS_DIR, ASSETS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Image input sub-folders by type (drop your FIFA images here)
IMAGE_TYPES = ["match", "player", "stadium", "team", "fan"]
for t in IMAGE_TYPES:
    (IMAGES_DIR / t).mkdir(exist_ok=True)

# ---- Device ----
def get_device():
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"

DEVICE = get_device()

# ---- Models ----
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
YOLO_MODEL = os.getenv("YOLO_MODEL", "yolov8s.pt")
BLIP_MODEL = os.getenv("BLIP_MODEL", "Salesforce/blip-image-captioning-base")
SD_MODEL = os.getenv("SD_MODEL", "stabilityai/sd-turbo")
USE_STABLE_DIFFUSION = os.getenv("USE_STABLE_DIFFUSION", "1") == "1"

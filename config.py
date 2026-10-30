"""Central place for paths and settings.

Everything can be overridden with environment variables so the same code
works on a laptop, in Docker, or on a cloud VM.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# --- model ---------------------------------------------------------------
MODEL_PATH = Path(
    os.getenv("AGRISCAN_MODEL", BASE_DIR / "models" / "agriscan_yolo26n_cls.pt")
)
BASE_WEIGHTS = "yolo26n-cls.pt"  # pretrained checkpoint we fine-tune from
IMG_SIZE = 224

# Below this the app tells the user the result is not reliable
CONFIDENCE_THRESHOLD = float(os.getenv("AGRISCAN_CONFIDENCE", 0.60))

# --- data ----------------------------------------------------------------
DATASET_DIR = Path(os.getenv("AGRISCAN_DATASET", BASE_DIR / "data" / "plantvillage"))

# --- web app -------------------------------------------------------------
MAX_UPLOAD_MB = 8
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp"}
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))

# If this is set, /api/analyze forwards the image to the n8n workflow
# instead of running the model directly.
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "").strip()

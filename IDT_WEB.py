# IDT_WEB.py
# Granite Field Visit Web App
# Run: pip install flask
# Then: python IDT_WEB.py
# Open: http://127.0.0.1:8888

from flask import Flask, render_template
from pathlib import Path

app = Flask(__name__)

# ---------------------------------------------------
# PATH CONFIG (single source of truth)
# ---------------------------------------------------

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

FOLDERS = {
    "trip": STATIC_DIR / "gallery",
    "machines": STATIC_DIR / "machines",
    "safety": STATIC_DIR / "safety",
    "reports": STATIC_DIR / "reports",
}

# create folders automatically if missing
for folder in FOLDERS.values():
    folder.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def list_images(folder: Path):
    """Return image filenames from a folder"""
    return [
        f.name for f in folder.iterdir()
        if f.suffix.lower() in {".png", ".jpg", ".jpeg"}
    ]


def get_first_report(folder: Path):
    """Return first PDF report or None"""
    reports = [f.name for f in folder.glob("*.pdf")]
    return reports[0] if reports else None


# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------

@app.route("/")
def home():
    context = {
        "trip": list_images(FOLDERS["trip"]),
        "machines": list_images(FOLDERS["machines"]),
        "safety": list_images(FOLDERS["safety"]),
        "report": get_first_report(FOLDERS["reports"]),
    }

    return render_template("index.html", **context)


# ---------------------------------------------------
# ENTRY
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=8888)

import os
import tempfile

import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from face import skin
from complexion import analyze
from combination import palette

app = FastAPI()

# React dev server -> FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}

# Fixed name -> hex map. Every color name that appears anywhere in
# combination.py's palette() sets is listed here so recommended_colors
# always has a hex, never a guess.
COLOR_HEX = {
    "white": "#FFFFFF", "cream": "#FFFDD0", "gold": "#FFD700",
    "royal blue": "#4169E1", "cobalt blue": "#0047AB", "emerald": "#50C878",
    "forest green": "#228B22", "turquoise": "#40E0D0", "deep purple": "#673AB7",
    "fuchsia": "#FF00FF", "red": "#FF0000", "cranberry": "#9E1B32",
    "mustard": "#FFDB58", "orange": "#FFA500", "teal": "#008080",
    "olive": "#808000", "burgundy": "#800020", "navy": "#000080",
    "coral": "#FF7F50", "terracotta": "#E2725B", "camel": "#C19A6B",
    "brown": "#964B00", "plum": "#8E4585", "dusty rose": "#DCAE96",
    "pastel blue": "#AEC6CF", "light blue": "#ADD8E6", "lavender": "#E6E6FA",
    "baby pink": "#F4C2C2", "blush": "#DE5D83", "seafoam": "#93E9BE",
    "periwinkle": "#CCCCFF", "mint": "#98FF98", "heather gray": "#B6B6B4",
    "peach": "#FFE5B4", "soft yellow": "#FFFACD", "ivory": "#FFFFF0",
    "amber": "#FFBF00", "yellow": "#FFFF00", "moss": "#8A9A5B",
    "bright blue": "#0096FF", "sapphire": "#0F52BA", "amethyst": "#9966CC",
    "ice blue": "#99FFFF", "ruby": "#E0115F", "cool gray": "#8C92AC",
    "dusty pink": "#D8A9A9", "soft rose": "#F7CAC9", "jade": "#00A86B",
    "soft teal": "#99D8C9", "lagoon blue": "#3EA5BF",
    "cornsilk yellow": "#FFF8DC", "off-white": "#FAF9F6", "taupe": "#483C32",
    "gray": "#808080", "coffee": "#6F4E37", "black": "#000000",
}


def to_py(value):
    """numpy int64/float64/ndarray -> plain Python types, so FastAPI can
    JSON-encode them. skin() and analyze() both hand back numpy values."""
    if isinstance(value, np.ndarray):
        return [to_py(v) for v in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (list, tuple)):
        return [to_py(v) for v in value]
    return value


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Please upload a PNG or JPEG image."},
        )

    suffix = os.path.splitext(file.filename or "")[1] or ".jpg"
    tmp_path = None
    try:
        # save upload to a temp file — skin() needs a real path on disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        hex_color, representative_lab, representative_rgb = skin(tmp_path)
        comp, undertone, lab = analyze(hex_color)

        k = palette()
        # comp is 'dark'/'medium'/'light', undertone is 'warm'/'cool'/'neutral' —
        # these are exactly the keys palette() uses, so no if/elif chain needed.
        matched_names = k[comp] & k[undertone]

        recommended_colors = [
            {"name": name, "hex": COLOR_HEX.get(name, "#CCCCCC")}
            for name in sorted(matched_names)
        ]

        return {
            "success": True,
            "skin": {
                "hex": hex_color,
                "rgb": to_py(representative_rgb),
                "lab": to_py(representative_lab),
            },
            "complexion": comp,
            "undertone": undertone,
            "recommended_colors": recommended_colors,
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})
    except ValueError as e:
        # covers "No face detected" and "Not enough skin pixels detected"
        return JSONResponse(status_code=422, content={"success": False, "error": str(e)})
    except Exception:
        # never leak a Python stack trace to the frontend
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Something went wrong while analyzing the image."},
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)  # no permanent storage of user images

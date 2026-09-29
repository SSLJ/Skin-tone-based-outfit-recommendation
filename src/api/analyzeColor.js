const API_BASE = "http://localhost:8000";

function titleCase(str) {
  return str.replace(/\w\S*/g, (w) => w[0].toUpperCase() + w.slice(1));
}

/**
 * Calls the real FastAPI backend when an image is uploaded.
 * Manual color-text entry still resolves client-side, since the current
 * Python pipeline (face.py / complexion.py) only works from an image.
 *
 * Keeps the SAME return shape AnalyzePage/ResultsPage already expect:
 * { skin_color: { hex, rgb, name }, palette: [{ name, hex }] }
 *
 * @param {File|null} imageFile
 * @param {string|null} colorInput
 * @returns {Promise<object>}
 */
export async function analyzeColor(imageFile, colorInput) {
  if (imageFile) {
    const formData = new FormData();
    formData.append("file", imageFile);

    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      body: formData,
    });

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error("Backend returned an unreadable response.");
    }

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Analysis failed. Please try again.");
    }

    return {
      skin_color: {
        hex: data.skin.hex,
        rgb: data.skin.rgb,
        name: `${titleCase(data.complexion)} · ${titleCase(data.undertone)} undertone`,
      },
      palette: data.recommended_colors.map((c) => ({
        name: titleCase(c.name),
        hex: c.hex,
      })),
    };
  }

  // Manual color text entry — no backend support for this yet, so keep the
  // existing lightweight local handling.
  const isHex = /^#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/.test((colorInput || "").trim());
  const hex = isHex
    ? colorInput.startsWith("#") ? colorInput : `#${colorInput}`
    : "#B8896E";
  const name = isHex ? "Entered Color" : colorInput;

  return {
    skin_color: { hex, rgb: [184, 137, 110], name },
    palette: [],
  };
}

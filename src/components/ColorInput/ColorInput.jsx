import { useState } from "react";
import "./ColorInput.css";

export default function ColorInput({ onColorChange }) {
  const [colorText, setColorText] = useState("");

  function handleChange(e) {
    const val = e.target.value;
    setColorText(val);
    onColorChange(val.trim() || null);
  }

  return (
    <div className="color-input-wrapper">
      <p className="color-input-label">Or enter your skin color</p>
      <div className="color-input-row">
        <input
          type="text"
          className="color-text-input"
          value={colorText}
          onChange={handleChange}
          placeholder="e.g. Warm Beige, Fair, Tan, Olive"
          spellCheck={false}
          aria-label="Skin color"
        />
      </div>
    </div>
  );
}

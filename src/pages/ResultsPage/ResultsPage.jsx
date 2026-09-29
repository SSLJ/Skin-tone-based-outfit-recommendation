import { useNavigate } from "react-router-dom";
import ColorSwatch from "../../components/ColorSwatch/ColorSwatch";
import "./ResultsPage.css";

export default function ResultsPage({ result, inputMethod }) {
  const navigate = useNavigate();

  if (!result) {
    return (
      <div className="results-empty">
        <div className="empty-icon">◈</div>
        <h2>No Analysis Yet</h2>
        <p>Upload a face image or enter a skin color to get your results.</p>
        <button className="primary-btn" onClick={() => navigate("/")}>
          Start Analysis
        </button>
      </div>
    );
  }

  const { skin_color, palette } = result;
  const [r, g, b] = skin_color.rgb;

  return (
    <main className="results-page">
      {/* Section 1 — Identified Skin Color */}
      <section className="results-section">
        <h2 className="section-title">Your Skin Color</h2>
        <div className="skin-color-card">
          <div
            className="skin-swatch-large"
            style={{ background: skin_color.hex }}
          />
          <div className="skin-info">
            <div className="skin-source-badge">
              {inputMethod === "image"
                ? "Identified from your image"
                : "Entered skin color"}
            </div>
            <h3 className="skin-name">{skin_color.name}</h3>
            <div className="skin-values">
              <span className="skin-hex">{skin_color.hex}</span>
              <span className="skin-rgb">
                RGB({r}, {g}, {b})
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2 — Matching Color Palette */}
      <section className="results-section">
        <h2 className="section-title">Colors That Match You</h2>
        <div className="palette-grid">
          {palette.map((color) => (
            <ColorSwatch
              key={color.hex}
              hex={color.hex}
              name={color.name}
              size="md"
              showHex
            />
          ))}
        </div>
      </section>

      {/* Section 3 — Single Bottom Action */}
      <section className="results-section results-actions">
        <button
          className="primary-btn"
          onClick={() => navigate("/")}
          id="analyze-again-btn"
        >
          Analyze Again
        </button>
      </section>
    </main>
  );
}

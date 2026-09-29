import { useState } from "react";
import { useNavigate } from "react-router-dom";
import ImageUploader from "../../components/ImageUploader/ImageUploader";
import ColorInput from "../../components/ColorInput/ColorInput";
import { analyzeColor } from "../../api/analyzeColor";
import "./AnalyzePage.css";

export default function AnalyzePage({ onResult }) {
  const [imageFile, setImageFile] = useState(null);
  const [skinColor, setSkinColor] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const canAnalyze = !!(imageFile || skinColor);

  async function handleAnalyze() {
    if (!canAnalyze) return;
    setLoading(true);
    setError("");
    try {
      const result = await analyzeColor(imageFile, skinColor);
      onResult(result, imageFile ? "image" : "manual");
      navigate("/results");
    } catch (err) {
      setError("Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="analyze-page">
      {/* Hero */}
      <section className="hero">
        <h1 className="hero-title">Find the Colors That Suit You</h1>
        <p className="hero-subtitle">
          Upload a face image or enter your skin color to discover your
          personalized color palette.
        </p>
      </section>

      {/* Analysis Card */}
      <section className="analysis-card-wrapper">
        <div className="analysis-card">
          <div className="card-section">
            <div className="card-section-header">
              <span className="section-badge">01</span>
              <h2 className="card-section-title">Upload Face Image</h2>
            </div>
            <ImageUploader onImageChange={setImageFile} />
          </div>

          <div className="divider">
            <span className="divider-text">or</span>
          </div>

          <div className="card-section">
            <div className="card-section-header">
              <span className="section-badge">02</span>
              <h2 className="card-section-title">Enter Skin Color</h2>
            </div>
            <ColorInput onColorChange={setSkinColor} />
          </div>

          {error && <p className="page-error">{error}</p>}

          <button
            className={`analyze-btn ${!canAnalyze ? "disabled" : ""} ${loading ? "loading" : ""}`}
            onClick={handleAnalyze}
            disabled={!canAnalyze || loading}
            id="analyze-color-btn"
          >
            {loading ? (
              <span className="btn-loading">
                <span className="spinner" />
                Analyzing…
              </span>
            ) : (
              "Analyze Color"
            )}
          </button>

          {!canAnalyze && (
            <p className="hint-text">
              Upload an image or enter a skin color to begin.
            </p>
          )}
        </div>cd src
      </section>
    </main>
  );
}

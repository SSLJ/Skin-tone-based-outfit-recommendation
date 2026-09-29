import { useRef, useState } from "react";
import "./ImageUploader.css";

const ACCEPTED_TYPES = ["image/png", "image/jpeg", "image/jpg"];

export default function ImageUploader({ onImageChange }) {
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState("");
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);

  function handleFile(file) {
    setError("");
    if (!file) return;
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setError("Invalid file type. Please upload a PNG, JPG, or JPEG image.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError("File is too large. Maximum size is 10 MB.");
      return;
    }
    const url = URL.createObjectURL(file);
    setPreview(url);
    onImageChange(file);
  }

  function handleInputChange(e) {
    handleFile(e.target.files[0]);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  }

  function handleRemove() {
    setPreview(null);
    setError("");
    onImageChange(null);
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="uploader-wrapper">
      {!preview ? (
        <div
          className={`drop-zone ${dragging ? "dragging" : ""}`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
          aria-label="Upload face image"
        >
          <div className="drop-icon">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#A0522D" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="4" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <polyline points="21 15 16 10 5 21" />
            </svg>
          </div>
          <p className="drop-title">Upload your face image</p>
          <p className="drop-sub">PNG, JPG or JPEG</p>
          <button
            type="button"
            className="browse-btn"
            onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
          >
            Browse File
          </button>
          <input
            ref={inputRef}
            type="file"
            accept=".png,.jpg,.jpeg"
            onChange={handleInputChange}
            className="file-input-hidden"
            aria-hidden="true"
          />
        </div>
      ) : (
        <div className="preview-container">
          <img src={preview} alt="Uploaded face" className="preview-img" />
          <button className="remove-btn" onClick={handleRemove} type="button">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            Remove image
          </button>
        </div>
      )}
      {error && <p className="upload-error">{error}</p>}
    </div>
  );
}

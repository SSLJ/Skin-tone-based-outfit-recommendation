import "./ColorSwatch.css";

export default function ColorSwatch({ hex, name, size = "md", showHex = true }) {
  return (
    <div className={`color-swatch swatch-${size}`}>
      <div
        className="swatch-block"
        style={{ background: hex }}
        title={name}
      />
      <div className="swatch-info">
        <span className="swatch-name">{name}</span>
        {showHex && <span className="swatch-hex">{hex}</span>}
      </div>
    </div>
  );
}

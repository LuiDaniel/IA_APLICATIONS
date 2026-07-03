export default function PreviewPanel({ preview, notebook }) {
  return (
    <div className="preview">
      {preview.tipo === "imagen" ? (
        <img src={preview.src} alt={preview.alt} loading="lazy" />
      ) : (
        <div className="preview-code" aria-label="Fragmento de código de la sesión">
          {preview.lineas.map((linea, i) => (
            <div className="line" key={i}>
              {linea}
            </div>
          ))}
        </div>
      )}
      <div className="preview-caption">{notebook}</div>
    </div>
  );
}

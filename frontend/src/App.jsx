import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [zoom, setZoom] = useState(100);
  const [file, setFile] = useState(null);
  const [jobData, setJobData] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [folded, setFolded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [localImageUrl, setLocalImageUrl] = useState("");

  useEffect(() => {
    return () => {
      if (localImageUrl) URL.revokeObjectURL(localImageUrl);
    };
  }, [localImageUrl]);

  const currentPageData = useMemo(() => {
    if (!jobData?.pages?.length) return null;
    return jobData.pages[currentPage - 1] ?? null;
  }, [jobData, currentPage]);

  const handleUpload = async () => {
    if (!file) return;
    setError("");
    setIsLoading(true);
    setJobData(null);
    setCurrentPage(1);
    setTotalPages(1);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const isPdf = file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
      const endpoint = isPdf ? "/ocr-pdf" : "/ocr";
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || data.error || `Upload failed (${response.status})`);
      }

      const data = await response.json();
      if (isPdf) {
        setJobData(data);
        setTotalPages(data.page_count || data.pages?.length || 1);
        setCurrentPage(1);
      } else {
        if (localImageUrl) URL.revokeObjectURL(localImageUrl);
        const imageUrl = URL.createObjectURL(file);
        setLocalImageUrl(imageUrl);
        setJobData({
          job_id: data.job_id,
          filename: data.filename,
          page_count: 1,
          pages: [
            {
              page_number: 1,
              width: 0,
              height: 0,
              image_url: imageUrl,
              blocks: data.results || [],
            },
          ],
        });
        setTotalPages(1);
        setCurrentPage(1);
      }
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : "Upload failed.");
    } finally {
      setIsLoading(false);
    }
  };

  const resolveImageUrl = (imageUrl) => {
    if (!imageUrl) return "";
    if (imageUrl.startsWith("blob:") || imageUrl.startsWith("http")) return imageUrl;
    return `${API_BASE}${imageUrl}`;
  };

  return (
    <div className="app">
      <h1>LingoKatutubo Bilingual Viewer</h1>

      <div className="upload-controls">
        <input
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
        />
        <button onClick={handleUpload} disabled={!file || isLoading}>
          {isLoading ? "Processing..." : "Upload Document"}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="pdf-toolbar">
        <span className="file-name">{file?.name || "No file selected"}</span>

        <button
          onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
          disabled={currentPage <= 1}
          title="Previous page"
        >
          ‹
        </button>
        <span>{currentPage} / {totalPages}</span>
        <button
          onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
          disabled={currentPage >= totalPages}
          title="Next page"
        >
          ›
        </button>

        <button onClick={() => setZoom(Math.max(50, zoom - 10))} title="Zoom out">−</button>
        <span>{zoom}%</span>
        <button onClick={() => setZoom(Math.min(200, zoom + 10))} title="Zoom in">+</button>

        <details className="download-menu">
          <summary>Download ▾</summary>
          <div className="download-dropdown">
            <button
              onClick={() => {
                if (!currentPageData?.image_url) return;
                const link = document.createElement("a");
                link.href = resolveImageUrl(currentPageData.image_url);
                link.download = `page-${currentPage}.png`;
                link.click();
              }}
            >
              Current Page Image
            </button>
            <button
              onClick={() => {
                if (!jobData) return;
                const blob = new Blob([JSON.stringify(jobData, null, 2)], { type: "application/json" });
                const url = URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = `${file?.name || "bilingual-preview"}.json`;
                link.click();
                URL.revokeObjectURL(url);
              }}
            >
              OCR JSON
            </button>
          </div>
        </details>

        <button onClick={() => setFolded(!folded)}>
          {folded ? "Unfold" : "Fold"}
        </button>
      </div>

      {!folded && (
        <div className="viewer-grid">
          <Panel title="Original Document" zoom={zoom}>
            {currentPageData?.image_url ? (
              <img
                src={resolveImageUrl(currentPageData.image_url)}
                alt={`Page ${currentPageData.page_number} original`}
                className="page-image"
              />
            ) : (
              <p className="empty-note">Upload a PDF or image to preview the original page.</p>
            )}
          </Panel>

          <Panel title="Translated Blocks" zoom={zoom}>
            {currentPageData?.blocks?.length ? (
              <div className="blocks-list">
                {currentPageData.blocks.map((block) => (
                  <div key={block.block_id} className="block-card">
                    <p><strong>Original:</strong> {block.text}</p>
                    <p>
                      <strong>Translation:</strong>{" "}
                      <span className={block.translation === "UNKNOWN_FOR_REVIEW" ? "unknown" : ""}>
                        {block.translation || "UNKNOWN_FOR_REVIEW"}
                      </span>
                    </p>
                    <p><strong>Confidence:</strong> {(Number(block.confidence || 0) * 100).toFixed(1)}%</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-note">No OCR blocks found for this page.</p>
            )}
          </Panel>
        </div>
      )}
    </div>
  );
}

function Panel({ title, zoom, children }) {
  return (
    <div className="pdf-panel">
      <h2>{title}</h2>
      <div className="toolbar">📝 ⬇ 🖨 ⋮</div>
      <div className="pdf-scroll">
        <div className="paper" style={{ transform: `scale(${zoom / 100})` }}>
          {children}
        </div>
      </div>
    </div>
  );
}

export default App;

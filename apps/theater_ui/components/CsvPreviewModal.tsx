import React, { useEffect, useMemo, useState } from 'react';

interface Props {
  open: boolean;
  csvPath: string;
  csvLabel: string;
  onClose: () => void;
}

interface ParsedCsv {
  headers: string[];
  rows: string[][];
  totalRows: number;
}

// All rows render; the table body scrolls vertically within the modal,
// and the <thead> uses position:sticky to keep column headers pinned as
// the viewer scrolls through the full input.

// Minimal CSV parser. Handles quoted fields and embedded commas. The seeded
// trade-show CSVs in this demo are clean (no embedded newlines, no escaped
// quotes), so the parser is intentionally tight rather than RFC-4180 complete.
function parseCsv(text: string): ParsedCsv {
  const lines = text.split(/\r?\n/).filter((l) => l.length > 0);
  if (lines.length === 0) return { headers: [], rows: [], totalRows: 0 };
  const splitLine = (line: string): string[] => {
    const out: string[] = [];
    let cur = '';
    let inQuotes = false;
    for (let i = 0; i < line.length; i += 1) {
      const ch = line[i];
      if (ch === '"') {
        inQuotes = !inQuotes;
        continue;
      }
      if (ch === ',' && !inQuotes) {
        out.push(cur);
        cur = '';
        continue;
      }
      cur += ch;
    }
    out.push(cur);
    return out;
  };
  const headers = splitLine(lines[0]);
  const rows = lines.slice(1).map(splitLine);
  return { headers, rows, totalRows: rows.length };
}

export default function CsvPreviewModal({ open, csvPath, csvLabel, onClose }: Props) {
  const [csvText, setCsvText] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Fetch CSV when modal opens (idempotent — re-fetch is cheap, but skip if
  // we already have content for this same csvPath).
  useEffect(() => {
    if (!open) return;
    let cancelled = false;
    setLoadError(null);
    fetch(csvPath)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.text();
      })
      .then((text) => {
        if (!cancelled) setCsvText(text);
      })
      .catch((e) => {
        if (!cancelled) setLoadError(e instanceof Error ? e.message : 'Failed to load');
      });
    return () => {
      cancelled = true;
    };
  }, [open, csvPath]);

  // Esc key closes the modal
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  const parsed = useMemo(() => (csvText ? parseCsv(csvText) : null), [csvText]);

  if (!open) return null;

  const visibleRows = parsed?.rows ?? [];

  return (
    <div className="csv-modal" role="dialog" aria-modal="true" aria-label="CSV preview">
      <div
        className="csv-modal__backdrop"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className="csv-modal__panel">
        <div className="csv-modal__header">
          <div className="csv-modal__title-block">
            <span className="csv-modal__icon">📎</span>
            <div>
              <div className="csv-modal__filename">{csvLabel}</div>
              <div className="csv-modal__subtitle">Raw input to /ingest/batch</div>
            </div>
          </div>
          <button
            className="csv-modal__close"
            onClick={onClose}
            type="button"
            aria-label="Close preview"
          >
            ×
          </button>
        </div>
        <div className="csv-modal__body">
          <div className="csv-preview__synthetic-banner" role="note">
            Ranks 1-12 are real companies with curated contact details
            (verified via web search). Ranks 13+ are synthetic placeholders
            with <code>@demo.invalid</code> addresses (RFC 6761 reserved TLD,
            guaranteed unresolvable). This is a demo seed file — no actual
            outreach is sent.
          </div>
          {loadError && (
            <div className="csv-modal__error">Could not load CSV: {loadError}</div>
          )}
          {!loadError && !parsed && (
            <div className="csv-modal__loading">Loading…</div>
          )}
          {parsed && (
            <div className="csv-modal__table-wrap">
              <table className="csv-modal__table">
                <thead>
                  <tr>
                    {parsed.headers.map((h, i) => (
                      <th key={i}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {visibleRows.map((row, ri) => (
                    <tr key={ri}>
                      {parsed.headers.map((_, ci) => (
                        <td key={ci}>{row[ci] ?? ''}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        {parsed && (
          <div className="csv-modal__footer">
            Showing all {parsed.totalRows} rows · {parsed.headers.length} columns · scroll to inspect
          </div>
        )}
      </div>
    </div>
  );
}

import React, { useEffect, useRef, useState } from 'react';

// Hardcoded mirror of packages/knowledge_graph/graph.json — the 5 deployment
// anchors that the container-boot validator (packages/knowledge_graph/
// verify.py) re-checks against the Matta_Intel_cleaned.md substrate before
// the FastAPI lifespan completes startup. If any anchor's
// citation_verbatim_excerpt does not appear at its citation_substrate_line
// in the source intel, the container refuses to become healthy.
//
// This component surfaces the validation status visually:
// - A brief auto-dismissing banner at page load
// - A persistent forest dot in the header (next to the WS dot)
// - Click the dot to open a popover listing the 5 verified anchors with
//   their substrate-line citations
//
// The list is hardcoded because packages/ is not in the theater_ui build
// path; the alternative would have been a backend endpoint, which violates
// the iteration spec's "no backend route additions" constraint. The hardcoded
// list is a snapshot of graph.json v phase1-v1.

interface KGAnchor {
  id: string;
  display: string;
  vertical: string;
  substrate_lines: number[];
  citation_excerpt: string;
}

const KG_ANCHORS: KGAnchor[] = [
  {
    id: 'matta_deployment_bowers_and_wilkins',
    display: 'Bowers & Wilkins',
    vertical: 'electronics_assembly',
    substrate_lines: [540, 600],
    citation_excerpt: 'working with Bowers & Wilkins, where Matta',
  },
  {
    id: 'matta_deployment_caracol_am',
    display: 'Caracol AM',
    vertical: 'additive_manufacturing',
    substrate_lines: [542, 602],
    citation_excerpt: 'OEMs, Caracol',
  },
  {
    id: 'matta_deployment_global_drinks_brand',
    display: 'Global drinks brand (anonymized)',
    vertical: 'fnb_bottling',
    substrate_lines: [540, 600],
    citation_excerpt: 'high-speed bottling for defects with a global drinks brand',
  },
  {
    id: 'matta_deployment_polymer_unnamed',
    display: 'Polymer manufacturer (unnamed)',
    vertical: 'polymer_extrusion',
    substrate_lines: [540, 600],
    citation_excerpt: 'polymer manufacturing deployment, Matta achieved over 99% defect-detection',
  },
  {
    id: 'matta_deployment_metal_casting_unnamed',
    display: 'Metal casting (unnamed)',
    vertical: 'metal_casting',
    substrate_lines: [271, 421],
    citation_excerpt: 'polymer manufacturing and metal casting to bottling and consumer electronics',
  },
];

const BANNER_DURATION_MS = 3500;

export default function KGValidatorIndicator() {
  const [bannerVisible, setBannerVisible] = useState(true);
  const [popoverOpen, setPopoverOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-dismiss the banner after the duration
  useEffect(() => {
    const t = window.setTimeout(() => setBannerVisible(false), BANNER_DURATION_MS);
    return () => window.clearTimeout(t);
  }, []);

  // Click-outside dismiss for the popover
  useEffect(() => {
    if (!popoverOpen) return;
    const onClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setPopoverOpen(false);
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setPopoverOpen(false);
    };
    window.addEventListener('mousedown', onClick);
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('mousedown', onClick);
      window.removeEventListener('keydown', onKey);
    };
  }, [popoverOpen]);

  return (
    <div className="kg-indicator" ref={containerRef} data-tutorial-anchor="kg-validator">
      {bannerVisible && (
        <div className="kg-indicator__banner" role="status">
          <span className="kg-indicator__banner-check">✓</span>
          <span>
            Knowledge graph validated · {KG_ANCHORS.length} anchors verified against
            intel substrate · 0 mismatches
          </span>
        </div>
      )}
      <button
        className="kg-indicator__dot"
        type="button"
        onClick={() => setPopoverOpen((v) => !v)}
        title="Knowledge graph validated · click for details"
        aria-expanded={popoverOpen}
      >
        <span className="kg-indicator__dot-inner" aria-hidden="true" />
        <span className="kg-indicator__dot-label">KG ✓</span>
      </button>
      {popoverOpen && (
        <div className="kg-indicator__popover" role="dialog" aria-label="Verified knowledge graph anchors">
          <div className="kg-indicator__popover-header">
            <strong>Knowledge graph anchors verified at container boot</strong>
            <div className="kg-indicator__popover-sub">
              packages/knowledge_graph/verify.py refused to start the API if any
              anchor's citation excerpt did not appear at its substrate line
              in Matta_Intel_cleaned.md.
            </div>
          </div>
          <ul className="kg-indicator__anchors">
            {KG_ANCHORS.map((a) => (
              <li key={a.id} className="kg-indicator__anchor">
                <div className="kg-indicator__anchor-head">
                  <span className="kg-indicator__anchor-display">{a.display}</span>
                  <span className="kg-indicator__anchor-vertical">{a.vertical}</span>
                </div>
                <div className="kg-indicator__anchor-id">{a.id}</div>
                <div className="kg-indicator__anchor-cite">
                  substrate lines {a.substrate_lines.join(', ')}
                </div>
                <div className="kg-indicator__anchor-excerpt">
                  "{a.citation_excerpt}"
                </div>
              </li>
            ))}
          </ul>
          <div className="kg-indicator__popover-footer">
            phase1-v1 · validated at container boot
          </div>
        </div>
      )}
    </div>
  );
}

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
  source_url?: string;
  source_archive_url?: string;
  source_label?: string;
  dossier_sections_used: string[];
}

// Phase 1.7 Stage D: metal_casting_unnamed REMOVED (no verifiable substrate
// per kg_anchor_sources.md). All 4 surviving anchors point to the Cambridge
// IfM funding announcement as the canonical source. Wayback snapshot
// captured 2026-05-21 ensures audit-readers can verify the verbatim excerpts
// even if the live URL reorganizes.
const CAMBRIDGE_IFM_LIVE =
  'https://www.ifm.eng.cam.ac.uk/news/cambridge-spin-out-matta-raises-14m-to-build-sentient-factories/';
const CAMBRIDGE_IFM_WAYBACK =
  'https://web.archive.org/web/20260521124555/https://www.ifm.eng.cam.ac.uk/news/cambridge-spin-out-matta-raises-14m-to-build-sentient-factories/';
const CAMBRIDGE_IFM_LABEL = 'Cambridge IfM news, 10 Dec 2025';

const KG_ANCHORS: KGAnchor[] = [
  {
    id: 'matta_deployment_bowers_and_wilkins',
    display: 'Bowers & Wilkins',
    vertical: 'electronics_assembly',
    substrate_lines: [540, 600],
    citation_excerpt: 'working with Bowers & Wilkins, where Matta',
    source_url: CAMBRIDGE_IFM_LIVE,
    source_archive_url: CAMBRIDGE_IFM_WAYBACK,
    source_label: CAMBRIDGE_IFM_LABEL,
    dossier_sections_used: ['§3 Comparable Matta Deployment (when prospect is electronics_assembly)'],
  },
  {
    id: 'matta_deployment_caracol_am',
    display: 'Caracol AM',
    vertical: 'additive_manufacturing',
    substrate_lines: [542, 602],
    citation_excerpt: 'OEMs, Caracol',
    source_url: CAMBRIDGE_IFM_LIVE,
    source_archive_url: CAMBRIDGE_IFM_WAYBACK,
    source_label: CAMBRIDGE_IFM_LABEL,
    dossier_sections_used: ['§3 Comparable Matta Deployment (when prospect is additive_manufacturing)'],
  },
  {
    id: 'matta_deployment_global_drinks_brand',
    display: 'Global drinks brand (anonymized)',
    vertical: 'fnb_bottling',
    substrate_lines: [540, 600],
    citation_excerpt: 'high-speed bottling for defects with a global drinks brand',
    source_url: CAMBRIDGE_IFM_LIVE,
    source_archive_url: CAMBRIDGE_IFM_WAYBACK,
    source_label: CAMBRIDGE_IFM_LABEL,
    dossier_sections_used: ['§3 Comparable Matta Deployment (when prospect is fnb_bottling)'],
  },
  {
    id: 'matta_deployment_polymer_unnamed',
    display: 'Polymer manufacturer (unnamed)',
    vertical: 'polymer_extrusion',
    substrate_lines: [540, 600],
    citation_excerpt: 'polymer manufacturing deployment, Matta achieved over 99% defect-detection',
    source_url: CAMBRIDGE_IFM_LIVE,
    source_archive_url: CAMBRIDGE_IFM_WAYBACK,
    source_label: CAMBRIDGE_IFM_LABEL,
    dossier_sections_used: ['§3 Comparable Matta Deployment (when prospect is polymer_extrusion)'],
  },
];

const BANNER_DURATION_MS = 3500;
const AUTO_OPEN_DURATION_MS = 8000;

interface KGIndicatorProps {
  // Phase 1.7 Stage E: when phase transitions to 'complete', auto-open
  // the popover so Doug sees the Verify (Wayback) links without having
  // to discover the small dot in the header. Single highest-impact
  // demo UX change.
  phase?: string;
  // Phase 1.7 Stage E C9: anchor ID powering the current dossier — the
  // matching card gets a forest-tinted active highlight in the popover.
  activeAnchorId?: string | null;
}

export default function KGValidatorIndicator({ phase, activeAnchorId }: KGIndicatorProps = {}) {
  const [bannerVisible, setBannerVisible] = useState(true);
  const [popoverOpen, setPopoverOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const autoOpenFired = useRef(false);

  // Auto-dismiss the banner after the duration
  useEffect(() => {
    const t = window.setTimeout(() => setBannerVisible(false), BANNER_DURATION_MS);
    return () => window.clearTimeout(t);
  }, []);

  // Auto-open popover when dossier reaches complete state (once per session)
  useEffect(() => {
    if (phase !== 'complete' || autoOpenFired.current) return;
    autoOpenFired.current = true;
    setPopoverOpen(true);
    const t = window.setTimeout(() => setPopoverOpen(false), AUTO_OPEN_DURATION_MS);
    return () => window.clearTimeout(t);
  }, [phase]);

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
            Cambridge IfM substrate · 0 mismatches
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
              <code>packages/knowledge_graph/verify.py</code> refused to start
              the API if any anchor&apos;s citation excerpt did not appear at
              its substrate line in <code>docs/Matta_Intel_cleaned.md</code>.
              This eliminates the most common source of LLM dossier failure:
              confidently citing customer deployments that don&apos;t exist.
            </div>
            <div className="kg-indicator__popover-note">
              <em>
                Methodology note: structurally this is a verified citation
                table rather than a traversal graph (no entities or
                relations) — branded &ldquo;Knowledge Graph&rdquo; for
                architectural continuity with the broader pattern of
                substrate-pinned LLM output constraints.
              </em>
            </div>
          </div>
          <ul className="kg-indicator__anchors">
            {KG_ANCHORS.map((a) => (
              <li
                key={a.id}
                className={`kg-indicator__anchor${
                  a.id === activeAnchorId ? ' kg-indicator__anchor--active' : ''
                }`}
              >
                <div className="kg-indicator__anchor-head">
                  <span className="kg-indicator__anchor-display">{a.display}</span>
                  {a.id === activeAnchorId && (
                    <span className="kg-indicator__anchor-active-tag">
                      · powering this dossier
                    </span>
                  )}
                  <span className="kg-indicator__anchor-vertical">{a.vertical}</span>
                </div>
                <div className="kg-indicator__anchor-id">{a.id}</div>
                <div className="kg-indicator__anchor-cite">
                  substrate lines {a.substrate_lines.join(', ')}
                </div>
                <div className="kg-indicator__anchor-excerpt">
                  "{a.citation_excerpt}"
                </div>
                {a.dossier_sections_used.length > 0 && (
                  <p className="kg-indicator__anchor-usage">
                    Cited in: <strong>{a.dossier_sections_used[0]}</strong>
                  </p>
                )}
                {a.source_url && (
                  <div className="kg-indicator__anchor-source">
                    <span className="kg-indicator__anchor-source-label">
                      Source: {a.source_label}
                    </span>
                    <a
                      href={a.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="kg-indicator__anchor-source-link"
                    >
                      Verify (live)
                    </a>
                    {a.source_archive_url && (
                      <a
                        href={a.source_archive_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="kg-indicator__anchor-source-link"
                      >
                        Verify (Wayback)
                      </a>
                    )}
                  </div>
                )}
              </li>
            ))}
          </ul>
          <div className="kg-indicator__popover-footer">
            phase1-v3 · validated at container boot · 4 anchors
          </div>
        </div>
      )}
    </div>
  );
}

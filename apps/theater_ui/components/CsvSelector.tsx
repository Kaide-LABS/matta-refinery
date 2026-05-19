import React, { useEffect, useRef, useState } from 'react';
import type { CsvSelection } from '../hooks/useWebSocket';
import { SEED_CSVS, SeedCsv } from './seedCsvs';

interface Props {
  selectedCsv: CsvSelection;
  activeCsv: SeedCsv;
  disabled?: boolean;
  onSelect: (selection: CsvSelection) => void;
}

const RANDOM_ID: CsvSelection = 'random';

export default function CsvSelector({ selectedCsv, activeCsv, disabled, onSelect }: Props) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Click-outside / Escape dismissal
  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false);
    };
    window.addEventListener('mousedown', onClick);
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('mousedown', onClick);
      window.removeEventListener('keydown', onKey);
    };
  }, [open]);

  const isRandom = selectedCsv === RANDOM_ID;
  const triggerLabel = isRandom
    ? 'Random pick'
    : activeCsv.tradeShowDisplay;
  const triggerSubLabel = isRandom
    ? 'next Run Demo locks the choice'
    : `${activeCsv.approxLeadCount} leads`;

  const handleSelect = (sel: CsvSelection) => {
    onSelect(sel);
    setOpen(false);
  };

  return (
    <div
      className={`csv-selector ${disabled ? 'csv-selector--disabled' : ''} ${
        open ? 'csv-selector--open' : ''
      }`}
      data-tutorial-anchor="csv-selector"
      ref={containerRef}
    >
      <button
        type="button"
        className="csv-selector__trigger"
        onClick={() => !disabled && setOpen((v) => !v)}
        disabled={disabled}
        aria-expanded={open}
        aria-haspopup="listbox"
        aria-label="Trade-show CSV selector"
      >
        <div className="csv-selector__trigger-text">
          {isRandom && <span className="csv-selector__random-icon" aria-hidden="true">⚄</span>}
          <span className="csv-selector__trigger-name">{triggerLabel}</span>
          <span className="csv-selector__trigger-sep">·</span>
          <span className="csv-selector__trigger-sub">{triggerSubLabel}</span>
        </div>
        <span className="csv-selector__chevron" aria-hidden="true">▾</span>
      </button>

      {open && (
        <div className="csv-selector__popover" role="listbox">
          <button
            type="button"
            className={`csv-selector__option csv-selector__option--random ${
              isRandom ? 'csv-selector__option--active' : ''
            }`}
            role="option"
            aria-selected={isRandom}
            data-csv-id="random"
            onClick={() => handleSelect(RANDOM_ID)}
          >
            <span className="csv-selector__option-indicator" aria-hidden="true">
              {isRandom ? '●' : ' '}
            </span>
            <span className="csv-selector__random-icon" aria-hidden="true">⚄</span>
            <span className="csv-selector__option-label">Random pick</span>
            <span className="csv-selector__option-hint">surprise me</span>
          </button>
          <div className="csv-selector__divider" />
          {SEED_CSVS.map((csv) => {
            const isActive = !isRandom && selectedCsv === csv.id;
            return (
              <button
                key={csv.id}
                type="button"
                className={`csv-selector__option ${
                  isActive ? 'csv-selector__option--active' : ''
                }`}
                role="option"
                aria-selected={isActive}
                data-csv-id={csv.id}
                onClick={() => handleSelect(csv.id)}
              >
                <span className="csv-selector__option-indicator" aria-hidden="true">
                  {isActive ? '●' : ' '}
                </span>
                <span className="csv-selector__option-label">{csv.tradeShowDisplay}</span>
                <span className="csv-selector__option-count">{csv.approxLeadCount} leads</span>
              </button>
            );
          })}
        </div>
      )}

      <div className="csv-selector__caption">
        Pick a trade show — the engine ranks the cohort deterministically regardless of input.
      </div>
    </div>
  );
}

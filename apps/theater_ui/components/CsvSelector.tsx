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
  // Random pre-fire: trigger reads just "Random pick" (the dice icon does the
  // secondary work). Once Run Demo rolls, selectedCsv is set to the picked
  // CSV id and the trigger flips to the specific CSV display. Specific
  // selections always show name + lead count.
  const triggerLabel = isRandom ? 'Random pick' : activeCsv.tradeShowDisplay;
  // Lead-count subline only shows for specific selections — random pre-fire
  // leaves the secondary slot empty so the trigger reads cleanly.
  const triggerSubLabel = isRandom ? null : `${activeCsv.approxLeadCount} leads`;
  // The "↳ Run Demo will pick one randomly and lock the choice" hint
  // surfaces inline beneath the supporting line when the user has selected
  // Random pick and the demo hasn't fired yet. Suppressed in all other
  // states (specific selection, mid-run, complete).
  const showRandomLockHint = isRandom && !disabled;

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
      <label className="csv-selector__label" htmlFor="csv-selector-trigger">
        Choose a trade-show batch
      </label>
      <button
        id="csv-selector-trigger"
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
          {triggerSubLabel && (
            <>
              <span className="csv-selector__trigger-sep">·</span>
              <span className="csv-selector__trigger-sub">{triggerSubLabel}</span>
            </>
          )}
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
        The engine ranks each cohort deterministically — pick any batch to compare.
      </div>
      {showRandomLockHint && (
        <div className="csv-selector__hint">
          ↳ Run Demo will pick one randomly and lock the choice
        </div>
      )}
    </div>
  );
}

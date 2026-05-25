import { ReactNode, useCallback, useEffect, useRef, useState } from 'react';

const STORAGE_KEY = 'matta-refinery-layout-v1';
const RESET_EVENT = 'matta-reset-layout';

const DEFAULTS = { slack: 1.2, theater: 1.0, drive: 2.2 };
const MIN_PX = { slack: 240, theater: 200, drive: 380 };
const MAX_VIEWPORT_FRACTION = 0.7;

type Fractions = { slack: number; theater: number; drive: number };

function loadFractions(): Fractions {
  if (typeof window === 'undefined') return { ...DEFAULTS };
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULTS };
    const parsed = JSON.parse(raw);
    if (
      typeof parsed?.slack === 'number' &&
      typeof parsed?.theater === 'number' &&
      typeof parsed?.drive === 'number' &&
      parsed.slack > 0 &&
      parsed.theater > 0 &&
      parsed.drive > 0
    ) {
      return { slack: parsed.slack, theater: parsed.theater, drive: parsed.drive };
    }
  } catch {
    // fall through
  }
  return { ...DEFAULTS };
}

function saveFractions(f: Fractions) {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(f));
  } catch {
    // ignore quota errors
  }
}

interface Props {
  slack: ReactNode;
  theater: ReactNode;
  drive: ReactNode;
}

export default function ResizablePaneGrid({ slack, theater, drive }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [fr, setFr] = useState<Fractions>(() => ({ ...DEFAULTS }));
  const dragRef = useRef<{ handle: 'left' | 'right'; startX: number; start: Fractions; containerPx: number } | null>(null);

  useEffect(() => {
    setFr(loadFractions());
  }, []);

  useEffect(() => {
    const onReset = () => {
      setFr({ ...DEFAULTS });
      saveFractions({ ...DEFAULTS });
    };
    window.addEventListener(RESET_EVENT, onReset);
    return () => window.removeEventListener(RESET_EVENT, onReset);
  }, []);

  const onMouseMove = useCallback((e: MouseEvent) => {
    const drag = dragRef.current;
    if (!drag) return;
    const totalFr = drag.start.slack + drag.start.theater + drag.start.drive;
    const pxPerFr = drag.containerPx / totalFr;
    const deltaFr = (e.clientX - drag.startX) / pxPerFr;

    const maxPx = window.innerWidth * MAX_VIEWPORT_FRACTION;
    const maxFr = maxPx / pxPerFr;
    const minSlackFr = MIN_PX.slack / pxPerFr;
    const minTheaterFr = MIN_PX.theater / pxPerFr;
    const minDriveFr = MIN_PX.drive / pxPerFr;

    if (drag.handle === 'left') {
      let slackFr = drag.start.slack + deltaFr;
      let theaterFr = drag.start.theater - deltaFr;
      if (slackFr < minSlackFr) {
        theaterFr -= minSlackFr - slackFr;
        slackFr = minSlackFr;
      }
      if (theaterFr < minTheaterFr) {
        slackFr -= minTheaterFr - theaterFr;
        theaterFr = minTheaterFr;
      }
      if (slackFr > maxFr) {
        theaterFr -= slackFr - maxFr;
        slackFr = maxFr;
      }
      if (slackFr < minSlackFr || theaterFr < minTheaterFr) return;
      setFr({ slack: slackFr, theater: theaterFr, drive: drag.start.drive });
    } else {
      let theaterFr = drag.start.theater + deltaFr;
      let driveFr = drag.start.drive - deltaFr;
      if (theaterFr < minTheaterFr) {
        driveFr -= minTheaterFr - theaterFr;
        theaterFr = minTheaterFr;
      }
      if (driveFr < minDriveFr) {
        theaterFr -= minDriveFr - driveFr;
        driveFr = minDriveFr;
      }
      if (driveFr > maxFr) {
        theaterFr -= driveFr - maxFr;
        driveFr = maxFr;
      }
      if (theaterFr < minTheaterFr || driveFr < minDriveFr) return;
      setFr({ slack: drag.start.slack, theater: theaterFr, drive: driveFr });
    }
  }, []);

  const onMouseUp = useCallback(() => {
    if (!dragRef.current) return;
    dragRef.current = null;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    setFr((current) => {
      saveFractions(current);
      return current;
    });
  }, [onMouseMove]);

  const startDrag = (handle: 'left' | 'right') => (e: React.MouseEvent) => {
    e.preventDefault();
    const container = containerRef.current;
    if (!container) return;
    dragRef.current = {
      handle,
      startX: e.clientX,
      start: { ...fr },
      containerPx: container.getBoundingClientRect().width,
    };
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  };

  const gridStyle = {
    gridTemplateColumns: `${fr.slack}fr 6px ${fr.theater}fr 6px ${fr.drive}fr`,
  };

  return (
    <div ref={containerRef} className="resizable-pane-grid" style={gridStyle}>
      <div className="resizable-pane-grid__pane">{slack}</div>
      <div
        className="resizable-pane-grid__handle"
        role="separator"
        aria-orientation="vertical"
        aria-label="Resize Slack and Theater panes"
        onMouseDown={startDrag('left')}
      />
      <div className="resizable-pane-grid__pane">{theater}</div>
      <div
        className="resizable-pane-grid__handle"
        role="separator"
        aria-orientation="vertical"
        aria-label="Resize Theater and Drive panes"
        onMouseDown={startDrag('right')}
      />
      <div className="resizable-pane-grid__pane">{drive}</div>
    </div>
  );
}

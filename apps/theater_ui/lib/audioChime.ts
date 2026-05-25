// Web Audio chimes for Stage 1 + Stage 2 completion. No external assets —
// synthesized on demand so the demo has zero runtime audio dependencies.
//
// Stage 1: single C5 (523Hz) sine, 320ms, vol 0.18.
// Stage 2: C5+G5 two-note arpeggio, 440ms total, vol 0.22.
//
// Phase 1.7 Stage E: Chrome autoplay policy blocks audio until first user
// gesture. installAudioUnlock attaches a one-shot document.click listener
// that resumes any suspended AudioContext. Call this on app mount; the
// presenter's first click (Run Demo, Generate Briefing, etc.) unlocks
// chimes for the rest of the session.

let ctx: AudioContext | null = null;

function getCtx(): AudioContext | null {
  if (typeof window === 'undefined') return null;
  if (ctx) return ctx;
  const Ctor =
    (window.AudioContext as typeof AudioContext | undefined) ||
    ((window as unknown as { webkitAudioContext?: typeof AudioContext })
      .webkitAudioContext as typeof AudioContext | undefined);
  if (!Ctor) return null;
  try {
    ctx = new Ctor();
  } catch {
    return null;
  }
  return ctx;
}

function tone(freq: number, startOffset: number, durationMs: number, vol: number) {
  const c = getCtx();
  if (!c) return;
  const osc = c.createOscillator();
  const gain = c.createGain();
  osc.type = 'sine';
  osc.frequency.value = freq;
  const start = c.currentTime + startOffset / 1000;
  const end = start + durationMs / 1000;
  gain.gain.setValueAtTime(0.0001, start);
  gain.gain.exponentialRampToValueAtTime(vol, start + 0.02);
  gain.gain.exponentialRampToValueAtTime(0.0001, end);
  osc.connect(gain).connect(c.destination);
  osc.start(start);
  osc.stop(end + 0.05);
}

export function chimeStage1Complete() {
  tone(523.25, 0, 320, 0.18);
}

export function chimeStage2Complete() {
  tone(523.25, 0, 220, 0.22);
  tone(783.99, 200, 240, 0.22);
}

// Phase 1.7 Stage E: Chrome autoplay policy. The AudioContext starts
// suspended until the first user gesture. Resume it on the first
// document click; chimes thereafter play normally.
let unlockInstalled = false;
export function installAudioUnlock(): void {
  if (typeof document === 'undefined' || unlockInstalled) return;
  unlockInstalled = true;
  const unlock = () => {
    const c = getCtx();
    if (c && c.state === 'suspended') {
      // resume() is a Promise; failures are silent.
      void c.resume().catch(() => {});
    }
  };
  document.addEventListener('click', unlock, { once: true, capture: true });
}

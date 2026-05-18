import { useState, useEffect, useRef, useCallback } from 'react';

export interface TheaterEvent {
  type: string;
  timestamp: string;
  payload: Record<string, unknown>;
}

export type DemoPhase =
  | 'idle'
  | 'ingesting'
  | 'stage1'
  | 'stage1_complete'
  | 'stage2_requesting'
  | 'stage2'
  | 'complete'
  | 'error';

export type Stage2Section =
  | 'process_taxonomy'
  | 'defect_hypothesis'
  | 'comparable_deployment'
  | 'risk_register'
  | 'suggested_approach';

export interface Stage2Progress {
  process_taxonomy: 'pending' | 'active' | 'complete';
  defect_hypothesis: 'pending' | 'active' | 'complete';
  comparable_deployment: 'pending' | 'active' | 'complete';
  risk_register: 'pending' | 'active' | 'complete';
  suggested_approach: 'pending' | 'active' | 'complete';
}

export interface DossierPayload {
  process_taxonomy?: unknown;
  defect_hypothesis?: unknown;
  comparable_deployment?: unknown;
  risk_register?: unknown;
  suggested_approach?: unknown;
  deterministic_section_ratio?: number;
  company_facts?: Record<string, unknown>;
  verified_kg_anchors?: unknown;
  fitness_score_rationale?: unknown;
  risk_checklist_baseline?: unknown;
  approach_template_baseline?: unknown;
  unverified_sections?: string[];
  [key: string]: unknown;
}

const API_BASE =
  typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://localhost:8080'
    : '';

// Empirical Stage 1 wallclock from §H smoke runs: 319-338s. Use 300s threshold
// to unlock the top-12 cards. Worker tasks don't publish to the theater Redis
// channel yet, so the WS is silent — this timer is the pragmatic transition
// signal until Phase 1.7 wires worker publishes.
const STAGE1_UNLOCK_MS = 300_000;
const DOSSIER_POLL_MS = 5_000;

export interface UseDemoStateResult {
  phase: DemoPhase;
  batchId: string | null;
  dossierId: string | null;
  elapsedSec: number;
  stage2Progress: Stage2Progress;
  dossier: DossierPayload | null;
  byteDensityRatio: number | null;
  events: TheaterEvent[];
  connected: boolean;
  error: string | null;
  runDemo: () => Promise<void>;
  clickProspect: (prospectId: string, companyName: string) => Promise<void>;
  reset: () => void;
}

const initialStage2: Stage2Progress = {
  process_taxonomy: 'pending',
  defect_hypothesis: 'pending',
  comparable_deployment: 'pending',
  risk_register: 'pending',
  suggested_approach: 'pending',
};

export function useDemoState(): UseDemoStateResult {
  const [phase, setPhase] = useState<DemoPhase>('idle');
  const [batchId, setBatchId] = useState<string | null>(null);
  const [dossierId, setDossierId] = useState<string | null>(null);
  const [elapsedSec, setElapsedSec] = useState(0);
  const [stage2Progress, setStage2Progress] = useState<Stage2Progress>(initialStage2);
  const [dossier, setDossier] = useState<DossierPayload | null>(null);
  const [byteDensityRatio, setByteDensityRatio] = useState<number | null>(null);
  const [events, setEvents] = useState<TheaterEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startedAtRef = useRef<number | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const dossierPollRef = useRef<number | null>(null);
  const stage1TimerRef = useRef<number | null>(null);
  const elapsedTimerRef = useRef<number | null>(null);

  // ─── WebSocket connect once batchId is known ──────────────────────────────
  useEffect(() => {
    if (!batchId) return;
    const wsUrl = API_BASE.replace(/^http/, 'ws') + `/ws/theater/${batchId}`;
    let socket: WebSocket;
    try {
      socket = new WebSocket(wsUrl);
    } catch {
      return;
    }
    wsRef.current = socket;
    socket.onopen = () => setConnected(true);
    socket.onclose = () => setConnected(false);
    socket.onmessage = (ev) => {
      try {
        const parsed: TheaterEvent = JSON.parse(ev.data);
        setEvents((prev) => [...prev, parsed]);
      } catch {
        // ignore malformed frames
      }
    };
    socket.onerror = () => {
      // Silent: backend isn't currently publishing; polling drives state
    };
    return () => {
      try {
        socket.close();
      } catch {
        /* noop */
      }
    };
  }, [batchId]);

  // ─── Elapsed counter while demo running ───────────────────────────────────
  useEffect(() => {
    if (phase === 'idle' || phase === 'complete' || phase === 'error') {
      if (elapsedTimerRef.current) {
        window.clearInterval(elapsedTimerRef.current);
        elapsedTimerRef.current = null;
      }
      return;
    }
    elapsedTimerRef.current = window.setInterval(() => {
      if (startedAtRef.current) {
        setElapsedSec(Math.floor((Date.now() - startedAtRef.current) / 1000));
      }
    }, 1000);
    return () => {
      if (elapsedTimerRef.current) {
        window.clearInterval(elapsedTimerRef.current);
        elapsedTimerRef.current = null;
      }
    };
  }, [phase]);

  // ─── Stage 1 → Stage 1 complete transition (timer-based) ──────────────────
  useEffect(() => {
    if (phase !== 'stage1') return;
    stage1TimerRef.current = window.setTimeout(() => {
      setPhase('stage1_complete');
    }, STAGE1_UNLOCK_MS);
    return () => {
      if (stage1TimerRef.current) {
        window.clearTimeout(stage1TimerRef.current);
        stage1TimerRef.current = null;
      }
    };
  }, [phase]);

  // ─── Stage 2 dossier polling ──────────────────────────────────────────────
  useEffect(() => {
    if (phase !== 'stage2' || !dossierId) return;

    const poll = async () => {
      try {
        const res = await fetch(`${API_BASE}/dossier/${dossierId}`);
        if (res.status === 202) {
          // Still generating — keep polling
          return;
        }
        if (!res.ok) return;
        const body = (await res.json()) as DossierPayload;
        setDossier(body);
        if (typeof body.deterministic_section_ratio === 'number') {
          setByteDensityRatio(body.deterministic_section_ratio);
        }
        setStage2Progress((prev) => {
          const next = { ...prev };
          (
            [
              'process_taxonomy',
              'defect_hypothesis',
              'comparable_deployment',
              'risk_register',
              'suggested_approach',
            ] as Stage2Section[]
          ).forEach((s) => {
            if (body[s] && next[s] !== 'complete') {
              next[s] = 'complete';
            }
          });
          return next;
        });
        const allComplete =
          body.process_taxonomy &&
          body.defect_hypothesis &&
          body.comparable_deployment &&
          body.risk_register &&
          body.suggested_approach;
        if (allComplete) {
          setPhase('complete');
        }
      } catch {
        // network glitch — keep polling silently
      }
    };

    poll();
    dossierPollRef.current = window.setInterval(poll, DOSSIER_POLL_MS);
    return () => {
      if (dossierPollRef.current) {
        window.clearInterval(dossierPollRef.current);
        dossierPollRef.current = null;
      }
    };
  }, [phase, dossierId]);

  // ─── Heuristic Stage 2 section "active" rotation ──────────────────────────
  // Worker tasks don't publish per-section events; rotate the active highlight
  // through pending sections so viewers see motion. When a section actually
  // completes via poll, it locks to 'complete' and the rotation moves on.
  useEffect(() => {
    if (phase !== 'stage2') return;
    const ORDER: Stage2Section[] = [
      'process_taxonomy',
      'defect_hypothesis',
      'comparable_deployment',
      'risk_register',
      'suggested_approach',
    ];
    const tick = window.setInterval(() => {
      setStage2Progress((prev) => {
        const next = { ...prev };
        let foundActive = false;
        for (const s of ORDER) {
          if (next[s] === 'complete') continue;
          if (!foundActive) {
            next[s] = 'active';
            foundActive = true;
          } else {
            next[s] = 'pending';
          }
        }
        return next;
      });
    }, 8_000);
    return () => window.clearInterval(tick);
  }, [phase]);

  // ─── Actions ──────────────────────────────────────────────────────────────
  const runDemo = useCallback(async () => {
    setError(null);
    setPhase('ingesting');
    try {
      const csvRes = await fetch('/UK_Metals_Expo_2025_leads.csv');
      if (!csvRes.ok) throw new Error(`CSV fetch failed: HTTP ${csvRes.status}`);
      const csvBlob = await csvRes.blob();

      const form = new FormData();
      form.append('file', csvBlob, 'UK_Metals_Expo_2025_leads.csv');
      form.append('source_label', 'uk_metals_expo_2025');

      const res = await fetch(`${API_BASE}/ingest/batch`, {
        method: 'POST',
        body: form,
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Ingest failed: HTTP ${res.status} — ${txt.slice(0, 160)}`);
      }
      const body = (await res.json()) as { batch_id: string; status: string };
      setBatchId(body.batch_id);
      startedAtRef.current = Date.now();
      setElapsedSec(0);
      setPhase('stage1');
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Unknown error';
      setError(msg);
      setPhase('error');
    }
  }, []);

  const clickProspect = useCallback(
    async (prospectId: string, companyName: string) => {
      // Only William Cook actually triggers Stage 2 in this demo
      if (!companyName.toLowerCase().includes('william cook')) {
        return;
      }
      if (phase !== 'stage1_complete') return;
      setError(null);
      setPhase('stage2_requesting');

      const payload = {
        action_id: 'generate_full_dossier',
        prospect_id: prospectId,
        signal_hash: 'demo-ui-click',
        slack_response_url: 'https://hooks.slack.com/mock',
      };
      const form = new URLSearchParams();
      form.append('payload', JSON.stringify(payload));

      try {
        const res = await fetch(`${API_BASE}/slack/interactions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: form.toString(),
        });
        if (!res.ok) {
          const txt = await res.text();
          throw new Error(`Click failed: HTTP ${res.status} — ${txt.slice(0, 160)}`);
        }
        const body = (await res.json()) as { dossier_id: string; status: string };
        setDossierId(body.dossier_id);
        setPhase('stage2');
      } catch (e) {
        const msg = e instanceof Error ? e.message : 'Unknown error';
        setError(msg);
        setPhase('error');
      }
    },
    [phase]
  );

  const reset = useCallback(() => {
    setPhase('idle');
    setBatchId(null);
    setDossierId(null);
    setElapsedSec(0);
    setStage2Progress(initialStage2);
    setDossier(null);
    setByteDensityRatio(null);
    setEvents([]);
    setError(null);
    startedAtRef.current = null;
  }, []);

  return {
    phase,
    batchId,
    dossierId,
    elapsedSec,
    stage2Progress,
    dossier,
    byteDensityRatio,
    events,
    connected,
    error,
    runDemo,
    clickProspect,
    reset,
  };
}

// Legacy export retained for any consumer importing the original shape
export function useWebSocket(_url: string) {
  const [events] = useState<TheaterEvent[]>([]);
  const [connected] = useState(false);
  const [lastEvent] = useState<TheaterEvent | null>(null);
  return { events, connected, lastEvent };
}

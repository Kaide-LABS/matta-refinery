import { NextPage } from 'next';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import SlackLeftPane from '../components/SlackLeftPane';
import TheaterCenterPane from '../components/TheaterCenterPane';
import DriveDossierRightPane from '../components/DriveDossierRightPane';
import TutorialCallout from '../components/TutorialCallout';
import KGValidatorIndicator from '../components/KGValidatorIndicator';
import { useDemoState } from '../hooks/useWebSocket';
import { useTabTitle } from '../hooks/useTabTitle';

function MattaWordmark() {
  // PNG asset will replace the text fallback when dropped in
  // apps/theater_ui/public/branding/matta_logo_wordmark.png
  const [imgFailed, setImgFailed] = useState(false);
  if (imgFailed) {
    return <span className="app-header__wordmark-fallback">matta</span>;
  }
  return (
    /* eslint-disable-next-line @next/next/no-img-element */
    <img
      className="app-header__wordmark"
      src="/branding/matta_logo_wordmark.png"
      alt="Matta"
      onError={() => setImgFailed(true)}
    />
  );
}

const IndexPage: NextPage = () => {
  const demo = useDemoState();
  useTabTitle(demo.phase);

  // Phase 1.7 Stage D: /sandbox?mode=quickdemo skips Stage 1 UI and loads
  // the pre-baked batch directly. Polls /api/batch/prebaked once on mount;
  // shows "warming up" message if the startup pre-bake hasn't completed.
  const router = useRouter();
  const isQuickdemoMode = router.query.mode === 'quickdemo';
  const [quickdemoStatus, setQuickdemoStatus] = useState<
    'idle' | 'loading' | 'complete' | 'warming' | 'not_started' | 'error'
  >('idle');

  useEffect(() => {
    if (!isQuickdemoMode || demo.phase !== 'idle') return;
    let cancelled = false;
    (async () => {
      setQuickdemoStatus('loading');
      const result = await demo.loadPrebaked();
      if (!cancelled) setQuickdemoStatus(result);
    })();
    return () => {
      cancelled = true;
    };
  }, [isQuickdemoMode, demo.phase, demo.loadPrebaked]);

  if (isQuickdemoMode && (quickdemoStatus === 'warming' || quickdemoStatus === 'not_started')) {
    return (
      <div className="theater-shell">
        <div className="quickdemo-warming">
          <div className="quickdemo-warming__title">
            Demo is warming up — refresh in 30 seconds
          </div>
          <div className="quickdemo-warming__body">
            The Stage 1 ranking pipeline is pre-baking against the Industrial
            AI Summit cohort. This takes ~3 minutes on first container boot
            and is cached thereafter. Refresh the page once the worker has
            finished ranking all 65 prospects.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="theater-shell" data-quickdemo={isQuickdemoMode ? 'true' : 'false'}>

      <header className="app-header">
        <div className="app-header__brand">
          <MattaWordmark />
          <div className="app-header__divider" />
          <div className="app-header__title">Lead Refinery · Theater Console</div>
        </div>
        <div className="app-header__right">
          <KGValidatorIndicator phase={demo.phase} />
          {demo.batchId && (
            <div
              className="app-header__connection"
              title={demo.connected ? 'WebSocket live' : 'WebSocket awaiting events'}
            >
              <span
                className={
                  demo.connected
                    ? 'app-header__connection-dot'
                    : 'app-header__connection-dot app-header__connection-dot--off'
                }
                aria-label={demo.connected ? 'Live' : 'Awaiting events'}
              />
            </div>
          )}
        </div>
      </header>
      <div className="theater-grid">
        <SlackLeftPane
          phase={demo.phase}
          elapsedSec={demo.elapsedSec}
          activeCsv={demo.activeCsv}
          tracerProspect={demo.tracerProspect}
          tracerStatus={demo.tracerStatus}
          onClickProspect={demo.clickProspect}
          quickdemoMode={isQuickdemoMode}
        />
        <TheaterCenterPane
          phase={demo.phase}
          elapsedSec={demo.elapsedSec}
          batchId={demo.batchId}
          dossierId={demo.dossierId}
          stage2Progress={demo.stage2Progress}
          stage2Timings={demo.stage2Timings}
          byteDensityRatio={demo.byteDensityRatio}
          dossier={demo.dossier}
          error={demo.error}
          activeCsv={demo.activeCsv}
          selectedCsv={demo.selectedCsv}
          onSelectCsv={demo.selectCsv}
          onRunDemo={demo.runDemo}
          onReset={demo.reset}
          tracerProspect={demo.tracerProspect}
        />
        <DriveDossierRightPane
          phase={demo.phase}
          dossier={demo.dossier}
          activeCsv={demo.activeCsv}
          tracerProspect={demo.tracerProspect}
        />
      </div>
      <TutorialCallout
        phase={demo.phase}
        elapsedSec={demo.elapsedSec}
        stage2Progress={demo.stage2Progress}
        byteDensityRatio={demo.byteDensityRatio}
        tracerName={demo.tracerProspect?.company_name ?? demo.activeCsv.tracerCompany}
      />
    </div>
  );
};

export default IndexPage;

import { NextPage } from 'next';
import { useState } from 'react';
import SlackLeftPane from '../components/SlackLeftPane';
import TheaterCenterPane from '../components/TheaterCenterPane';
import DriveDossierRightPane from '../components/DriveDossierRightPane';
import CRMRecordInset from '../components/CRMRecordInset';
import TutorialCallout from '../components/TutorialCallout';
import { useDemoState } from '../hooks/useWebSocket';

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

  return (
    <div className="theater-shell">
      <header className="app-header">
        <div className="app-header__brand">
          <MattaWordmark />
          <div className="app-header__divider" />
          <div className="app-header__title">Lead Refinery · Theater Console</div>
        </div>
        <div className="app-header__right">
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
          onClickProspect={demo.clickProspect}
        />
        <TheaterCenterPane
          phase={demo.phase}
          elapsedSec={demo.elapsedSec}
          batchId={demo.batchId}
          dossierId={demo.dossierId}
          stage2Progress={demo.stage2Progress}
          stage2Timings={demo.stage2Timings}
          byteDensityRatio={demo.byteDensityRatio}
          error={demo.error}
          onRunDemo={demo.runDemo}
          onReset={demo.reset}
        />
        <DriveDossierRightPane phase={demo.phase} dossier={demo.dossier} />
        <CRMRecordInset phase={demo.phase} />
      </div>
      <TutorialCallout
        phase={demo.phase}
        elapsedSec={demo.elapsedSec}
        stage2Progress={demo.stage2Progress}
        byteDensityRatio={demo.byteDensityRatio}
      />
    </div>
  );
};

export default IndexPage;

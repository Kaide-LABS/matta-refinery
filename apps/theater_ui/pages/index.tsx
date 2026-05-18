import { NextPage } from 'next';
import SlackLeftPane from '../components/SlackLeftPane';
import TheaterCenterPane from '../components/TheaterCenterPane';
import DriveDossierRightPane from '../components/DriveDossierRightPane';
import CRMRecordInset from '../components/CRMRecordInset';
import { useDemoState } from '../hooks/useWebSocket';

const IndexPage: NextPage = () => {
  const demo = useDemoState();

  return (
    <div className="theater-grid">
      <SlackLeftPane
        phase={demo.phase}
        elapsedSec={demo.elapsedSec}
        onClickProspect={demo.clickProspect}
      />
      <TheaterCenterPane
        phase={demo.phase}
        elapsedSec={demo.elapsedSec}
        batchId={demo.batchId}
        dossierId={demo.dossierId}
        stage2Progress={demo.stage2Progress}
        byteDensityRatio={demo.byteDensityRatio}
        error={demo.error}
        onRunDemo={demo.runDemo}
        onReset={demo.reset}
      />
      <DriveDossierRightPane phase={demo.phase} dossier={demo.dossier} />
      <CRMRecordInset phase={demo.phase} />
    </div>
  );
};

export default IndexPage;

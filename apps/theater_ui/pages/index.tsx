import { NextPage } from 'next';
import { useRouter } from 'next/router';
import SlackLeftPane from '../components/SlackLeftPane';
import TheaterCenterPane from '../components/TheaterCenterPane';
import DriveDossierRightPane from '../components/DriveDossierRightPane';
import CRMRecordInset from '../components/CRMRecordInset';
import { useWebSocket } from '../hooks/useWebSocket';

const IndexPage: NextPage = () => {
  const router = useRouter();
  const batchId = (router.query.batchId as string) || 'demo_batch';
  const { events, connected } = useWebSocket(`/ws/theater/${batchId}`);

  return (
    <div className="grid grid-cols-3 h-screen relative">
      <SlackLeftPane events={events} />
      <TheaterCenterPane events={events} />
      <DriveDossierRightPane events={events} />
      <CRMRecordInset events={events} />
    </div>
  );
};

export default IndexPage;

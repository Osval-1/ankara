import { ContentLayout } from '@/components/layouts/content-layout';
import { EscalationsList } from '@/features/interactions/components/escalations-list';

export default function EscalationsPage() {
  return (
    <ContentLayout title="Escalations">
      <EscalationsList />
    </ContentLayout>
  );
}

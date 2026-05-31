import { ContentLayout } from '@/components/layouts/content-layout';
import { InteractionsList } from '@/features/interactions/components/interactions-list';

export default function InteractionsPage() {
  return (
    <ContentLayout title="Interactions">
      <InteractionsList />
    </ContentLayout>
  );
}

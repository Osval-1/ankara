import { ContentLayout } from '@/components/layouts/content-layout';
import { ExtensionWorkersList } from '@/features/extension-workers/components/extension-workers-list';

export default function ExtensionWorkersPage() {
  return (
    <ContentLayout title="Extension Workers">
      <ExtensionWorkersList />
    </ContentLayout>
  );
}

import { ContentLayout } from '@/components/layouts/content-layout';
import { ModelVersionsList } from '@/features/model-versions/components/model-versions-list';

export default function ModelVersionsPage() {
  return (
    <ContentLayout title="Model Versions">
      <ModelVersionsList />
    </ContentLayout>
  );
}

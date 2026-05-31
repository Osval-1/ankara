import { ContentLayout } from '@/components/layouts/content-layout';
import { Diagnose } from '@/features/diagnosis/components/diagnose';

export default function DiagnosePage() {
  return (
    <ContentLayout title="Diagnose">
      <Diagnose />
    </ContentLayout>
  );
}

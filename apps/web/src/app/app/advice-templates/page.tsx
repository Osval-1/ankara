import { ContentLayout } from '@/components/layouts/content-layout';
import { AdviceTemplatesList } from '@/features/advice-templates/components/advice-templates-list';

export default function AdviceTemplatesPage() {
  return (
    <ContentLayout title="Advice Templates">
      <AdviceTemplatesList />
    </ContentLayout>
  );
}

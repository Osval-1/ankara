import { ScanScreen } from '@/features/diagnosis/scan-screen';
import { useSelectedLanguage } from '@/lib/i18n/utils';

export default function ScanPage() {
  const { language } = useSelectedLanguage();
  return <ScanScreen language={language === 'fr' ? 'fr' : 'en'} />;
}

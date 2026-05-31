import { useRouter } from 'expo-router';
import { ConsentScreen } from '@/features/consent/consent-screen';

export default function ConsentPage() {
  const router = useRouter();
  return <ConsentScreen onDone={() => router.replace('/(app)')} />;
}

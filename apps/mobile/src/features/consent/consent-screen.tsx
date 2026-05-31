import { View } from 'react-native';
import { Button, Text } from '@/components/ui';
import { translate } from '@/lib/i18n/utils';
import { storage } from '@/lib/storage';

export const CONSENT_KEY = 'consent_given';

type Props = { onDone: () => void };

export function ConsentScreen({ onDone }: Props) {
  const accept = () => {
    storage.set(CONSENT_KEY, 'true');
    onDone();
  };

  const decline = () => {
    storage.set(CONSENT_KEY, 'false');
    onDone();
  };

  return (
    <View className="flex-1 bg-white justify-center px-6 space-y-6">
      <Text className="text-2xl font-bold text-center">{translate('consent.title')}</Text>
      <Text className="text-base text-gray-600 text-center leading-6">
        {translate('consent.message')}
      </Text>
      <Button label={translate('consent.accept')} onPress={accept} />
      <Button label={translate('consent.decline')} onPress={decline} variant="outline" />
    </View>
  );
}

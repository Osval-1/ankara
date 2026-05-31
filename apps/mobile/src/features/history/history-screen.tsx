import { FlatList, Image, View } from 'react-native';
import { Text } from '@/components/ui';
import { translate } from '@/lib/i18n/utils';
import { useDiagnosisStore, DiagnosisRecord } from '@/features/diagnosis/use-diagnosis-store';
import { ResultCard } from '@/features/diagnosis/result-card';

function HistoryItem({ record }: { record: DiagnosisRecord }) {
  return (
    <View className="mb-4">
      <Text className="text-xs text-gray-400 mb-1">
        {new Date(record.createdAt).toLocaleDateString()} — {record.crop}
      </Text>
      {record.imageUri ? (
        <Image source={{ uri: record.imageUri }} className="w-full h-40 rounded-lg mb-2" resizeMode="cover" />
      ) : null}
      <ResultCard reply={record.reply} />
    </View>
  );
}

export function HistoryScreen() {
  const records = useDiagnosisStore((s) => s.records);

  if (records.length === 0) {
    return (
      <View className="flex-1 items-center justify-center bg-white">
        <Text className="text-gray-500">{translate('history.empty')}</Text>
      </View>
    );
  }

  return (
    <FlatList
      data={records}
      keyExtractor={(r) => r.id}
      renderItem={({ item }) => <HistoryItem record={item} />}
      contentContainerClassName="p-4 bg-white"
    />
  );
}

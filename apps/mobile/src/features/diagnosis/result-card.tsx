import { View } from 'react-native';
import { Text } from '@/components/ui';
import { DiagnosisReply } from './api';
import { translate } from '@/lib/i18n/utils';

type Props = { reply: DiagnosisReply };

const CONFIDENCE_COLOUR: Record<string, string> = {
  low: 'text-red-600',
  medium: 'text-amber-600',
  high: 'text-green-600',
};

export function ResultCard({ reply }: Props) {
  return (
    <View className="rounded-xl border border-gray-200 p-4 space-y-3 bg-white shadow-sm">
      <View className="flex-row items-center justify-between">
        <Text className="text-lg font-bold">{reply.label}</Text>
        <Text className={`text-sm font-medium capitalize ${CONFIDENCE_COLOUR[reply.confidence]}`}>
          {reply.confidence}
        </Text>
      </View>

      <Text className="text-sm text-gray-700">{reply.opening}</Text>

      {reply.steps.map((step, i) => (
        <Text key={i} className="text-sm text-gray-600">
          {i + 1}. {step}
        </Text>
      ))}

      {reply.escalate && (
        <View className="bg-amber-50 border border-amber-200 rounded-lg p-3 mt-2">
          <Text className="text-sm text-amber-800 font-medium">
            ⚠️ {translate('diagnosis.escalate_warning')}
          </Text>
          <Text className="text-sm text-amber-700 mt-1">{reply.consultMessage}</Text>
        </View>
      )}
    </View>
  );
}

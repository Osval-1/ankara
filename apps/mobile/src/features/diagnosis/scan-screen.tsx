import * as ImagePicker from 'expo-image-picker';
import { useState } from 'react';
import { ActivityIndicator, Alert, Image, ScrollView, TouchableOpacity, View } from 'react-native';

import { Button, Text } from '@/components/ui';
import { translate } from '@/lib/i18n/utils';
import { useDiagnosisStore } from './use-diagnosis-store';
import { Crop, Language, diagnose } from './api';

const CROPS: { value: Crop; labelKey: string }[] = [
  { value: 'cassava', labelKey: 'crops.cassava' },
  { value: 'maize', labelKey: 'crops.maize' },
  { value: 'plantain', labelKey: 'crops.plantain' },
  { value: 'tomato', labelKey: 'crops.tomato' },
  { value: 'cocoa', labelKey: 'crops.cocoa' },
];

type Props = { language: Language };

export function ScanScreen({ language }: Props) {
  const [crop, setCrop] = useState<Crop>('cassava');
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const addRecord = useDiagnosisStore((s) => s.addRecord);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled) setImageUri(result.assets[0].uri);
  };

  const takePhoto = async () => {
    const result = await ImagePicker.launchCameraAsync({ quality: 0.8 });
    if (!result.canceled) setImageUri(result.assets[0].uri);
  };

  const runDiagnosis = async () => {
    if (!imageUri) return;
    setLoading(true);
    try {
      const reply = await diagnose({ crop, imageUri, language });
      addRecord({ crop, imageUri, reply, createdAt: Date.now(), synced: false });
    } catch {
      Alert.alert('Error', 'Diagnosis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView className="flex-1 bg-white p-4">
      <Text className="text-xl font-bold mb-4">{translate('diagnosis.select_crop')}</Text>

      <View className="flex-row flex-wrap gap-2 mb-6">
        {CROPS.map((c) => (
          <TouchableOpacity
            key={c.value}
            onPress={() => setCrop(c.value)}
            className={`px-3 py-2 rounded-full border ${crop === c.value ? 'bg-primary-500 border-primary-500' : 'border-gray-300'}`}
          >
            <Text className={crop === c.value ? 'text-white' : 'text-gray-700'}>
              {translate(c.labelKey as any)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <View className="flex-row gap-3 mb-6">
        <Button label={translate('diagnosis.take_photo')} onPress={takePhoto} className="flex-1" />
        <Button label={translate('diagnosis.choose_photo')} onPress={pickImage} className="flex-1" variant="outline" />
      </View>

      {imageUri && (
        <Image source={{ uri: imageUri }} className="w-full h-56 rounded-lg mb-4" resizeMode="cover" />
      )}

      {loading ? (
        <ActivityIndicator size="large" className="mt-4" />
      ) : (
        <Button
          label="Run Diagnosis"
          onPress={runDiagnosis}
          disabled={!imageUri}
        />
      )}
    </ScrollView>
  );
}

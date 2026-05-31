import { client } from '@/lib/api/client';

export type Crop = 'cassava' | 'maize' | 'plantain' | 'tomato' | 'cocoa';
export type Language = 'fr' | 'en';
export type ConfidenceLevel = 'low' | 'medium' | 'high';

export type DiagnosisReply = {
  crop: Crop;
  predictedClass: string;
  confidence: ConfidenceLevel;
  label: string;
  opening: string;
  steps: string[];
  consultMessage: string;
  escalate: boolean;
  adviceTemplateVersion: number | null;
};

export async function diagnose(params: {
  crop: Crop;
  imageUri: string;
  language: Language;
}): Promise<DiagnosisReply> {
  const form = new FormData();
  form.append('crop', params.crop);
  form.append('channel', 'mobile');
  form.append('language', params.language);
  form.append('image', {
    uri: params.imageUri,
    name: 'photo.jpg',
    type: 'image/jpeg',
  } as any);

  const { data } = await client.post<DiagnosisReply>('/diagnosis', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

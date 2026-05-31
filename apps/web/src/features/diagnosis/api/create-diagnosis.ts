import { api } from '@/lib/api-client';
import { DiagnosisReply } from '@/types/api';

export const createDiagnosis = (form: FormData): Promise<DiagnosisReply> => {
  return api.post('/diagnosis', form);
};

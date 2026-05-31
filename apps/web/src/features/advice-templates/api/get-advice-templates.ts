import { api } from '@/lib/api-client';
import { AdviceTemplate } from '@/types/api';

export const getAdviceTemplates = (): Promise<AdviceTemplate[]> => {
  return api.get('/advice-templates');
};

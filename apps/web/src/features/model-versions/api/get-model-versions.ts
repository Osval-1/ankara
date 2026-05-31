import { api } from '@/lib/api-client';
import { ModelVersion } from '@/types/api';

export const getModelVersions = (): Promise<ModelVersion[]> => {
  return api.get('/model-versions');
};

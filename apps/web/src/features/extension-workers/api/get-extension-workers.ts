import { api } from '@/lib/api-client';
import { ExtensionWorker } from '@/types/api';

export const getExtensionWorkers = (params?: { region?: string }): Promise<ExtensionWorker[]> => {
  return api.get('/extension-workers', { params });
};

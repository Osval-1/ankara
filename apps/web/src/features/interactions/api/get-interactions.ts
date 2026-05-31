import { api } from '@/lib/api-client';
import { Interaction } from '@/types/api';

export const getInteractions = (params?: { skip?: number; limit?: number }): Promise<Interaction[]> => {
  return api.get('/interactions', { params });
};

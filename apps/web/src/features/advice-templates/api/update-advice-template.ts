import { api } from '@/lib/api-client';
import { AdviceTemplate } from '@/types/api';

type UpdateAdviceTemplateInput = {
  id: string;
  label?: string;
  opening?: string;
  steps?: string[];
  consultMessage?: string;
  reviewedBy?: string;
  isActive?: boolean;
};

export const updateAdviceTemplate = ({ id, ...data }: UpdateAdviceTemplateInput): Promise<AdviceTemplate> => {
  return api.put(`/advice-templates/${id}`, data);
};

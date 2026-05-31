'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Spinner } from '@/components/ui/spinner';
import { Button } from '@/components/ui/button';
import { AdviceTemplate } from '@/types/api';
import { getAdviceTemplates } from '../api/get-advice-templates';
import { updateAdviceTemplate } from '../api/update-advice-template';

export const AdviceTemplatesList = () => {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery<AdviceTemplate[]>({
    queryKey: ['advice-templates'],
    queryFn: getAdviceTemplates,
  });

  const toggle = useMutation({
    mutationFn: ({ id, isActive }: { id: string; isActive: boolean }) =>
      updateAdviceTemplate({ id, isActive }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['advice-templates'] }),
  });

  if (isLoading) return <Spinner />;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Advice Templates</h1>
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-muted text-left">
              <th className="p-2 border">Crop</th>
              <th className="p-2 border">Class</th>
              <th className="p-2 border">Language</th>
              <th className="p-2 border">Label</th>
              <th className="p-2 border">Version</th>
              <th className="p-2 border">Reviewed by</th>
              <th className="p-2 border">Active</th>
              <th className="p-2 border"></th>
            </tr>
          </thead>
          <tbody>
            {data?.map((t) => (
              <tr key={t.id} className="hover:bg-muted/30">
                <td className="p-2 border capitalize">{t.crop}</td>
                <td className="p-2 border">{t.cropClass}</td>
                <td className="p-2 border uppercase">{t.language}</td>
                <td className="p-2 border">{t.label}</td>
                <td className="p-2 border">{t.version}</td>
                <td className="p-2 border">{t.reviewedBy ?? '—'}</td>
                <td className="p-2 border">{t.isActive ? 'Yes' : 'No'}</td>
                <td className="p-2 border">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => toggle.mutate({ id: t.id, isActive: !t.isActive })}
                  >
                    {t.isActive ? 'Deactivate' : 'Activate'}
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

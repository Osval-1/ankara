'use client';

import { useQuery } from '@tanstack/react-query';
import { Spinner } from '@/components/ui/spinner';
import { ModelVersion } from '@/types/api';
import { getModelVersions } from '../api/get-model-versions';

export const ModelVersionsList = () => {
  const { data, isLoading } = useQuery<ModelVersion[]>({
    queryKey: ['model-versions'],
    queryFn: getModelVersions,
  });

  if (isLoading) return <Spinner />;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Model Versions</h1>
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-muted text-left">
              <th className="p-2 border">Crop</th>
              <th className="p-2 border">Version</th>
              <th className="p-2 border">Dataset</th>
              <th className="p-2 border">Commit</th>
              <th className="p-2 border">Accuracy</th>
              <th className="p-2 border">ECE</th>
              <th className="p-2 border">Deployed</th>
              <th className="p-2 border">Active</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((m) => (
              <tr key={m.id} className="hover:bg-muted/30">
                <td className="p-2 border capitalize">{m.crop}</td>
                <td className="p-2 border">{m.version}</td>
                <td className="p-2 border">{m.datasetVersion}</td>
                <td className="p-2 border font-mono">{m.codeCommit.slice(0, 7)}</td>
                <td className="p-2 border">{m.accuracy != null ? `${(m.accuracy * 100).toFixed(1)}%` : '—'}</td>
                <td className="p-2 border">{m.ece != null ? m.ece.toFixed(3) : '—'}</td>
                <td className="p-2 border">{m.deployedAt ? new Date(m.deployedAt).toLocaleDateString() : '—'}</td>
                <td className="p-2 border">{m.isActive ? '✓' : '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

'use client';

import { useQuery } from '@tanstack/react-query';
import { Spinner } from '@/components/ui/spinner';
import { Interaction } from '@/types/api';
import { getInteractions } from '../api/get-interactions';

export const InteractionsList = () => {
  const { data, isLoading } = useQuery<Interaction[]>({
    queryKey: ['interactions'],
    queryFn: () => getInteractions({ limit: 100 }),
  });

  if (isLoading) return <Spinner />;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Interactions</h1>
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-muted text-left">
              <th className="p-2 border">Date</th>
              <th className="p-2 border">Channel</th>
              <th className="p-2 border">Crop</th>
              <th className="p-2 border">Predicted Class</th>
              <th className="p-2 border">Confidence</th>
              <th className="p-2 border">Escalated</th>
              <th className="p-2 border">Region</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((row) => (
              <tr key={row.id} className="hover:bg-muted/30">
                <td className="p-2 border">{new Date(row.createdAt).toLocaleDateString()}</td>
                <td className="p-2 border capitalize">{row.channel}</td>
                <td className="p-2 border capitalize">{row.crop}</td>
                <td className="p-2 border">{row.predictedClass}</td>
                <td className="p-2 border capitalize">{row.confidenceLevel}</td>
                <td className="p-2 border">{row.escalated ? '⚠️ Yes' : 'No'}</td>
                <td className="p-2 border">{row.region ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

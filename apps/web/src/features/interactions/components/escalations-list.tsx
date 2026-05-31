'use client';

import { useQuery } from '@tanstack/react-query';
import { Spinner } from '@/components/ui/spinner';
import { Interaction } from '@/types/api';
import { getInteractions } from '../api/get-interactions';

export const EscalationsList = () => {
  const { data, isLoading } = useQuery<Interaction[]>({
    queryKey: ['escalations'],
    queryFn: () => getInteractions({ limit: 200 }),
    select: (rows) => rows.filter((r) => r.escalated),
  });

  if (isLoading) return <Spinner />;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Escalations</h1>
      <p className="text-sm text-muted-foreground">Low-confidence diagnoses pending expert review.</p>
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-muted text-left">
              <th className="p-2 border">Date</th>
              <th className="p-2 border">Channel</th>
              <th className="p-2 border">Crop</th>
              <th className="p-2 border">Predicted Class</th>
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
                <td className="p-2 border">{row.region ?? '—'}</td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr><td colSpan={5} className="p-4 text-center text-muted-foreground">No escalations.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

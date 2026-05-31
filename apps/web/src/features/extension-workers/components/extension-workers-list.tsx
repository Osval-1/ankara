'use client';

import { useQuery } from '@tanstack/react-query';
import { Spinner } from '@/components/ui/spinner';
import { ExtensionWorker } from '@/types/api';
import { getExtensionWorkers } from '../api/get-extension-workers';

export const ExtensionWorkersList = () => {
  const { data, isLoading } = useQuery<ExtensionWorker[]>({
    queryKey: ['extension-workers'],
    queryFn: () => getExtensionWorkers(),
  });

  if (isLoading) return <Spinner />;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Extension Workers</h1>
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-muted text-left">
              <th className="p-2 border">Name</th>
              <th className="p-2 border">Region</th>
              <th className="p-2 border">Phone</th>
              <th className="p-2 border">WhatsApp</th>
              <th className="p-2 border">Crops</th>
              <th className="p-2 border">Active</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((w) => (
              <tr key={w.id} className="hover:bg-muted/30">
                <td className="p-2 border">{w.name}</td>
                <td className="p-2 border">{w.region}</td>
                <td className="p-2 border">{w.phone}</td>
                <td className="p-2 border">{w.whatsappAvailable ? '✓' : '—'}</td>
                <td className="p-2 border">{w.crops.join(', ')}</td>
                <td className="p-2 border">{w.active ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

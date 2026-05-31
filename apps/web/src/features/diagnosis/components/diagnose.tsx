'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { Crop, DiagnosisReply, Language } from '@/types/api';
import { createDiagnosis } from '../api/create-diagnosis';

const CROPS: { value: Crop; label: string }[] = [
  { value: 'cassava', label: 'Cassava (Manioc)' },
  { value: 'maize', label: 'Maize (Maïs)' },
  { value: 'plantain', label: 'Plantain' },
  { value: 'tomato', label: 'Tomato (Tomate)' },
  { value: 'cocoa', label: 'Cocoa (Cacao)' },
];

export const Diagnose = () => {
  const [crop, setCrop] = useState<Crop>('cassava');
  const [language, setLanguage] = useState<Language>('fr');
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<DiagnosisReply | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append('crop', crop);
      form.append('channel', 'web');
      form.append('language', language);
      form.append('image', file);
      const reply = await createDiagnosis(form);
      setResult(reply);
    } catch (err: any) {
      setError(err.message ?? 'Diagnosis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <h1 className="text-2xl font-semibold">Diagnose a Crop</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Crop</label>
          <select
            className="w-full rounded border p-2 text-sm"
            value={crop}
            onChange={(e) => setCrop(e.target.value as Crop)}
          >
            {CROPS.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Language</label>
          <select
            className="w-full rounded border p-2 text-sm"
            value={language}
            onChange={(e) => setLanguage(e.target.value as Language)}
          >
            <option value="fr">Français</option>
            <option value="en">English</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Plant photo</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="text-sm"
          />
        </div>
        <Button type="submit" disabled={!file || loading}>
          {loading ? <Spinner size="sm" /> : 'Run Diagnosis'}
        </Button>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {result && (
        <div className="rounded border p-4 space-y-2 bg-muted/30">
          <p className="font-semibold">{result.label} — <span className="capitalize">{result.confidence}</span> confidence</p>
          <p className="text-sm">{result.opening}</p>
          <ol className="list-decimal list-inside text-sm space-y-1">
            {result.steps.map((s, i) => <li key={i}>{s}</li>)}
          </ol>
          {result.escalate && (
            <p className="text-sm text-amber-700 font-medium">⚠️ {result.consultMessage}</p>
          )}
        </div>
      )}
    </div>
  );
};

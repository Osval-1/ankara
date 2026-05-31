import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { storage } from '@/lib/storage';
import { Crop, DiagnosisReply } from './api';

export type DiagnosisRecord = {
  id: string;
  crop: Crop;
  imageUri: string;
  reply: DiagnosisReply;
  createdAt: number;
  synced: boolean;
};

type DiagnosisState = {
  records: DiagnosisRecord[];
  addRecord: (record: Omit<DiagnosisRecord, 'id'>) => void;
  markSynced: (id: string) => void;
  clear: () => void;
};

const mmkvStorage = {
  getItem: (key: string) => storage.getString(key) ?? null,
  setItem: (key: string, value: string) => storage.set(key, value),
  removeItem: (key: string) => storage.delete(key),
};

export const useDiagnosisStore = create<DiagnosisState>()(
  persist(
    (set) => ({
      records: [],
      addRecord: (record) =>
        set((s) => ({
          records: [{ ...record, id: `${Date.now()}` }, ...s.records],
        })),
      markSynced: (id) =>
        set((s) => ({
          records: s.records.map((r) => (r.id === id ? { ...r, synced: true } : r)),
        })),
      clear: () => set({ records: [] }),
    }),
    {
      name: 'diagnosis-store',
      storage: createJSONStorage(() => mmkvStorage),
    },
  ),
);

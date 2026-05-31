import { User } from '@/types/api';

export const canViewInteractions = (user: User | null | undefined) =>
  user?.role === 'admin';

export const canViewEscalations = (user: User | null | undefined) =>
  user?.role === 'admin' || user?.role === 'agronomist';

export const canEditAdviceTemplates = (user: User | null | undefined) =>
  user?.role === 'admin' || user?.role === 'agronomist';

export const canManageExtensionWorkers = (user: User | null | undefined) =>
  user?.role === 'admin';

export const canViewModelVersions = (user: User | null | undefined) =>
  user?.role === 'admin';

export const canViewUsers = (user: User | null | undefined) =>
  user?.role === 'admin';

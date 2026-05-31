export type BaseEntity = {
  id: string;
  createdAt: number;
};

export type Entity<T> = {
  [K in keyof T]: T[K];
} & BaseEntity;

export type Meta = {
  page: number;
  total: number;
  totalPages: number;
};

export type UserRole = 'admin' | 'agronomist' | 'extension_worker' | 'labeler';

export type User = Entity<{
  name: string;
  username: string;
  email: string;
  role: UserRole;
  profileImageUrl: string;
}>;

export type AuthResponse = {
  jwt: string;
  user: User;
};

export type Crop = 'cassava' | 'maize' | 'plantain' | 'tomato' | 'cocoa';
export type Channel = 'whatsapp' | 'telegram' | 'mobile' | 'web';
export type Language = 'fr' | 'en';
export type ConfidenceLevel = 'low' | 'medium' | 'high';

export type Interaction = Entity<{
  channel: Channel;
  crop: Crop;
  predictedClass: string;
  confidenceLevel: ConfidenceLevel;
  adviceTemplateVersion: number | null;
  imageRef: string | null;
  farmerId: number | null;
  region: string | null;
  escalated: boolean;
  modelVersionId: number | null;
}>;

export type AdviceTemplate = Entity<{
  crop: Crop;
  cropClass: string;
  language: Language;
  version: number;
  label: string;
  opening: string;
  steps: string[];
  consultMessage: string;
  reviewedBy: string | null;
  reviewedAt: string | null;
  isActive: boolean;
}>;

export type ExtensionWorker = Entity<{
  name: string;
  region: string;
  phone: string;
  whatsappAvailable: boolean;
  crops: Crop[];
  active: boolean;
}>;

export type ModelVersion = Entity<{
  crop: Crop;
  version: string;
  datasetVersion: string;
  codeCommit: string;
  accuracy: number | null;
  ece: number | null;
  artifactPath: string;
  deployedAt: string | null;
  isActive: boolean;
}>;

export type DiagnosisRequest = {
  crop: Crop;
  imageRef: string;
  userId?: string;
  channel: Channel;
  language: Language;
};

export type DiagnosisReply = {
  crop: Crop;
  predictedClass: string;
  confidence: ConfidenceLevel;
  label: string;
  opening: string;
  steps: string[];
  consultMessage: string;
  escalate: boolean;
  adviceTemplateVersion: number | null;
};

// Auto-generated from FastAPI OpenAPI spec via openapi-typescript.
// Run: pnpm openapi-ts services/api/openapi.json -o packages/shared-types/index.ts

export type Crop = "cassava" | "maize" | "plantain" | "tomato" | "cocoa";

export type CropClass =
  | "healthy"
  | "cassava_mosaic"
  | "cassava_brown_streak"
  | "pest_damage"
  | "maize_streak"
  | "northern_leaf_blight"
  | "fall_armyworm"
  | "black_sigatoka"
  | "bunchy_top"
  | "banana_weevil"
  | "late_blight"
  | "early_blight"
  | "tuta_absoluta"
  | "black_pod"
  | "swollen_shoot"
  | "capsid_bug"
  | "unknown";

export type ConfidenceLevel = "low" | "medium" | "high";

export type Language = "fr" | "en";

export type Channel = "whatsapp" | "telegram" | "mobile" | "web";

export interface DiagnosisRequest {
  crop: Crop;
  image_ref: string;
  user_id: string;
  channel: Channel;
  language: Language;
}

export interface DiagnosisReply {
  crop: Crop;
  predicted_class: CropClass;
  confidence: ConfidenceLevel;
  label: string;
  opening: string;
  steps: string[];
  consult_message: string;
  escalate: boolean;
  advice_template_version: string;
}

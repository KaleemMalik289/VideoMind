export type VideoStatus = 'pending' | 'downloading' | 'extracting_audio' | 'transcribing' | 'analyzing' | 'completed' | 'failed';

export interface VideoDTO {
  id: string;
  title: string;
  url?: string;
  status: VideoStatus;
  duration?: number;
  thumbnailUrl?: string;
  createdAt: string;
  updatedAt: string;
}

export interface UploadVideoPayload {
  file?: File;
  youtubeUrl?: string;
}

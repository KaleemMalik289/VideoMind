// import { apiClient } from './client';
// import { ENDPOINTS } from './endpoints';
import type { VideoDTO, UploadVideoPayload, VideoStatus } from '@/types/video.types';

// Mocking API for now
const mockVideos: Record<string, VideoDTO> = {
  '123': {
    id: '123',
    title: 'Sample Video',
    status: 'analyzing',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  }
};

export const uploadVideo = async (_payload: UploadVideoPayload): Promise<VideoDTO> => {
  // return apiClient.post(ENDPOINTS.VIDEOS, _payload).then(res => res.data);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: '123',
        title: 'New Uploaded Video',
        status: 'pending',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
    }, 1000);
  });
};

export const submitYoutubeUrl = async (url: string): Promise<VideoDTO> => {
  // return apiClient.post(ENDPOINTS.VIDEOS, { youtubeUrl: url }).then(res => res.data);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: '123',
        title: 'YouTube Video',
        url,
        status: 'pending',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
    }, 1000);
  });
};

export const getVideo = async (id: string): Promise<VideoDTO> => {
  // return apiClient.get(ENDPOINTS.VIDEO_BY_ID(id)).then(res => res.data);
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (mockVideos[id]) resolve(mockVideos[id]);
      else reject(new Error('Not found'));
    }, 500);
  });
};

export const getVideoStatus = async (_id: string): Promise<{ status: VideoStatus; progress: number }> => {
  // return apiClient.get(ENDPOINTS.VIDEO_STATUS(_id)).then(res => res.data);
  return new Promise((resolve) => {
    setTimeout(() => {
      // simulate status progression
      const statuses: VideoStatus[] = ['pending', 'downloading', 'extracting_audio', 'transcribing', 'analyzing', 'completed'];
      const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
      resolve({ status: randomStatus, progress: Math.floor(Math.random() * 100) });
    }, 500);
  });
};

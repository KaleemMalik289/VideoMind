import { useMutation, useQueryClient } from '@tanstack/react-query';
import { uploadVideo, submitYoutubeUrl } from '@/api/videos.api';
import type { UploadVideoPayload, VideoDTO } from '@/types/video.types';

export const useUploadVideo = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UploadVideoPayload) => {
      if (payload.youtubeUrl) {
        return submitYoutubeUrl(payload.youtubeUrl);
      }
      return uploadVideo(payload);
    },
    onSuccess: (data: VideoDTO) => {
      // Invalidate queries or update cache
      queryClient.setQueryData(['video', data.id], data);
    },
  });
};

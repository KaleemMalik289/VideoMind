import { useQuery } from '@tanstack/react-query';
import { getVideo } from '@/api/videos.api';

export const useVideo = (videoId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['video', videoId],
    queryFn: () => getVideo(videoId),
    enabled,
  });
};

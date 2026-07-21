import { useQuery } from '@tanstack/react-query';
import { getVideoStatus } from '@/api/videos.api';

export const useVideoStatus = (videoId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['video-status', videoId],
    queryFn: () => getVideoStatus(videoId),
    refetchInterval: (query) => {
      // stop polling if status is completed or failed
      const status = query.state.data?.status;
      if (status === 'completed' || status === 'failed') {
        return false;
      }
      return 2000; // poll every 2 seconds
    },
    enabled,
  });
};

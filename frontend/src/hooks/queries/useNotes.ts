import { useQuery } from '@tanstack/react-query';
import { getNotes, getSummary } from '@/api/notes.api';

export const useNotes = (videoId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['notes', videoId],
    queryFn: () => getNotes(videoId),
    enabled,
  });
};

export const useSummary = (videoId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['summary', videoId],
    queryFn: () => getSummary(videoId),
    enabled,
  });
};

import React, { useRef, useEffect } from 'react';
import { usePlayerStore } from '@/store/playerStore';
import { useVideo } from '@/hooks/queries/useVideo';
import { Skeleton } from '@/components/ui/Skeleton';
import { PlayCircle } from 'lucide-react';

export const VideoPlayer: React.FC<{ videoId: string }> = ({ videoId }) => {
  const { data: video, isLoading } = useVideo(videoId);
  const videoRef = useRef<HTMLVideoElement>(null);
  
  const setCurrentTime = usePlayerStore(state => state.setCurrentTime);
  const setDuration = usePlayerStore(state => state.setDuration);
  const setIsPlaying = usePlayerStore(state => state.setIsPlaying);
  const seekRequest = usePlayerStore(state => state.seekRequest);
  const clearSeekRequest = usePlayerStore(state => state.clearSeekRequest);

  useEffect(() => {
    if (seekRequest !== null && videoRef.current) {
      videoRef.current.currentTime = seekRequest;
      clearSeekRequest();
    }
  }, [seekRequest, clearSeekRequest]);

  if (isLoading) return <Skeleton className="w-full h-full bg-muted/20" />;

  return (
    <div className="relative w-full h-full flex items-center justify-center bg-black group">
      {/* Mocking video player for now */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-white/50">
        <PlayCircle className="w-20 h-20 mb-4 opacity-50 group-hover:opacity-100 transition-opacity cursor-pointer" />
        <p className="font-medium">Video Player Placeholder</p>
        <p className="text-sm opacity-70 mt-1">{video?.title}</p>
      </div>
      
      {/* Invisible video element to satisfy types and events if we had a real src */}
      <video
        ref={videoRef}
        className="hidden"
        onTimeUpdate={(e) => setCurrentTime(e.currentTarget.currentTime)}
        onDurationChange={(e) => setDuration(e.currentTarget.duration)}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
      />
    </div>
  );
};

import React from 'react';
import { useNotes } from '@/hooks/queries/useNotes';
import { Skeleton } from '@/components/ui/Skeleton';
import { usePlayerStore } from '@/store/playerStore';
import { Clock } from 'lucide-react';

export const DetailedNotesTab: React.FC<{ videoId: string }> = ({ videoId }) => {
  const { data: notes, isLoading } = useNotes(videoId);
  const seekTo = usePlayerStore(state => state.seekTo);

  const handleTimestampClick = (seconds: number) => {
    seekTo(seconds);
  };

  if (isLoading) return (
    <div className="space-y-6">
      <Skeleton className="h-24 w-full" />
      <Skeleton className="h-24 w-full" />
    </div>
  );

  return (
    <div className="space-y-6 pb-20">
      {notes?.map((note) => (
        <div key={note.id} className="border-b border-border pb-6 last:border-0 group">
          <div 
            className="inline-flex items-center gap-1.5 text-xs font-mono font-medium text-primary bg-primary/10 px-2 py-1 rounded cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors mb-2"
            onClick={() => handleTimestampClick(note.timestamp)}
          >
            <Clock className="w-3 h-3" />
            {formatSeconds(note.timestamp)}
          </div>
          <p className="text-muted-foreground text-sm leading-relaxed">{note.content}</p>
        </div>
      ))}
    </div>
  );
};

// Helper for display
function formatSeconds(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

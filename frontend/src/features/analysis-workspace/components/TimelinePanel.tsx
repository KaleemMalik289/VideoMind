import React from 'react';
import { useVideo } from '@/hooks/queries/useVideo';
import { Skeleton } from '@/components/ui/Skeleton';
import { Clock } from 'lucide-react';

export const TimelinePanel: React.FC<{ videoId: string }> = ({ videoId }) => {
  const { isLoading } = useVideo(videoId);

  if (isLoading) return <Skeleton className="w-full h-full" />;

  return (
    <div className="flex flex-col h-full bg-card rounded-xl border shadow-lg overflow-hidden">
      <div className="p-4 border-b bg-muted/30">
        <h3 className="font-semibold text-foreground flex items-center gap-2">
          <Clock className="w-4 h-4 text-primary" />
          Timeline
        </h3>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Mock timeline events */}
        {[
          { time: '00:00', title: 'Introduction' },
          { time: '05:20', title: 'Core Concepts' },
          { time: '12:45', title: 'Deep Dive' },
          { time: '28:10', title: 'Summary & Q&A' }
        ].map((event, i) => (
          <div key={i} className="flex gap-3 items-start group cursor-pointer hover:bg-muted p-2 rounded-lg transition-colors">
            <span className="text-xs font-mono text-primary bg-primary/10 px-1.5 py-0.5 rounded mt-0.5">{event.time}</span>
            <span className="text-sm text-foreground font-medium group-hover:text-primary transition-colors">{event.title}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

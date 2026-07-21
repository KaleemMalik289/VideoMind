import React from 'react';
import { useSummary } from '@/hooks/queries/useNotes';
import { Skeleton } from '@/components/ui/Skeleton';

export const SummaryTab: React.FC<{ videoId: string }> = ({ videoId }) => {
  const { data, isLoading } = useSummary(videoId);

  if (isLoading) return (
    <div className="space-y-4">
      <Skeleton className="h-6 w-3/4" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
    </div>
  );

  return (
    <div className="prose prose-sm dark:prose-invert max-w-none text-foreground pb-20">
      <h3 className="text-xl font-semibold mb-4 text-primary">Executive Summary</h3>
      <p className="text-muted-foreground leading-relaxed">{data?.overview}</p>
      
      {data?.keyPoints && data.keyPoints.length > 0 && (
        <>
          <h4 className="font-medium mt-6 mb-2">Key Points</h4>
          <ul className="list-disc pl-5 space-y-1 text-muted-foreground">
            {data.keyPoints.map((kp, idx) => (
              <li key={idx}>{kp}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

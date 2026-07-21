import React, { useEffect, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useVideoStatus } from '@/hooks/queries/useVideoStatus';
import { Card, CardContent } from '@/components/ui/Card';
import { Progress } from '@/components/ui/Progress';
import { FadeIn } from '@/components/motion/FadeIn';
import { CheckCircle2, Loader2, Circle } from 'lucide-react';
import type { VideoStatus } from '@/types/video.types';

const STAGES: { id: VideoStatus; label: string }[] = [
  { id: 'pending', label: 'Queued for processing' },
  { id: 'downloading', label: 'Downloading video' },
  { id: 'extracting_audio', label: 'Extracting audio & frames' },
  { id: 'transcribing', label: 'Generating transcript & OCR' },
  { id: 'analyzing', label: 'Analyzing content with AI' },
  { id: 'completed', label: 'Finished' },
];

export const ProcessingStatusPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data, isLoading, error } = useVideoStatus(id || '');

  useEffect(() => {
    if (data?.status === 'completed') {
      setTimeout(() => navigate(`/videos/${id}/workspace`), 1500);
    }
  }, [data?.status, id, navigate]);

  const currentStageIndex = useMemo(() => {
    if (!data?.status) return 0;
    const idx = STAGES.findIndex(s => s.id === data.status);
    return idx >= 0 ? idx : 0;
  }, [data?.status]);

  if (isLoading) return <div className="p-8 text-center text-muted-foreground mt-20"><Loader2 className="w-8 h-8 animate-spin mx-auto mb-4" /> Loading status...</div>;
  if (error) return <div className="p-8 text-center text-destructive mt-20">Error loading status.</div>;

  return (
    <FadeIn className="max-w-2xl mx-auto mt-16 px-4">
      <Card className="shadow-lg border-primary/10 overflow-hidden">
        <div className="h-1.5 bg-gradient-to-r from-primary via-secondary to-primary bg-[length:200%_100%] animate-pulse" />
        <CardContent className="p-8 md:p-12">
          <div className="text-center mb-10">
            <h1 className="text-3xl font-extrabold tracking-tight mb-3">Processing Video</h1>
            <p className="text-muted-foreground">We are generating your AI summary, notes, and transcript. This may take a few moments.</p>
          </div>
          
          <div className="mb-8">
            <div className="flex justify-between text-sm font-medium mb-3">
              <span className="text-foreground capitalize">{data?.status?.replace('_', ' ')}</span>
              <span className="text-primary font-bold">{data?.progress || 0}%</span>
            </div>
            <Progress value={data?.progress || 0} className="h-3" />
          </div>

          <div className="space-y-6 mt-10">
            {STAGES.map((stage, idx) => {
              const isCompleted = idx < currentStageIndex || data?.status === 'completed';
              const isActive = idx === currentStageIndex && data?.status !== 'completed';
              
              return (
                <div key={stage.id} className={`flex items-center gap-4 transition-all duration-300 ${isActive ? 'scale-105' : ''}`}>
                  <div className="flex-shrink-0 relative">
                    {isCompleted ? (
                      <CheckCircle2 className="w-6 h-6 text-success" />
                    ) : isActive ? (
                      <Loader2 className="w-6 h-6 text-primary animate-spin" />
                    ) : (
                      <Circle className="w-6 h-6 text-muted" />
                    )}
                    {idx !== STAGES.length - 1 && (
                      <div className={`absolute top-6 bottom-[-24px] left-[11px] w-0.5 ${isCompleted ? 'bg-success' : 'bg-muted'}`} />
                    )}
                  </div>
                  <span className={`text-base font-medium transition-colors ${isCompleted ? 'text-foreground' : isActive ? 'text-primary font-semibold' : 'text-muted-foreground'}`}>
                    {stage.label}
                  </span>
                </div>
              );
            })}
          </div>
          
        </CardContent>
      </Card>
    </FadeIn>
  );
};

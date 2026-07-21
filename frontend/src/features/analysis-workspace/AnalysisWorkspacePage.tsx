import React from 'react';
import { useParams } from 'react-router-dom';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { VideoPlayer } from './components/VideoPlayer';
import { TimelinePanel } from './components/TimelinePanel';
import { SummaryTab } from './components/SummaryTab';
import { DetailedNotesTab } from './components/DetailedNotesTab';
import { FadeIn } from '@/components/motion/FadeIn';

export const AnalysisWorkspacePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <FadeIn className="h-[calc(100vh-4rem)] flex flex-col md:flex-row p-4 gap-4 bg-background">
      {/* Left Panel: Timeline */}
      <aside className="w-full md:w-64 flex-shrink-0 flex flex-col gap-4">
        <TimelinePanel videoId={id!} />
      </aside>

      {/* Middle Panel: Video Player */}
      <main className="flex-1 flex flex-col min-w-0">
        <div className="flex-1 bg-black rounded-xl overflow-hidden shadow-lg border border-border">
          <VideoPlayer videoId={id!} />
        </div>
      </main>

      {/* Right Panel: Content Tabs */}
      <aside className="w-full md:w-[400px] lg:w-[500px] flex-shrink-0 flex flex-col bg-card rounded-xl border shadow-lg overflow-hidden">
        <Tabs defaultValue="summary" className="flex flex-col h-full">
          <div className="p-2 border-b bg-muted/30 overflow-x-auto">
            <TabsList className="w-full justify-start h-auto p-1 bg-transparent">
              <TabsTrigger value="summary" className="data-[state=active]:bg-background">Summary</TabsTrigger>
              <TabsTrigger value="notes" className="data-[state=active]:bg-background">Notes</TabsTrigger>
              <TabsTrigger value="transcript" className="data-[state=active]:bg-background">Transcript</TabsTrigger>
            </TabsList>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4">
            <TabsContent value="summary" className="m-0 h-full outline-none">
              <SummaryTab videoId={id!} />
            </TabsContent>
            <TabsContent value="notes" className="m-0 h-full outline-none">
              <DetailedNotesTab videoId={id!} />
            </TabsContent>
            <TabsContent value="transcript" className="m-0 h-full outline-none">
              <div className="text-muted-foreground text-center mt-10">Transcript coming soon...</div>
            </TabsContent>
          </div>
        </Tabs>
      </aside>
    </FadeIn>
  );
};

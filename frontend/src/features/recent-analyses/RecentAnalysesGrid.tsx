import React from 'react';
import { PlayCircle, Clock, MoreVertical } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { FadeIn } from '@/components/motion/FadeIn';

const mockAnalyses = [
  { id: '1', title: 'React 18 Architecture Masterclass', duration: '45:20', timeAgo: '2 hours ago', status: 'completed' },
  { id: '2', title: 'YCombinator Startup School - Funding', duration: '32:15', timeAgo: 'Yesterday', status: 'completed' },
  { id: '3', title: 'Stanford CS229: Machine Learning', duration: '1:12:05', timeAgo: '3 days ago', status: 'completed' },
];

export const RecentAnalysesGrid: React.FC = () => {
  return (
    <section className="py-12">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Recent Analyses</h2>
          <p className="text-muted-foreground text-sm mt-1">Pick up where you left off</p>
        </div>
        <button className="text-primary text-sm font-medium hover:underline">View All</button>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockAnalyses.map((item, i) => (
          <FadeIn key={item.id} delay={i * 0.1}>
            <Card className="overflow-hidden hover:shadow-md transition-shadow group cursor-pointer border-border/50">
              <div className="h-32 bg-muted relative flex items-center justify-center">
                <PlayCircle className="w-10 h-10 text-muted-foreground/40 group-hover:text-primary transition-colors" />
                <div className="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded font-medium">
                  {item.duration}
                </div>
              </div>
              <CardContent className="p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-foreground line-clamp-1" title={item.title}>
                      {item.title}
                    </h3>
                    <div className="flex items-center text-xs text-muted-foreground mt-2 gap-1">
                      <Clock className="w-3 h-3" />
                      {item.timeAgo}
                    </div>
                  </div>
                  <button className="text-muted-foreground hover:text-foreground p-1 rounded hover:bg-accent">
                    <MoreVertical className="w-4 h-4" />
                  </button>
                </div>
              </CardContent>
            </Card>
          </FadeIn>
        ))}
      </div>
    </section>
  );
};

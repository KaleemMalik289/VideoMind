import React from 'react';
import { Sparkles, FileText, Search, Code, GraduationCap, FileOutput } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { FadeIn } from '@/components/motion/FadeIn';

const features = [
  { icon: Sparkles, title: 'AI Summary', desc: 'Get concise, highly accurate overviews of any lengthy video.' },
  { icon: FileText, title: 'Detailed Notes', desc: 'Timestamp-synced notes capturing all essential points.' },
  { icon: Search, title: 'OCR & Transcript', desc: 'Search through spoken words and on-screen text instantly.' },
  { icon: Code, title: 'Extracted Code', desc: 'Automatically grab code snippets shown in programming tutorials.' },
  { icon: GraduationCap, title: 'Quiz & Flashcards', desc: 'Test your knowledge with auto-generated learning materials.' },
  { icon: FileOutput, title: 'Export Anywhere', desc: 'Export to Markdown, PDF, or Notion with one click.' },
];

export const FeaturesSection: React.FC = () => {
  return (
    <section className="py-16">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold tracking-tight mb-4">Everything You Need to Learn Faster</h2>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Our multimodal AI doesn't just transcribe audio. It watches the video, reads the screen, and understands the context.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, i) => (
          <FadeIn key={i} delay={i * 0.1}>
            <Card className="h-full hover:shadow-md transition-shadow group border-primary/5">
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.desc}</p>
              </CardContent>
            </Card>
          </FadeIn>
        ))}
      </div>
    </section>
  );
};

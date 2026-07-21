import React from 'react';
import { motion } from 'framer-motion';
import { BrainCircuit, FileText, Code2, GraduationCap, Sparkles, MessageSquare } from 'lucide-react';

const features = [
  { icon: Sparkles, label: 'AI Summary', color: 'bg-purple-500/10 text-purple-500', delay: 0 },
  { icon: FileText, label: 'OCR Extraction', color: 'bg-blue-500/10 text-blue-500', delay: 0.1 },
  { icon: MessageSquare, label: 'Speech Transcription', color: 'bg-green-500/10 text-green-500', delay: 0.2 },
  { icon: Code2, label: 'Code Reconstruction', color: 'bg-orange-500/10 text-orange-500', delay: 0.3 },
  { icon: GraduationCap, label: 'Flashcards & Quizzes', color: 'bg-pink-500/10 text-pink-500', delay: 0.4 },
];

export const AuthIllustration: React.FC = () => {
  return (
    <div className="hidden lg:flex flex-col justify-between w-1/2 bg-muted/20 p-12 relative overflow-hidden border-r">
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary/20 blur-[100px] rounded-full -translate-y-1/2 translate-x-1/3" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-secondary/20 blur-[100px] rounded-full translate-y-1/3 -translate-x-1/3" />

      <div className="relative z-10">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex items-center gap-2 text-primary font-bold text-3xl mb-12"
        >
          <div className="bg-primary text-primary-foreground p-2 rounded-xl shadow-lg">
            <BrainCircuit size={28} />
          </div>
          <span className="tracking-tight">VideoMind AI</span>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight text-foreground leading-[1.1] mb-6">
            Transform Videos into Knowledge with AI
          </h1>
          <p className="text-lg text-muted-foreground leading-relaxed max-w-md">
            Upload videos, extract transcripts, generate intelligent summaries, OCR text, reconstruct code, and create study notes — all powered by AI.
          </p>
        </motion.div>
      </div>

      <div className="relative z-10 flex-1 flex flex-col justify-end pb-8">
        <div className="grid grid-cols-2 gap-4">
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.4 + feature.delay }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="flex items-center gap-3 bg-card border shadow-sm p-4 rounded-xl cursor-default transition-shadow hover:shadow-md"
            >
              <div className={`p-2 rounded-lg ${feature.color}`}>
                <feature.icon className="w-5 h-5" />
              </div>
              <span className="font-semibold text-sm">{feature.label}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

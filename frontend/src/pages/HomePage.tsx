import React from 'react';
import { HeroUploadSection } from '@/features/video-upload/HeroUploadSection';
import { RecentAnalysesGrid } from '@/features/recent-analyses/RecentAnalysesGrid';
import { FeaturesSection } from '@/features/features-showcase/FeaturesSection';

export const HomePage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto px-4 md:px-8 space-y-12 pb-20">
      <HeroUploadSection />
      <RecentAnalysesGrid />
      <FeaturesSection />
    </div>
  );
};

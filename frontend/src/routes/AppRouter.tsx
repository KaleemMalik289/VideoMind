import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppShell } from '@/components/layout/AppShell';
import { HomePage } from '@/pages/HomePage';
import { WorkspacePage } from '@/pages/WorkspacePage';
import { ProcessingStatusPage } from '@/features/processing-status/ProcessingStatusPage';
import { AuthPage } from '@/features/auth/AuthPage';
import { ProtectedRoute } from '@/routes/ProtectedRoute';
import { ProfileSettingsPage } from '@/features/profile/ProfileSettingsPage';

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/auth" element={<AuthPage />} />
        
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<AppShell />}>
            <Route index element={<HomePage />} />
          <Route path="videos/:id/status" element={<ProcessingStatusPage />} />
          <Route path="videos/:id/workspace" element={<WorkspacePage />} />
          <Route path="profile" element={<ProfileSettingsPage />} />
          
          {/* Fallback mock routes to prevent 404 for un-implemented pages */}
          <Route path="search" element={<div className="p-8 text-gray-500">Search coming soon</div>} />
          <Route path="*" element={<div className="p-8 text-red-500">404 - Not Found</div>} />
        </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

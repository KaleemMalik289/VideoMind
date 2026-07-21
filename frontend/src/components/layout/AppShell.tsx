import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { TopNav } from './TopNav';
import { ToastProvider } from '../feedback/ToastProvider';
import { useUiStore } from '@/store/uiStore';

export const AppShell: React.FC = () => {
  const isSidebarOpen = useUiStore((state) => state.isSidebarOpen);

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      <Sidebar />
      
      <main className={`flex-1 flex flex-col transition-all duration-300 ${isSidebarOpen ? 'md:ml-64' : 'md:ml-20'}`}>
        <TopNav />
        <div className="flex-1 overflow-y-auto">
          <Outlet />
        </div>
      </main>
      
      <ToastProvider />
    </div>
  );
};

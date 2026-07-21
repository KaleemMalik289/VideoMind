import React from 'react';
import { NavLink } from 'react-router-dom';
import { useUiStore } from '@/store/uiStore';
import { Upload, Home, Search, Settings, FileVideo, X } from 'lucide-react';
import { Button } from '../ui/Button';

export const Sidebar: React.FC = () => {
  const isSidebarOpen = useUiStore((state) => state.isSidebarOpen);
  const toggleSidebar = useUiStore((state) => state.toggleSidebar);

  return (
    <>
      {/* Mobile overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 md:hidden animate-in fade-in"
          onClick={toggleSidebar}
        />
      )}
      
      <aside className={`fixed inset-y-0 left-0 bg-background border-r z-40 flex flex-col transition-all duration-300 ${isSidebarOpen ? 'w-64 translate-x-0' : '-translate-x-full md:translate-x-0 md:w-20'}`}>
        <div className="h-16 flex items-center justify-between md:justify-start px-4 md:px-6 border-b">
          <div className="flex items-center gap-2 text-primary font-bold text-xl">
            <div className="bg-primary text-primary-foreground p-1.5 rounded-lg shadow-sm">
              <FileVideo size={20} />
            </div>
            {isSidebarOpen && <span className="tracking-tight">VideoMind</span>}
          </div>
          {isSidebarOpen && (
            <Button variant="ghost" size="icon" className="md:hidden" onClick={toggleSidebar}>
              <X className="h-5 w-5" />
            </Button>
          )}
        </div>
      
      <div className="p-4">
        <Button className={`w-full ${!isSidebarOpen && 'px-0'} rounded-full shadow-md bg-gradient-to-r from-primary to-secondary hover:shadow-lg transition-all duration-300`}>
          <Upload size={18} className={isSidebarOpen ? 'mr-2' : ''} />
          {isSidebarOpen && "New Analysis"}
        </Button>
      </div>

      <nav className="flex-1 overflow-y-auto py-2">
        <ul className="space-y-1 px-3">
          <li>
            <NavLink to="/" className={({isActive}) => `flex items-center ${isSidebarOpen ? 'gap-3 px-3' : 'justify-center'} py-2.5 rounded-lg transition-colors ${isActive ? 'bg-primary/10 text-primary font-medium' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}`}>
              <Home size={20} />
              {isSidebarOpen && <span>Dashboard</span>}
            </NavLink>
          </li>
          <li>
            <NavLink to="/search" className={({isActive}) => `flex items-center ${isSidebarOpen ? 'gap-3 px-3' : 'justify-center'} py-2.5 rounded-lg transition-colors ${isActive ? 'bg-primary/10 text-primary font-medium' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}`}>
              <Search size={20} />
              {isSidebarOpen && <span>Search</span>}
            </NavLink>
          </li>
        </ul>

        {isSidebarOpen && (
          <div className="mt-8 px-6 text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
            Recent Analyses
          </div>
        )}
        {/* Mock recent analyses list could go here */}
      </nav>
      
      <div className="p-4 border-t">
        <button className={`flex items-center ${isSidebarOpen ? 'gap-3 px-3' : 'justify-center'} py-2.5 text-muted-foreground hover:text-foreground hover:bg-muted w-full rounded-lg transition-colors`}>
          <Settings size={20} />
          {isSidebarOpen && <span className="font-medium text-sm">Settings</span>}
        </button>
      </div>
    </aside>
    </>
  );
};

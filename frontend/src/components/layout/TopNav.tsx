import React, { useState, useRef, useEffect } from 'react';
import { useTheme } from '@/hooks/ui/useTheme';
import { Moon, Sun, Bell, Menu, User as UserIcon, Settings, LogOut } from 'lucide-react';
import { Button } from '../ui/Button';
import { useUiStore } from '@/store/uiStore';
import { useAuthStore } from '@/store/authStore';
import { useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

export const TopNav: React.FC = () => {
  const { theme, setTheme } = useTheme();
  const toggleSidebar = useUiStore((state) => state.toggleSidebar);
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  // Extract first letter of name
  const userInitial = user?.name ? user.name.charAt(0).toUpperCase() : 'U';
  const displayFirstName = user?.name ? user.name.split(' ')[0] : 'User';

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b bg-background/80 backdrop-blur-md sticky top-0 z-30">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" className="md:hidden" onClick={toggleSidebar}>
          <Menu className="h-5 w-5" />
        </Button>
        <h2 className="text-lg font-medium text-foreground tracking-tight hidden sm:block">
          {getGreeting()}, <span className="font-semibold">{displayFirstName}</span> 👋
        </h2>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground">
          <Bell className="h-5 w-5" />
        </Button>
        <Button 
          variant="ghost" 
          size="icon" 
          className="text-muted-foreground hover:text-foreground"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        >
          {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </Button>
        
        <div className="relative ml-2" ref={dropdownRef}>
          <button 
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm shadow-sm ring-2 ring-background hover:ring-primary/50 transition-all cursor-pointer"
          >
            {userInitial}
          </button>

          <AnimatePresence>
            {isDropdownOpen && (
              <motion.div 
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                transition={{ duration: 0.2 }}
                className="absolute right-0 mt-2 w-56 bg-card border shadow-xl rounded-xl py-2 z-50 origin-top-right"
              >
                <div className="px-4 py-2 border-b mb-2">
                  <p className="font-medium text-sm truncate">{user?.name || 'User'}</p>
                  <p className="text-xs text-muted-foreground truncate">{user?.email || 'user@example.com'}</p>
                </div>
                
                <Link to="/profile" onClick={() => setIsDropdownOpen(false)}>
                  <div className="w-full text-left px-4 py-2 text-sm text-foreground hover:bg-muted transition-colors flex items-center cursor-pointer">
                    <UserIcon className="w-4 h-4 mr-2" />
                    Profile Settings
                  </div>
                </Link>

                <div className="w-full text-left px-4 py-2 text-sm text-foreground hover:bg-muted transition-colors flex items-center cursor-pointer cursor-not-allowed opacity-50">
                  <Settings className="w-4 h-4 mr-2" />
                  Preferences (Soon)
                </div>

                <div className="border-t my-2"></div>

                <button 
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-500 hover:bg-red-500/10 transition-colors flex items-center"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Sign out
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  );
};

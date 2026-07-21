import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AuthIllustration } from './components/AuthIllustration';
import { LoginForm } from './components/LoginForm';
import { RegisterForm } from './components/RegisterForm';
import { FileVideo } from 'lucide-react';

export const AuthPage: React.FC = () => {
  const [mode, setMode] = useState<'login' | 'register'>('login');

  const toggleMode = () => {
    setMode(prev => prev === 'login' ? 'register' : 'login');
  };

  return (
    <div className="min-h-screen flex bg-background w-full">
      {/* Left Branding Section (Desktop only) */}
      <AuthIllustration />

      {/* Right Auth Section */}
      <div className="w-full lg:w-1/2 flex flex-col items-center justify-center p-6 sm:p-12 relative overflow-hidden">
        {/* Mobile Logo */}
        <div className="flex items-center gap-2 text-primary font-bold text-2xl mb-8 lg:hidden">
          <div className="bg-primary text-primary-foreground p-1.5 rounded-lg shadow-sm">
            <FileVideo size={24} />
          </div>
          <span className="tracking-tight">VideoMind AI</span>
        </div>

        {/* Auth Card */}
        <motion.div 
          className="w-full max-w-md bg-card border shadow-xl rounded-2xl p-6 sm:p-8 relative z-10"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
        >
          {/* Tabs */}
          <div className="flex bg-muted p-1 rounded-xl mb-8">
            <button
              className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all ${mode === 'login' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
              onClick={() => setMode('login')}
            >
              Login
            </button>
            <button
              className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all ${mode === 'register' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
              onClick={() => setMode('register')}
            >
              Register
            </button>
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={mode}
              initial={{ opacity: 0, x: mode === 'login' ? -20 : 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: mode === 'login' ? 20 : -20 }}
              transition={{ duration: 0.3 }}
            >
              {mode === 'login' ? (
                <LoginForm onToggleMode={toggleMode} />
              ) : (
                <RegisterForm onToggleMode={toggleMode} />
              )}
            </motion.div>
          </AnimatePresence>
        </motion.div>
        
        {/* Background gradient blob for mobile */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-primary/10 blur-[100px] rounded-full z-0 lg:hidden pointer-events-none" />
      </div>
    </div>
  );
};

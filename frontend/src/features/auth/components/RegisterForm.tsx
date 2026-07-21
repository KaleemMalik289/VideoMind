import React, { useState } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/Button';
import { User, Mail, Lock, Loader2, ArrowRight } from 'lucide-react';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { PasswordStrengthIndicator } from './PasswordStrengthIndicator';
import { motion, AnimatePresence } from 'framer-motion';

const registerSchema = z.object({
  fullName: z.string().min(2, 'Full name is required'),
  email: z.string().min(1, 'Email is required').email('Invalid email address'),
  password: z.string()
    .min(8, 'Minimum 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain a number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),
  confirmPassword: z.string(),
  acceptTerms: z.boolean().refine(val => val === true, {
    message: 'You must accept the terms and conditions'
  })
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

type RegisterValues = z.infer<typeof registerSchema>;

interface RegisterFormProps {
  onToggleMode: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onToggleMode }) => {
  const [step, setStep] = useState<'form' | 'otp'>('form');
  const [isLoading, setIsLoading] = useState(false);
  const [otp, setOtp] = useState('');
  const [pendingData, setPendingData] = useState<RegisterValues | null>(null);
  const navigate = useNavigate();
  const login = useAuthStore(state => state.login);

  const {
    register,
    handleSubmit,
    control,
    formState: { errors, touchedFields },
  } = useForm<RegisterValues>({
    resolver: zodResolver(registerSchema),
    mode: 'onChange',
  });

  const passwordValue = useWatch({ control, name: 'password', defaultValue: '' });
  const confirmPasswordValue = useWatch({ control, name: 'confirmPassword', defaultValue: '' });

  const acceptTermsValue = useWatch({ control, name: 'acceptTerms', defaultValue: false });
  const isPasswordMatch = passwordValue && confirmPasswordValue && passwordValue === confirmPasswordValue;
  const showPasswordMismatch = touchedFields.confirmPassword && confirmPasswordValue && !isPasswordMatch;

  const onSubmit = async (data: RegisterValues) => {
    setIsLoading(true);
    // Simulate sending OTP instead of immediate creation
    setTimeout(() => {
      setIsLoading(false);
      if (data.email === 'exists@example.com') {
        toast.error('Email already exists');
      } else {
        setPendingData(data);
        setStep('otp');
        toast.success(`OTP sent to ${data.email}`);
      }
    }, 1500);
  };

  const verifyOtp = () => {
    if (otp !== '123456') {
      toast.error('Invalid OTP. Please use 123456 for testing.');
      return;
    }

    if (!pendingData) return;

    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      login({ id: '2', name: pendingData.fullName, email: pendingData.email }, 'mock-jwt-token');
      toast.success('Account Created Successfully');
      navigate('/');
    }, 1500);
  };

  const handleGoogleLogin = () => {
    toast.success('Google login simulation successful.');
  };

  return (
    <div className="w-full max-w-md mx-auto space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold tracking-tight">Create an account</h2>
        <p className="text-muted-foreground mt-2">Join VideoMind AI to start learning faster</p>
      </div>

      <AnimatePresence mode="wait">
        {step === 'form' && (
          <motion.div
            key="form"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
          >
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-sm font-medium">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                  <input
                    {...register('fullName')}
                    type="text"
                    placeholder="John Doe"
                    className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all ${errors.fullName ? 'border-red-500 focus:ring-red-500' : 'border-input'}`}
                    disabled={isLoading}
                  />
                </div>
                {errors.fullName && <p className="text-sm text-red-500 mt-1">{errors.fullName.message}</p>}
              </div>

              <div className="space-y-1.5">
                <label className="text-sm font-medium">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                  <input
                    {...register('email')}
                    type="email"
                    placeholder="user@example.com"
                    className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all ${errors.email ? 'border-red-500 focus:ring-red-500' : 'border-input'}`}
                    disabled={isLoading}
                  />
                </div>
                {errors.email && <p className="text-sm text-red-500 mt-1">{errors.email.message}</p>}
              </div>

              <div className="space-y-1.5">
                <label className="text-sm font-medium">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                  <input
                    {...register('password')}
                    type="password"
                    placeholder="••••••••"
                    className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all ${errors.password ? 'border-red-500 focus:ring-red-500' : 'border-input'}`}
                    disabled={isLoading}
                  />
                </div>
                <PasswordStrengthIndicator password={passwordValue} />
              </div>

              <div className="space-y-1.5">
                <label className="text-sm font-medium">Confirm Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                  <input
                    {...register('confirmPassword')}
                    type="password"
                    placeholder="••••••••"
                    className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all ${(errors.confirmPassword || showPasswordMismatch) ? 'border-red-500 focus:ring-red-500' : isPasswordMatch ? 'border-green-500 focus:ring-green-500' : 'border-input'}`}
                    disabled={isLoading}
                  />
                </div>
                {showPasswordMismatch && <p className="text-sm text-red-500 mt-1">Passwords do not match</p>}
                {isPasswordMatch && <p className="text-sm text-green-500 mt-1 flex items-center"><User className="w-4 h-4 mr-1"/> Passwords Match</p>}
              </div>

              <div className="flex items-start space-x-2 pt-2">
                <input 
                  type="checkbox" 
                  id="terms" 
                  {...register('acceptTerms')}
                  className="mt-1 h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary cursor-pointer"
                />
                <label htmlFor="terms" className="text-sm text-muted-foreground cursor-pointer">
                  I accept the <a href="#" className="text-primary hover:underline">Terms of Service</a> and <a href="#" className="text-primary hover:underline">Privacy Policy</a>
                </label>
              </div>
              {errors.acceptTerms && <p className="text-sm text-red-500 mt-1">{errors.acceptTerms.message}</p>}

              <Button type="submit" className="w-full h-12 text-base font-medium shadow-md shadow-primary/20 mt-4 transition-all" disabled={isLoading || !acceptTermsValue}>
                {isLoading ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : null}
                {isLoading ? 'Creating Account...' : 'Create Account'}
              </Button>
            </form>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-card text-muted-foreground">OR</span>
              </div>
            </div>

            <div className="space-y-3">
              <Button type="button" variant="outline" className="w-full h-11" onClick={handleGoogleLogin} disabled={isLoading}>
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                </svg>
                Continue with Google
              </Button>
            </div>
          </motion.div>
        )}

        {step === 'otp' && (
          <motion.div
            key="otp"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="space-y-6"
          >
            <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <h3 className="font-semibold text-primary mb-1">Verify your email</h3>
              <p className="text-sm text-muted-foreground">
                To complete your registration, please enter the 6-digit code sent to <span className="font-medium text-foreground">{pendingData?.email}</span>.
              </p>
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium">Verification Code</label>
              <input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="123456"
                maxLength={6}
                className="w-full px-4 py-2.5 rounded-lg border border-input bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 text-center tracking-[0.5em] font-mono text-lg"
                disabled={isLoading}
              />
              <p className="text-xs text-muted-foreground mt-2">For testing, use code: 123456</p>
            </div>

            <div className="flex items-center gap-3 pt-2">
              <Button onClick={verifyOtp} disabled={isLoading || otp.length < 6} className="flex-1 h-11">
                {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                Verify & Create Account
              </Button>
              <Button type="button" variant="outline" onClick={() => setStep('form')} disabled={isLoading} className="h-11 px-4">
                Back
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <p className="text-center text-sm text-muted-foreground mt-8">
        Already have an account?{' '}
        <button type="button" className="text-primary font-medium hover:underline flex items-center inline-flex" onClick={onToggleMode}>
          Login <ArrowRight className="w-4 h-4 ml-1" />
        </button>
      </p>
    </div>
  );
};

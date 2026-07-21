import React, { useState } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Lock, Loader2, CheckCircle2, Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { PasswordStrengthIndicator } from '@/features/auth/components/PasswordStrengthIndicator';
import { useAuthStore } from '@/store/authStore';

const securitySchema = z.object({
  currentPassword: z.string().min(1, 'Current password is required'),
  newPassword: z.string()
    .min(8, 'Minimum 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain a number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),
  confirmPassword: z.string(),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

type SecurityValues = z.infer<typeof securitySchema>;

export const ProfileSecurityTab: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [step, setStep] = useState<'form' | 'otp' | 'success'>('form');
  const [isLoading, setIsLoading] = useState(false);
  const [otp, setOtp] = useState('');

  const [deleteStep, setDeleteStep] = useState<'idle' | 'otp'>('idle');
  const [deleteOtp, setDeleteOtp] = useState('');

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors, touchedFields },
  } = useForm<SecurityValues>({
    resolver: zodResolver(securitySchema),
    mode: 'onChange',
  });

  const passwordValue = useWatch({ control, name: 'newPassword', defaultValue: '' });
  const confirmPasswordValue = useWatch({ control, name: 'confirmPassword', defaultValue: '' });

  const isPasswordMatch = passwordValue && confirmPasswordValue && passwordValue === confirmPasswordValue;
  const showPasswordMismatch = touchedFields.confirmPassword && confirmPasswordValue && !isPasswordMatch;

  const onPasswordSubmit = () => {
    setIsLoading(true);
    // Simulate sending OTP
    setTimeout(() => {
      setIsLoading(false);
      setStep('otp');
      toast.success(`OTP sent to ${user?.email}`);
    }, 1500);
  };

  const verifyOtp = () => {
    if (otp !== '123456') {
      toast.error('Invalid OTP. Please use 123456 for testing.');
      return;
    }

    setIsLoading(true);
    // Simulate API verification
    setTimeout(() => {
      setIsLoading(false);
      setStep('success');
      toast.success('Password updated successfully!');
      reset();
    }, 1500);
  };

  const onDeleteAccount = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setDeleteStep('otp');
      toast.success(`Account deletion OTP sent to ${user?.email}`);
    }, 1500);
  };

  const verifyDeleteOtp = () => {
    if (deleteOtp !== '123456') {
      toast.error('Invalid OTP. Please use 123456 for testing.');
      return;
    }

    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      toast.success('Account successfully deleted');
      logout();
      navigate('/auth');
    }, 1500);
  };

  return (
    <div className="space-y-8">
      <Card className="border-border/50 shadow-sm overflow-hidden">
        <CardHeader>
          <CardTitle>Security</CardTitle>
          <CardDescription>Update your password to secure your account.</CardDescription>
        </CardHeader>
        <CardContent>
          <AnimatePresence mode="wait">
            {step === 'form' && (
              <motion.div
                key="form"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <form onSubmit={handleSubmit(onPasswordSubmit)} className="space-y-6 max-w-md">
                  
                  <div className="space-y-1.5">
                    <label className="text-sm font-medium">Current Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                      <input
                        {...register('currentPassword')}
                        type="password"
                        placeholder="••••••••"
                        className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all ${errors.currentPassword ? 'border-red-500 focus:ring-red-500' : 'border-input'}`}
                        disabled={isLoading}
                      />
                    </div>
                    {errors.currentPassword && <p className="text-sm text-red-500 mt-1">{errors.currentPassword.message}</p>}
                  </div>

                  <div className="border-t border-border/50 my-6"></div>

                  <div className="space-y-1.5">
                    <label className="text-sm font-medium">New Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                      <input
                        {...register('newPassword')}
                        type="password"
                        placeholder="••••••••"
                        className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all ${errors.newPassword ? 'border-red-500 focus:ring-red-500' : 'border-input'}`}
                        disabled={isLoading}
                      />
                    </div>
                    <PasswordStrengthIndicator password={passwordValue} />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-sm font-medium">Confirm New Password</label>
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
                    {isPasswordMatch && <p className="text-sm text-green-500 mt-1 flex items-center"><CheckCircle2 className="w-4 h-4 mr-1"/> Passwords Match</p>}
                  </div>

                  <Button type="submit" disabled={isLoading} className="w-full sm:w-auto h-11 px-8">
                    {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                    {isLoading ? 'Sending OTP...' : 'Update Password'}
                  </Button>
                </form>
              </motion.div>
            )}

            {step === 'otp' && (
              <motion.div
                key="otp"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="max-w-md space-y-6"
              >
                <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
                  <h3 className="font-semibold text-primary mb-1">Verify Identity</h3>
                  <p className="text-sm text-muted-foreground">
                    To confirm this password change, please enter the 6-digit code sent to <span className="font-medium text-foreground">{user?.email}</span>.
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
                    Confirm Change
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setStep('form')} disabled={isLoading} className="h-11 px-4">
                    Cancel
                  </Button>
                </div>
              </motion.div>
            )}

            {step === 'success' && (
              <motion.div
                key="success"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex flex-col items-center justify-center py-8 text-center"
              >
                <div className="w-16 h-16 bg-green-500/10 text-green-500 rounded-full flex items-center justify-center mb-4">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">Password Updated</h3>
                <p className="text-muted-foreground max-w-sm mb-6">
                  Your password has been successfully changed.
                </p>
                <Button onClick={() => { setStep('form'); setOtp(''); }} variant="outline">
                  Back to Settings
                </Button>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>

      <Card className="border-red-500/20 shadow-sm overflow-hidden bg-red-500/5">
        <CardHeader>
          <CardTitle className="text-red-500 flex items-center">
            <Trash2 className="w-5 h-5 mr-2" />
            Danger Zone
          </CardTitle>
          <CardDescription>Permanently delete your account and all of your content.</CardDescription>
        </CardHeader>
        <CardContent>
          <AnimatePresence mode="wait">
            {deleteStep === 'idle' && (
              <motion.div
                key="idle"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="max-w-md"
              >
                <p className="text-sm text-muted-foreground mb-4">
                  Once you delete your account, there is no going back. Please be certain.
                </p>
                <Button 
                  variant="outline" 
                  className="border-red-500/50 text-red-500 hover:bg-red-500 hover:text-white"
                  onClick={onDeleteAccount}
                  disabled={isLoading}
                >
                  {isLoading && deleteStep === 'idle' ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
                  Delete Account
                </Button>
              </motion.div>
            )}

            {deleteStep === 'otp' && (
              <motion.div
                key="otp"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="max-w-md space-y-6"
              >
                <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
                  <h3 className="font-semibold text-red-500 mb-1">Verify Account Deletion</h3>
                  <p className="text-sm text-red-500/80">
                    To confirm the permanent deletion of your account, enter the 6-digit code sent to <span className="font-medium">{user?.email}</span>.
                  </p>
                </div>

                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-red-500">Verification Code</label>
                  <input
                    type="text"
                    value={deleteOtp}
                    onChange={(e) => setDeleteOtp(e.target.value)}
                    placeholder="123456"
                    maxLength={6}
                    className="w-full px-4 py-2.5 rounded-lg border border-red-500/30 bg-background focus:outline-none focus:ring-2 focus:ring-red-500/50 text-center tracking-[0.5em] font-mono text-lg"
                    disabled={isLoading}
                  />
                </div>

                <div className="flex items-center gap-3 pt-2">
                  <Button 
                    onClick={verifyDeleteOtp} 
                    disabled={isLoading || deleteOtp.length < 6} 
                    className="flex-1 h-11 bg-red-500 hover:bg-red-600 text-white"
                  >
                    {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                    Confirm Deletion
                  </Button>
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={() => { setDeleteStep('idle'); setDeleteOtp(''); }} 
                    disabled={isLoading} 
                    className="h-11 px-4"
                  >
                    Cancel
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>
    </div>
  );
};

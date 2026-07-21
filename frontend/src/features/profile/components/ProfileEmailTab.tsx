import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Mail, Loader2, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';
import { useAuthStore } from '@/store/authStore';
import { motion, AnimatePresence } from 'framer-motion';

const emailSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Invalid email address'),
});

type EmailValues = z.infer<typeof emailSchema>;

export const ProfileEmailTab: React.FC = () => {
  const { user, updateUser } = useAuthStore();
  const [step, setStep] = useState<'form' | 'otp' | 'success'>('form');
  const [isLoading, setIsLoading] = useState(false);
  const [pendingEmail, setPendingEmail] = useState('');
  const [otp, setOtp] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<EmailValues>({
    resolver: zodResolver(emailSchema),
  });

  const onEmailSubmit = (data: EmailValues) => {
    if (data.email === user?.email) {
      toast.error('This is already your current email address.');
      return;
    }
    
    setIsLoading(true);
    setPendingEmail(data.email);
    
    // Simulate sending OTP
    setTimeout(() => {
      setIsLoading(false);
      setStep('otp');
      toast.success(`OTP sent to ${data.email}`);
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
      updateUser({ email: pendingEmail });
      setStep('success');
      toast.success('Email updated successfully!');
    }, 1500);
  };

  return (
    <Card className="border-border/50 shadow-sm overflow-hidden">
      <CardHeader>
        <CardTitle>Email Address</CardTitle>
        <CardDescription>Update the email address associated with your account.</CardDescription>
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
              <div className="mb-6 p-4 bg-muted/50 rounded-lg border border-border/50 flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Current Email</p>
                  <p className="text-base font-semibold">{user?.email}</p>
                </div>
                <div className="px-2 py-1 bg-green-500/10 text-green-500 text-xs font-medium rounded-full flex items-center">
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  Verified
                </div>
              </div>

              <form onSubmit={handleSubmit(onEmailSubmit)} className="space-y-6 max-w-md">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium">New Email Address</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                    <input
                      {...register('email')}
                      type="email"
                      placeholder="new@example.com"
                      className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all ${errors.email ? 'border-red-500 focus:ring-red-500' : 'border-input'}`}
                      disabled={isLoading}
                    />
                  </div>
                  {errors.email && <p className="text-sm text-red-500 mt-1">{errors.email.message}</p>}
                </div>

                <Button type="submit" disabled={isLoading} className="w-full sm:w-auto h-11 px-8">
                  {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                  {isLoading ? 'Sending OTP...' : 'Send Verification Code'}
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
                <h3 className="font-semibold text-primary mb-1">Check your inbox</h3>
                <p className="text-sm text-muted-foreground">
                  We've sent a 6-digit verification code to <span className="font-medium text-foreground">{pendingEmail}</span>.
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
                  Verify & Update
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
              <h3 className="text-xl font-bold text-foreground mb-2">Email Updated</h3>
              <p className="text-muted-foreground max-w-sm mb-6">
                Your email address has been successfully updated to <span className="font-medium text-foreground">{user?.email}</span>.
              </p>
              <Button onClick={() => { setStep('form'); setOtp(''); }} variant="outline">
                Back to Settings
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </CardContent>
    </Card>
  );
};

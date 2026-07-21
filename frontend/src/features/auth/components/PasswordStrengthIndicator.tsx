import React from 'react';
import { motion } from 'framer-motion';
import { Check, X } from 'lucide-react';

interface PasswordStrengthProps {
  password?: string;
}

export const PasswordStrengthIndicator: React.FC<PasswordStrengthProps> = ({ password = '' }) => {
  const reqs = {
    length: password.length >= 8,
    upper: /[A-Z]/.test(password),
    lower: /[a-z]/.test(password),
    number: /[0-9]/.test(password),
    special: /[^A-Za-z0-9]/.test(password),
  };

  const score = Object.values(reqs).filter(Boolean).length;
  
  let strengthLabel = 'Weak';
  let strengthColor = 'bg-red-500';
  let width = 'w-[20%]';

  if (score === 0) {
    width = 'w-0';
    strengthLabel = '';
  } else if (score <= 2) {
    strengthLabel = 'Weak';
    strengthColor = 'bg-red-500';
    width = 'w-[20%]';
  } else if (score === 3) {
    strengthLabel = 'Fair';
    strengthColor = 'bg-orange-500';
    width = 'w-[40%]';
  } else if (score === 4) {
    strengthLabel = 'Good';
    strengthColor = 'bg-yellow-500';
    width = 'w-[60%]';
  } else if (score === 5 && password.length >= 12) {
    strengthLabel = 'Excellent';
    strengthColor = 'bg-green-500';
    width = 'w-[100%]';
  } else if (score === 5) {
    strengthLabel = 'Strong';
    strengthColor = 'bg-blue-500';
    width = 'w-[80%]';
  }

  const ReqItem = ({ met, text }: { met: boolean; text: string }) => (
    <div className="flex items-center gap-2 text-sm">
      {met ? <Check className="w-4 h-4 text-green-500" /> : <X className="w-4 h-4 text-muted-foreground" />}
      <span className={met ? 'text-green-500' : 'text-muted-foreground'}>{text}</span>
    </div>
  );

  return (
    <div className="space-y-3 mt-4 bg-muted/30 p-4 rounded-xl border border-border/50">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-medium text-foreground">Password Strength</span>
        {strengthLabel && <span className="text-xs font-semibold text-muted-foreground">{strengthLabel}</span>}
      </div>
      
      <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
        <motion.div 
          className={`h-full ${strengthColor} rounded-full`}
          initial={{ width: 0 }}
          animate={{ width: width === 'w-[20%]' ? '20%' : width === 'w-[40%]' ? '40%' : width === 'w-[60%]' ? '60%' : width === 'w-[80%]' ? '80%' : width === 'w-[100%]' ? '100%' : '0%' }}
          transition={{ duration: 0.3 }}
        />
      </div>

      <div className="space-y-1.5 pt-2">
        <ReqItem met={reqs.length} text="Minimum 8 characters" />
        <ReqItem met={reqs.upper} text="Contains uppercase letter" />
        <ReqItem met={reqs.lower} text="Contains lowercase letter" />
        <ReqItem met={reqs.number} text="Contains number" />
        <ReqItem met={reqs.special} text="Contains special character" />
      </div>
    </div>
  );
};

import React from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs';
import { ProfileGeneralTab } from './components/ProfileGeneralTab';
import { ProfileEmailTab } from './components/ProfileEmailTab';
import { ProfileSecurityTab } from './components/ProfileSecurityTab';
import { User, Mail, ShieldAlert } from 'lucide-react';
import { FadeIn } from '@/components/motion/FadeIn';

export const ProfileSettingsPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 lg:p-12 space-y-8">
      <FadeIn>
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Profile Settings</h1>
          <p className="text-muted-foreground mt-2">Manage your account settings and preferences.</p>
        </div>
      </FadeIn>

      <FadeIn delay={0.1}>
        <Tabs defaultValue="general" className="w-full">
          <TabsList className="grid w-full grid-cols-3 max-w-md h-12 bg-muted/50 p-1 mb-8">
            <TabsTrigger value="general" className="flex items-center gap-2 data-[state=active]:shadow-sm rounded-md">
              <User className="w-4 h-4" /> <span className="hidden sm:inline">General</span>
            </TabsTrigger>
            <TabsTrigger value="email" className="flex items-center gap-2 data-[state=active]:shadow-sm rounded-md">
              <Mail className="w-4 h-4" /> <span className="hidden sm:inline">Email</span>
            </TabsTrigger>
            <TabsTrigger value="security" className="flex items-center gap-2 data-[state=active]:shadow-sm rounded-md">
              <ShieldAlert className="w-4 h-4" /> <span className="hidden sm:inline">Security</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="general">
            <ProfileGeneralTab />
          </TabsContent>
          <TabsContent value="email">
            <ProfileEmailTab />
          </TabsContent>
          <TabsContent value="security">
            <ProfileSecurityTab />
          </TabsContent>
        </Tabs>
      </FadeIn>
    </div>
  );
};

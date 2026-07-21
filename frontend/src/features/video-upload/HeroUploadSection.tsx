import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUploadVideo } from '@/hooks/mutations/useUploadVideo';
import { Button } from '@/components/ui/Button';
import { FadeIn } from '@/components/motion/FadeIn';
import { Paperclip, Send, X } from 'lucide-react';

const TypewriterText: React.FC<{ text: string }> = ({ text }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText((prev) => prev + text.charAt(index));
        setIndex(index + 1);
      }, 150);
      return () => clearTimeout(timeout);
    } else {
      const timeout = setTimeout(() => {
        setDisplayedText('');
        setIndex(0);
      }, 4000);
      return () => clearTimeout(timeout);
    }
  }, [index, text]);

  return (
    <span>
      {displayedText}
      <span className="animate-pulse ml-1 text-primary">|</span>
    </span>
  );
};

export const HeroUploadSection: React.FC = () => {
  const navigate = useNavigate();
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const uploadVideoMutation = useUploadVideo();

  const handleFileUpload = (file: File) => {
    uploadVideoMutation.mutate({ file }, {
      onSuccess: (data) => {
        navigate(`/videos/${data.id}/status`);
      }
    });
  };

  const handleUrlSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!youtubeUrl) return;
    uploadVideoMutation.mutate({ youtubeUrl }, {
      onSuccess: (data) => {
        navigate(`/videos/${data.id}/status`);
      }
    });
  };

  return (
    <FadeIn className="max-w-4xl mx-auto space-y-10 py-10">
      <div className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent pb-2 min-h-[60px]">
          <TypewriterText text="Analyze YouTube Video" />
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Upload a local video file or paste a YouTube URL to automatically generate summaries, detailed notes, transcripts, and interactive quizzes.
        </p>
      </div>

      <div className="max-w-3xl mx-auto pt-8">
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            if (selectedFile) {
              handleFileUpload(selectedFile);
            } else if (youtubeUrl) {
              handleUrlSubmit(e);
            }
          }}
          className="relative flex items-center bg-card border border-input rounded-full shadow-lg p-2 transition-all focus-within:ring-2 focus-within:ring-primary focus-within:border-primary/50"
        >
          {/* File Upload Button */}
          <div className="flex-shrink-0">
            <input 
              type="file" 
              id="file-upload" 
              className="hidden" 
              accept="video/mp4,video/x-m4v,video/*"
              disabled={uploadVideoMutation.isPending}
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  setSelectedFile(e.target.files[0]);
                  setYoutubeUrl(''); // Clear URL if file is selected
                }
              }}
            />
            <label 
              htmlFor="file-upload"
              className={`flex items-center justify-center w-12 h-12 rounded-full cursor-pointer transition-colors ${selectedFile ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}`}
            >
              <Paperclip className="w-5 h-5" />
            </label>
          </div>

          {/* Input Area */}
          <div className="flex-1 px-4">
            {selectedFile ? (
              <div className="flex items-center justify-between bg-primary/10 rounded-full px-4 py-2">
                <span className="text-sm font-medium text-primary truncate max-w-[200px] md:max-w-sm">
                  {selectedFile.name}
                </span>
                <button 
                  type="button" 
                  onClick={() => setSelectedFile(null)}
                  className="text-primary hover:text-primary-foreground hover:bg-primary rounded-full p-1 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <input 
                type="url" 
                placeholder="Paste YouTube link here..." 
                className="w-full bg-transparent border-none focus:outline-none text-foreground placeholder:text-muted-foreground text-base"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                disabled={uploadVideoMutation.isPending}
              />
            )}
          </div>

          {/* Submit Button */}
          <div className="flex-shrink-0">
            <Button 
              type="submit" 
              size="icon" 
              className="w-12 h-12 rounded-full shadow-sm"
              disabled={(!youtubeUrl && !selectedFile) || uploadVideoMutation.isPending}
              isLoading={uploadVideoMutation.isPending}
            >
              {!uploadVideoMutation.isPending && <Send className="w-5 h-5 ml-0.5" />}
            </Button>
          </div>
        </form>
        <p className="text-center text-xs text-muted-foreground mt-4">
          MP4, AVI, MKV up to 2GB or any public YouTube URL
        </p>
      </div>
    </FadeIn>
  );
};

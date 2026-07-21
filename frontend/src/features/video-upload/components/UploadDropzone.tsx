import React, { useCallback, useState } from 'react';
import { UploadCloud } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface UploadDropzoneProps {
  onUpload: (file: File) => void;
  isUploading: boolean;
}

export const UploadDropzone: React.FC<UploadDropzoneProps> = ({ onUpload, isUploading }) => {
  const [isDragActive, setIsDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true);
    } else if (e.type === 'dragleave') {
      setIsDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  }, [onUpload]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <motion.div 
      whileHover={!isUploading ? { scale: 1.02 } : {}}
      whileTap={!isUploading ? { scale: 0.98 } : {}}
      className={`relative flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-2xl transition-all duration-300 overflow-hidden ${isDragActive ? 'border-primary bg-primary/10' : 'border-muted-foreground/30 bg-card hover:border-primary/50'}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input 
        type="file" 
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" 
        onChange={handleChange}
        accept="video/mp4,video/x-m4v,video/*"
        disabled={isUploading}
      />
      <div className="flex flex-col items-center justify-center p-6 text-center">
        <div className={`p-4 rounded-full mb-4 transition-colors ${isDragActive ? 'bg-primary/20 text-primary' : 'bg-muted text-muted-foreground'}`}>
          <UploadCloud className="w-8 h-8" />
        </div>
        <p className="mb-2 text-base font-semibold text-foreground">Click to upload or drag and drop</p>
        <p className="text-sm text-muted-foreground">MP4, AVI, MKV (Max. 2GB)</p>
        
        <AnimatePresence>
          {isUploading && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-20"
            >
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin mb-4" />
                <p className="text-primary font-medium">Uploading video...</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

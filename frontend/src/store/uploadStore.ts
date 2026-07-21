import { create } from 'zustand';

interface UploadState {
  isUploading: boolean;
  progress: number;
  setUploading: (status: boolean) => void;
  setProgress: (progress: number) => void;
  reset: () => void;
}

export const useUploadStore = create<UploadState>((set) => ({
  isUploading: false,
  progress: 0,
  setUploading: (status) => set({ isUploading: status }),
  setProgress: (progress) => set({ progress }),
  reset: () => set({ isUploading: false, progress: 0 }),
}));

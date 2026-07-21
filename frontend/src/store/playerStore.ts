import { create } from 'zustand';

interface PlayerState {
  currentTime: number;
  duration: number;
  isPlaying: boolean;
  setCurrentTime: (time: number) => void;
  setDuration: (duration: number) => void;
  setIsPlaying: (isPlaying: boolean) => void;
  seekTo: (time: number) => void;
  seekRequest: number | null; // Used to trigger a seek in the player component
  clearSeekRequest: () => void;
}

export const usePlayerStore = create<PlayerState>((set) => ({
  currentTime: 0,
  duration: 0,
  isPlaying: false,
  setCurrentTime: (time) => set({ currentTime: time }),
  setDuration: (duration) => set({ duration }),
  setIsPlaying: (isPlaying) => set({ isPlaying }),
  seekRequest: null,
  seekTo: (time) => set({ seekRequest: time }),
  clearSeekRequest: () => set({ seekRequest: null }),
}));

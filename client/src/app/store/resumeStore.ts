import { create } from 'zustand';

export interface ResumeResult {
  score: number;
  issues: string[];
  optimized: string;
  original: string;
}

interface ResumeState {
  file: File | null;
  jobDescription: string;
  isLoading: boolean;
  result: ResumeResult | null;
  error: string | null;
  
  // Actions
  setFile: (file: File | null) => void;
  setJobDescription: (description: string) => void;
  startOptimization: () => void;
  setResult: (result: ResumeResult) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const useResumeStore = create<ResumeState>((set) => ({
  file: null,
  jobDescription: '',
  isLoading: false,
  result: null,
  error: null,
  
  // Actions
  setFile: (file: File | null) => set({ file }),
  setJobDescription: (jobDescription: string) => set({ jobDescription }),
  startOptimization: () => set({ isLoading: true, error: null }),
  setResult: (result: ResumeResult) => set({ result, isLoading: false }),
  setError: (error: string | null) => set({ error, isLoading: false }),
  reset: () => set({
    file: null,
    jobDescription: '',
    isLoading: false,
    result: null,
    error: null
  })
})); 
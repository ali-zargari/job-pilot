import { create } from 'zustand';

export interface ResumeResult {
  score: number;
  issues: string[];
  optimized: string;
  original: string;
  draft?: string;
  lint_results?: any;
}

interface ResumeState {
  file: File | null;
  jobDescription: string;
  isLoading: boolean;
  result: ResumeResult | null;
  error: string | null;
  currentView: 'original' | 'draft' | 'optimized';
  
  // Actions
  setFile: (file: File | null) => void;
  setJobDescription: (description: string) => void;
  startOptimization: () => void;
  setResult: (result: ResumeResult) => void;
  setError: (error: string | null) => void;
  setCurrentView: (view: 'original' | 'draft' | 'optimized') => void;
  reset: () => void;
}

export const useResumeStore = create<ResumeState>((set) => ({
  file: null,
  jobDescription: '',
  isLoading: false,
  result: null,
  error: null,
  currentView: 'optimized',
  
  // Actions
  setFile: (file: File | null) => set({ file }),
  setJobDescription: (jobDescription: string) => set({ jobDescription }),
  startOptimization: () => set({ isLoading: true, error: null }),
  setResult: (result: ResumeResult) => set({ result, isLoading: false }),
  setError: (error: string | null) => set({ error, isLoading: false }),
  setCurrentView: (currentView) => set({ currentView }),
  reset: () => set({
    file: null,
    jobDescription: '',
    isLoading: false,
    result: null,
    error: null,
    currentView: 'optimized'
  })
})); 
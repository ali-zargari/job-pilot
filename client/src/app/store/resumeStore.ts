import { create } from 'zustand';

export interface ResumeResult {
  score: number;
  issues?: string[];
  lint_results?: {
    issues: Array<{
      message: string;
      severity: string;
      type: string;
      text?: string;
    }>;
  };
  optimized: string;
  original: string;
  rule_based: string;
  draft?: string; // Keep for backward compatibility
  improvements?: string[];
  optimized_with_ai?: boolean;
  original_format?: {
    filename: string;
    filetype: string;
    pdfMetadata: any;
  };
  suggestions?: {
    weak_verbs: string[];
    formatting_issues: string[];
    content_improvements: string[];
  };
}

interface ResumeState {
  file: File | null;
  jobDescription: string;
  isLoading: boolean;
  result: ResumeResult | null;
  error: string | null;
  currentView: 'original' | 'rule_based' | 'optimized';
  
  // Actions
  setFile: (file: File | null) => void;
  setJobDescription: (description: string) => void;
  startOptimization: () => void;
  setResult: (result: ResumeResult) => void;
  setError: (error: string | null) => void;
  setCurrentView: (view: 'original' | 'rule_based' | 'optimized') => void;
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
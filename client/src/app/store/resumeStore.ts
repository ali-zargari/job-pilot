import { create } from 'zustand';
import { ResumeData } from '@/types/resume';
import { parseResumeText, resumeDataToText } from '@/lib/resumeParser';
import { getDefaultDesignOptions } from '@/lib/resumeTemplates';

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
  
  // New template-based fields
  resumeData: ResumeData | null;
  originalResumeData: ResumeData | null;
  selectedTemplate: string;
  designOptions: any;
  activeSection: string;
  
  // Actions
  setFile: (file: File | null) => void;
  setJobDescription: (description: string) => void;
  startOptimization: () => void;
  setResult: (result: ResumeResult) => void;
  setError: (error: string | null) => void;
  setCurrentView: (view: 'original' | 'rule_based' | 'optimized') => void;
  
  // New template-based actions
  setResumeData: (data: ResumeData) => void;
  setOriginalResumeData: (data: ResumeData) => void;
  setSelectedTemplate: (templateId: string) => void;
  setDesignOptions: (options: any) => void;
  setActiveSection: (section: string) => void;
  updateResumeData: (data: Partial<ResumeData>) => void;
  
  reset: () => void;
}

// Default empty resume data structure
const getEmptyResumeData = (): ResumeData => ({
  contactInfo: {
    name: '',
    email: '',
    phone: '',
    location: '',
  },
  summary: '',
  experience: [],
  education: [],
  skills: {
    categories: []
  }
});

export const useResumeStore = create<ResumeState>((set) => ({
  file: null,
  jobDescription: '',
  isLoading: false,
  result: null,
  error: null,
  currentView: 'optimized',
  
  // Template-based state
  resumeData: null,
  originalResumeData: null,
  selectedTemplate: 'modern',
  designOptions: getDefaultDesignOptions('modern'),
  activeSection: 'contactInfo',
  
  // Actions
  setFile: (file: File | null) => set({ file }),
  
  setJobDescription: (jobDescription: string) => set({ jobDescription }),
  
  startOptimization: () => set({ isLoading: true, error: null }),
  
  setResult: (result: ResumeResult) => {
    // Also parse text content to structured data
    const resumeData = parseResumeText(result.optimized);
    const originalResumeData = parseResumeText(result.original);
    
    set({ 
      result, 
      isLoading: false,
      resumeData,
      originalResumeData
    });
  },
  
  setError: (error: string | null) => set({ error, isLoading: false }),
  
  setCurrentView: (currentView) => set({ currentView }),
  
  // Template-based actions
  setResumeData: (resumeData: ResumeData) => set({ resumeData }),
  
  setOriginalResumeData: (originalResumeData: ResumeData) => set({ originalResumeData }),
  
  setSelectedTemplate: (templateId: string) => {
    const designOptions = getDefaultDesignOptions(templateId);
    set({ 
      selectedTemplate: templateId,
      designOptions
    });
  },
  
  setDesignOptions: (options: any) => set({ designOptions: options }),
  
  setActiveSection: (activeSection: string) => set({ activeSection }),
  
  updateResumeData: (partialData: Partial<ResumeData>) => {
    set((state) => ({
      resumeData: state.resumeData 
        ? { ...state.resumeData, ...partialData } 
        : { ...getEmptyResumeData(), ...partialData }
    }));
  },
  
  reset: () => set({
    file: null,
    jobDescription: '',
    isLoading: false,
    result: null,
    error: null,
    currentView: 'optimized',
    resumeData: null,
    originalResumeData: null,
    selectedTemplate: 'modern',
    designOptions: getDefaultDesignOptions('modern'),
    activeSection: 'contactInfo'
  })
})); 
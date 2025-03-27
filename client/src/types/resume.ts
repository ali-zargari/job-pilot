// Types for the template-based resume system

// Basic contact information
export interface ContactInfo {
  name: string;
  email: string;
  phone: string;
  location: string;
  linkedin?: string;
  github?: string;
  portfolio?: string;
}

// Education entry
export interface Education {
  id?: string;
  institution: string;
  degree: string;
  field: string;
  startDate: string;
  endDate: string;
  location?: string;
  gpa?: string;
  highlights?: string[];
}

// Work experience entry
export interface Experience {
  id?: string;
  company: string;
  title: string;
  startDate: string;
  endDate: string;
  location?: string;
  description?: string;
  bullets: string[];
}

// Skills section with categories
export interface SkillCategory {
  name: string;
  skills: string[];
}

export interface Skills {
  categories: SkillCategory[];
}

// Project entry
export interface Project {
  id?: string;
  name: string;
  description?: string;
  startDate?: string;
  endDate?: string;
  url?: string;
  bullets: string[];
}

// Certification entry
export interface Certification {
  id?: string;
  name: string;
  issuer?: string;
  date?: string;
  url?: string;
  expires?: string;
}

// Additional section item
export interface AdditionalSectionItem {
  id?: string;
  title?: string;
  subtitle?: string;
  date?: string;
  bullets?: string[];
}

// Additional section
export interface AdditionalSection {
  title: string;
  items?: AdditionalSectionItem[];
  content?: string;
}

// Complete Resume Data Structure
export interface ResumeData {
  contactInfo: ContactInfo;
  summary: string;
  experience: Experience[];
  education: Education[];
  skills: Skills;
  projects: Project[];
  certifications: Certification[];
  additionalSections: AdditionalSection[];
}

// Template for formatting a resume
export interface ResumeTemplate {
  id: string;
  name: string;
  description: string;
  previewImage: string;
  sections: {
    contactInfo: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
    summary: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
    experience: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
    education: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
    skills: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
    projects: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
    certifications: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
    additionalSections: { visible: boolean; position: 'header' | 'sidebar' | 'main' };
  };
}

// Design options for resume customization
export interface FontSizes {
  name: number;
  sectionTitle: number;
  itemTitle: number;
  normal: number;
}

export interface Margins {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

export interface LineSpacing {
  lineHeight: number;
}

export interface SectionSpacing {
  sectionSpacing: number;
  itemSpacing: number;
}

export interface DesignOptions {
  fontSize: FontSizes;
  fontFamily: string;
  primaryColor: string;
  margins: Margins;
  lineSpacing: LineSpacing;
  sectionSpacing: SectionSpacing;
}

// Legacy design options interface (kept for compatibility)
export interface ResumeDesignOptions {
  template: string;
  fontSize: {
    name: number;
    sectionTitle: number;
    itemTitle: number;
    normal: number;
  };
  fontFamily: string;
  primaryColor: string;
  margins: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };
  lineSpacing: number;
  sectionSpacing: number;
}

// Result from resume analysis
export interface ResumeResult {
  score: number;
  issues: string[];
  optimized: string;
  original: string;
  improvementSuggestions?: {
    bullets?: string[];
    skills?: string[];
    keywords?: string[];
    formatting?: string[];
    content?: string[];
  };
} 
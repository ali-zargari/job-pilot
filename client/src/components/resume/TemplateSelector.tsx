import React from 'react';
import { RESUME_TEMPLATES } from '@/lib/resumeTemplates';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { ResumeDesignOptions } from '@/types/resume';
import Image from 'next/image';

interface TemplateSelectorProps {
  selectedTemplate: string;
  onSelectTemplate: (templateId: string) => void;
  designOptions: ResumeDesignOptions;
  onUpdateDesignOptions: (options: ResumeDesignOptions) => void;
}

const TemplateSelector: React.FC<TemplateSelectorProps> = ({
  selectedTemplate,
  onSelectTemplate,
  designOptions,
  onUpdateDesignOptions
}) => {
  const handleSelectTemplate = (templateId: string) => {
    onSelectTemplate(templateId);
  };

  // Helper to get section layout highlights
  const getTemplateHighlights = (template: typeof RESUME_TEMPLATES[0]) => {
    const highlights = [];
    
    // Ensure template has sections and contactInfo before trying to access
    if (template && template.sections) {
      // Generate highlights based on section layout
      if (template.sections.contactInfo && template.sections.contactInfo.position === 'sidebar') {
        highlights.push('Sidebar layout');
      } else {
        highlights.push('Header layout');
      }
      
      // Add highlights based on visible sections
      if (template.sections.skills && template.sections.skills.visible) {
        highlights.push('Skills section');
      }
      
      if (template.sections.projects && template.sections.projects.visible) {
        highlights.push('Projects showcase');
      }
      
      if (template.sections.certifications && template.sections.certifications.visible) {
        highlights.push('Certifications display');
      }
    }
    
    // Add some standard highlights based on template ID
    switch (template.id) {
      case 'modern':
        highlights.push('Clean, contemporary design');
        highlights.push('Professional spacing');
        break;
      case 'classic':
        highlights.push('Traditional chronological format');
        highlights.push('Professional typography');
        break;
      case 'creative':
        highlights.push('Bold design elements');
        highlights.push('Eye-catching format');
        break;
      case 'technical':
        highlights.push('Technical skills focus');
        highlights.push('Code-inspired layout');
        break;
      case 'minimal':
        highlights.push('Minimalist design');
        highlights.push('Content-focused layout');
        break;
      case 'professional':
        highlights.push('Business-friendly design');
        highlights.push('Formal layout');
        break;
      default:
        highlights.push('Professional design');
        highlights.push('ATS-friendly format');
    }
    
    return highlights;
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Resume Templates</h2>
      <p className="text-sm text-gray-500">
        Select a template to define the layout and style of your resume.
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {RESUME_TEMPLATES.map((template) => {
          const templateHighlights = getTemplateHighlights(template);
          
          return (
            <Card 
              key={template.id}
              className={`cursor-pointer transition-all hover:shadow-md overflow-hidden ${
                selectedTemplate === template.id 
                  ? 'ring-2 ring-primary-500' 
                  : 'hover:border-gray-300'
              }`}
              onClick={() => handleSelectTemplate(template.id)}
            >
              <div className="relative h-40 bg-gray-100">
                {/* Placeholder for template preview image */}
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-200 text-gray-500">
                  <div className="w-24 h-6 bg-white/60 rounded mb-2"></div>
                  <div className="w-full px-4 flex flex-col gap-1">
                    <div className="w-full h-2 bg-white/40 rounded"></div>
                    <div className="w-full h-2 bg-white/40 rounded"></div>
                    <div className="w-3/4 h-2 bg-white/40 rounded"></div>
                  </div>
                  <div className="absolute bottom-2 right-2 text-xs font-medium">
                    {template.name}
                  </div>
                </div>
                {/* Comment out Image component until we have real preview images
                <Image 
                  src={template.previewImage} 
                  alt={template.name} 
                  fill 
                  className="object-cover"
                />
                */}
              </div>
              
              <CardContent className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="font-medium">{template.name}</h3>
                    <p className="text-sm text-gray-500">{template.description}</p>
                  </div>
                  
                  {selectedTemplate === template.id && (
                    <div className="flex items-center justify-center w-6 h-6 bg-primary-500 rounded-full">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}
                </div>
                
                <div className="mt-2">
                  <h4 className="text-xs font-medium text-gray-500 mb-1">Features:</h4>
                  <ul className="text-xs space-y-1">
                    {templateHighlights.slice(0, 2).map((feature, index) => (
                      <li key={index} className="flex items-start">
                        <span className="inline-block w-3 h-3 mr-1 mt-0.5">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="text-primary-500">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </span>
                        {feature}
                      </li>
                    ))}
                    {templateHighlights.length > 2 && (
                      <li className="text-primary-500">+ {templateHighlights.length - 2} more</li>
                    )}
                  </ul>
                </div>
                
                <Button 
                  variant={selectedTemplate === template.id ? "default" : "outline"}
                  size="sm"
                  className="mt-3 w-full"
                  onClick={() => handleSelectTemplate(template.id)}
                >
                  {selectedTemplate === template.id ? "Selected" : "Select Template"}
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default TemplateSelector; 
'use client';

import React, { useState, useEffect } from 'react';
import { useResumeStore } from '@/app/store/resumeStore';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { useDropzone } from 'react-dropzone';
import { parseResumeText, resumeDataToText } from '@/lib/resumeParser';
import { getDefaultDesignOptions, RESUME_TEMPLATES } from '@/lib/resumeTemplates';
import { ArrowUpTrayIcon, DocumentTextIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import { Badge } from '@/components/ui/Badge';
import Link from 'next/link';
import { ResumeData } from '@/types/resume';

// Import our template-based components
import TemplateSelector from '@/components/resume/TemplateSelector';
import ResumeEditor from '@/components/resume/ResumeEditor';
import ResumePreview from '@/components/resume/ResumePreview';

export default function ResumeBuilderPage() {
  const [step, setStep] = useState(1);
  const [isExporting, setIsExporting] = useState(false);
  const [localResumeData, setLocalResumeData] = useState<ResumeData | null>(null);
  const [localTemplate, setLocalTemplate] = useState<string>('modern');
  const [localDesignOptions, setLocalDesignOptions] = useState(getDefaultDesignOptions('modern'));
  const [localActiveSection, setLocalActiveSection] = useState<string | null>(null);
  
  const {
    file,
    resumeData: storeResumeData,
    originalResumeData,
    selectedTemplate: storeSelectedTemplate,
    designOptions: storeDesignOptions,
    activeSection: storeActiveSection,
    setFile,
    updateResumeData,
    setSelectedTemplate,
    setDesignOptions,
    setActiveSection: storeSetActiveSection
  } = useResumeStore();

  // Use either store data or local data
  const resumeData = storeResumeData || localResumeData;
  const selectedTemplate = storeSelectedTemplate || localTemplate;
  const designOptions = storeDesignOptions || localDesignOptions;
  const activeSection = storeActiveSection || localActiveSection;
  
  // Combined function to update resume data in both store and local state
  const handleUpdateResumeData = (data: ResumeData) => {
    console.log('Attempting to update resume data');
    // Try to update in the store
    try {
      if (typeof updateResumeData === 'function') {
        console.log('Using store updateResumeData');
        updateResumeData(data);
      } else {
        console.log('Store updateResumeData not available');
      }
    } catch (error) {
      console.error('Error with store update:', error);
    }
    
    // Always update local state as fallback
    console.log('Updating local resume data state');
    setLocalResumeData(data);
  };

  // Combined function to handle template selection
  const handleSelectTemplate = (templateId: string) => {
    console.log('Attempting to update template to:', templateId);
    
    // Try to update in the store
    try {
      if (typeof setSelectedTemplate === 'function') {
        console.log('Using store setSelectedTemplate');
        setSelectedTemplate(templateId);
      } else {
        console.log('Store setSelectedTemplate not available');
      }
    } catch (error) {
      console.error('Error with store template update:', error);
    }
    
    // Always update local state as fallback
    console.log('Updating local template state');
    setLocalTemplate(templateId);
    
    // Update design options based on the template
    const newDesignOptions = getDefaultDesignOptions(templateId);
    handleUpdateDesignOptions(newDesignOptions);
  };
  
  // Combined function to handle design options updates
  const handleUpdateDesignOptions = (options: any) => {
    console.log('Attempting to update design options');
    
    // Try to update in the store
    try {
      if (typeof setDesignOptions === 'function') {
        console.log('Using store setDesignOptions');
        setDesignOptions(options);
      } else {
        console.log('Store setDesignOptions not available');
      }
    } catch (error) {
      console.error('Error with store design options update:', error);
    }
    
    // Always update local state as fallback
    console.log('Updating local design options state');
    setLocalDesignOptions(options);
  };

  // Combined function to set active section in both store and local state
  const handleSetActiveSection = (section: string | null) => {
    console.log('Attempting to set active section to:', section);
    
    // Try to update in the store
    try {
      if (typeof storeSetActiveSection === 'function') {
        console.log('Using store setActiveSection');
        storeSetActiveSection(section as string); // Cast to string for store compatibility
      } else {
        console.log('Store setActiveSection not available');
      }
    } catch (error) {
      console.error('Error with store active section update:', error);
    }
    
    // Always update local state as fallback
    console.log('Updating local active section state');
    setLocalActiveSection(section);
  };

  // Reset state when navigating away
  useEffect(() => {
    return () => {
      setFile(null);
    };
  }, [setFile]);

  // Use dropzone for file uploads
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    maxFiles: 1, // Only allow one file at a time
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    onDrop: async (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        console.log('File dropped:', acceptedFiles[0].name, 'Type:', acceptedFiles[0].type);
        setFile(acceptedFiles[0]);
        
        try {
          // Create form data for file upload
          const formData = new FormData();
          formData.append('resume', acceptedFiles[0]);
          console.log('Sending file to API...');
          
          // Extract text via API
          const response = await axios.post('/api/extract-resume-text', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          
          console.log('API response:', response.status, response.data);
          
          if (response.status === 200 && response.data.text) {
            // Parse the extracted text into structured data
            console.log('Parsing resume text...');
            const parsedData = parseResumeText(response.data.text);
            console.log('Parsed resume data:', parsedData);
            
            // Update resume data with our safe function
            handleUpdateResumeData(parsedData);
            
            // Use modern template by default if no template was previously selected
            if (!selectedTemplate) {
              handleSelectTemplate('modern');
            }
            
            // Display the extracted content immediately
            handleSetActiveSection(null);
            
            // Move to the edit content step directly
            console.log('Moving to step 3 (edit content)');
            setStep(3);
          } else {
            console.error('API response did not contain text:', response.data);
            toast.error('Failed to extract text from resume');
          }
        } catch (error) {
          console.error('Error extracting resume text:', error);
          toast.error('Error processing resume');
          
          // Fallback to direct file reading for TXT files
          if (acceptedFiles[0].type === 'text/plain') {
            console.log('Falling back to direct text reading');
            const reader = new FileReader();
            reader.onload = (e) => {
              const text = e.target?.result as string;
              console.log('File read directly, text length:', text.length);
              const parsedData = parseResumeText(text);
              handleUpdateResumeData(parsedData);
              handleSetActiveSection(null);
              setStep(3); // Go directly to edit
            };
            reader.readAsText(acceptedFiles[0]);
          }
        }
      }
    }
  });

  // Export resume to PDF
  const handleExportPDF = async () => {
    if (!resumeData) return;
    
    setIsExporting(true);
    
    try {
      const response = await fetch('/api/export-resume-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resumeText: resumeDataToText(resumeData),
          templateId: selectedTemplate,
          designOptions
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate PDF');
      }
      
      // Get the PDF blob from the response
      const blob = await response.blob();
      
      // Create a download link and click it
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'resume.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      
      // Clean up the URL object
      window.URL.revokeObjectURL(url);
      
      toast.success('Resume PDF exported successfully!');
    } catch (error) {
      console.error('Error exporting PDF:', error);
      toast.error('Failed to export PDF. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  // Render the current step
  const renderStepContent = () => {
    switch (step) {
      case 1:
        return (
          <Card>
            <CardHeader>
              <CardTitle>Upload Your Resume</CardTitle>
            </CardHeader>
            
            <CardContent className="pt-6">
              <div 
                {...getRootProps()} 
                className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
                  isDragActive 
                    ? 'border-primary-500 bg-primary-50' 
                    : 'border-gray-300 hover:border-primary-500'
                }`}
              >
                <input {...getInputProps()} />
                
                {file ? (
                  <div className="space-y-2">
                    <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center mx-auto">
                      <DocumentTextIcon className="h-8 w-8 text-primary-600" />
                    </div>
                    <div className="text-sm text-gray-500">Selected file:</div>
                    <div className="text-lg font-medium text-primary-600">{file.name}</div>
                    <div className="flex justify-center gap-2">
                      <Button 
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setFile(null);
                        }}
                        className="mt-2 text-sm text-danger-600 hover:text-danger-700"
                      >
                        Remove
                      </Button>
                      <Button 
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          console.log('Manual step progression');
                          // Create empty resume data if needed
                          if (!resumeData) {
                            const emptyData = {
                              contactInfo: {
                                name: 'Your Name',
                                email: 'your.email@example.com',
                                phone: '123-456-7890',
                                location: 'City, State',
                                linkedin: '',
                                github: '',
                                portfolio: '',
                              },
                              summary: 'Professional summary goes here...',
                              experience: [],
                              education: [],
                              skills: {
                                categories: [{ name: 'Skills', skills: ['Skill 1', 'Skill 2', 'Skill 3'] }]
                              },
                              projects: [],
                              certifications: [],
                              additionalSections: []
                            };
                            handleUpdateResumeData(emptyData);
                          }
                          setStep(2);
                        }}
                        className="mt-2 text-sm"
                      >
                        Continue Manually
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <DocumentTextIcon className="h-12 w-12 mx-auto text-gray-400" />
                    <p className="text-gray-500">
                      Drag and drop your resume here, or click to browse
                    </p>
                    <p className="text-xs text-gray-400">
                      Supported formats: PDF, DOC, DOCX, TXT
                    </p>
                  </div>
                )}
              </div>
              
              <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <h3 className="text-sm font-medium mb-2">Troubleshooting:</h3>
                <p className="text-xs text-gray-600 mb-2">If your resume upload is not working:</p>
                <ul className="text-xs text-gray-600 list-disc list-inside space-y-1">
                  <li>Try using the <Link href="/test-pdf" className="text-primary-600 hover:underline">PDF Test Page</Link> to check file compatibility</li>
                  <li>Use the "Continue Manually" button after selecting a file</li>
                  <li>Try converting your resume to PDF format before uploading</li>
                  <li>Check browser console for error messages</li>
                </ul>
              </div>
            </CardContent>
            
            <CardFooter className="flex justify-between">
              <Button 
                variant="outline" 
                onClick={() => window.history.back()}
              >
                Back
              </Button>
              <Button
                disabled={!file}
                onClick={() => {
                  if (resumeData) {
                    setStep(2);
                  } else {
                    toast.error('Please upload a resume file first');
                  }
                }}
              >
                Next: Choose Template
              </Button>
            </CardFooter>
          </Card>
        );
        
      case 2: // Template Selection
        return (
          <Card>
            <CardHeader>
              <CardTitle>Choose a Template</CardTitle>
            </CardHeader>
            
            <CardContent>
              <p className="text-gray-600 mb-6">
                Select a design template for your resume and customize its appearance.
              </p>
              
              <Tabs defaultValue="templates" className="w-full">
                <TabsList className="mb-4">
                  <TabsTrigger value="templates">Templates</TabsTrigger>
                  <TabsTrigger value="design">Design Options</TabsTrigger>
                </TabsList>
                
                <TabsContent value="templates">
                  {/* Check if templates and selected template are available */}
                  {RESUME_TEMPLATES && RESUME_TEMPLATES.length > 0 ? (
                    <TemplateSelector 
                      selectedTemplate={selectedTemplate || 'modern'}
                      onSelectTemplate={handleSelectTemplate}
                      designOptions={designOptions || getDefaultDesignOptions('modern')}
                      onUpdateDesignOptions={handleUpdateDesignOptions}
                    />
                  ) : (
                    <div className="p-4 border border-gray-200 rounded-md bg-gray-50 text-center">
                      <p className="text-gray-600">No templates available. Using default template.</p>
                    </div>
                  )}
                </TabsContent>
                
                <TabsContent value="design">
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Design Customization</h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Primary Color
                        </label>
                        <input 
                          type="color" 
                          value={designOptions?.primaryColor || '#2563eb'} 
                          onChange={(e) => {
                            handleUpdateDesignOptions({
                              ...designOptions,
                              primaryColor: e.target.value
                            });
                          }}
                          className="w-full h-10 rounded-md border border-gray-300"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Font Family
                        </label>
                        <select 
                          value={designOptions?.fontFamily || 'Inter, sans-serif'} 
                          onChange={(e) => {
                            handleUpdateDesignOptions({
                              ...designOptions,
                              fontFamily: e.target.value
                            });
                          }}
                          className="w-full p-2 border border-gray-300 rounded-md"
                        >
                          <option value="Inter, sans-serif">Inter (Sans-serif)</option>
                          <option value="Georgia, serif">Georgia (Serif)</option>
                          <option value="Montserrat, sans-serif">Montserrat (Sans-serif)</option>
                          <option value="Source Code Pro, monospace">Source Code Pro (Monospace)</option>
                        </select>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Font Size Scale
                      </label>
                      <input 
                        type="range" 
                        min="0.8" 
                        max="1.2" 
                        step="0.05" 
                        value={designOptions?.fontSize?.normal ? designOptions.fontSize.normal / 12 : 1} 
                        onChange={(e) => {
                          const scale = parseFloat(e.target.value);
                          const baseFontSize = 12;
                          handleUpdateDesignOptions({
                            ...designOptions,
                            fontSize: {
                              name: Math.round(24 * scale),
                              sectionTitle: Math.round(16 * scale),
                              itemTitle: Math.round(14 * scale),
                              normal: Math.round(baseFontSize * scale)
                            }
                          });
                        }}
                        className="w-full"
                      />
                      <div className="flex justify-between text-xs text-gray-500">
                        <span>Smaller</span>
                        <span>Default</span>
                        <span>Larger</span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Line Spacing
                        </label>
                        <input 
                          type="range" 
                          min="1" 
                          max="2" 
                          step="0.1" 
                          value={designOptions?.lineSpacing || 1.5} 
                          onChange={(e) => {
                            handleUpdateDesignOptions({
                              ...designOptions,
                              lineSpacing: parseFloat(e.target.value)
                            });
                          }}
                          className="w-full"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Section Spacing
                        </label>
                        <input 
                          type="range" 
                          min="10" 
                          max="30" 
                          step="1" 
                          value={designOptions?.sectionSpacing || 20} 
                          onChange={(e) => {
                            handleUpdateDesignOptions({
                              ...designOptions,
                              sectionSpacing: parseInt(e.target.value)
                            });
                          }}
                          className="w-full"
                        />
                      </div>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
            
            <CardFooter className="flex justify-between">
              <Button 
                variant="outline" 
                onClick={() => setStep(1)}
              >
                Back
              </Button>
              <Button
                onClick={() => setStep(3)}
              >
                Next: Edit Content
              </Button>
            </CardFooter>
          </Card>
        );
        
      case 3: // Edit Content
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Edit Your Resume</h1>
              <p className="text-gray-500 max-w-2xl mx-auto">
                {file ? 'We\'ve extracted your resume data. Review and edit each section as needed.' : 'Customize your resume content section by section.'}
              </p>
            </div>
            
            <Tabs defaultValue="edit" className="w-full">
              <TabsList className="mb-4 grid grid-cols-2">
                <TabsTrigger value="edit">Edit Content</TabsTrigger>
                <TabsTrigger value="preview">Preview</TabsTrigger>
              </TabsList>
              
              <TabsContent value="edit" className="space-y-4">
                <Card>
                  <CardContent className="pt-6 pb-6">
                    {resumeData && (
                      <ResumeEditor 
                        resumeData={resumeData}
                        onUpdateResumeData={handleUpdateResumeData}
                        activeSection={activeSection}
                        setActiveSection={handleSetActiveSection}
                      />
                    )}
                  </CardContent>
                </Card>
                
                <div className="flex justify-between mt-4">
                  <Button
                    variant="outline"
                    onClick={() => setStep(2)}
                  >
                    Back to Templates
                  </Button>
                  
                  <Button
                    disabled={isExporting}
                    onClick={handleExportPDF}
                  >
                    {isExporting ? 'Exporting...' : 'Export to PDF'}
                  </Button>
                </div>
              </TabsContent>
              
              <TabsContent value="preview">
                <Card>
                  <CardContent className="p-0 pt-6 pb-6 overflow-auto">
                    {resumeData && (
                      <ResumePreview 
                        resumeData={resumeData}
                        templateId={selectedTemplate}
                      />
                    )}
                  </CardContent>
                </Card>
                
                <div className="flex justify-between mt-4">
                  <Button
                    variant="outline"
                    onClick={() => setStep(2)}
                  >
                    Back to Templates
                  </Button>
                  
                  <Button
                    disabled={isExporting}
                    onClick={handleExportPDF}
                  >
                    {isExporting ? 'Exporting...' : 'Export to PDF'}
                  </Button>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        );
        
      default:
        return null;
    }
  };
  
  return (
    <div className="container mx-auto py-8 px-4 max-w-6xl">
      <h1 className="text-3xl font-bold mb-2">Resume Builder</h1>
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center space-x-4">
            <Badge variant={step === 1 ? "default" : "outline"} className="px-4 py-2">
              <span className="mr-2">1</span> Upload Resume
            </Badge>
            <ChevronRightIcon className="h-4 w-4 text-gray-400" />
            <Badge variant={step === 2 ? "default" : "outline"} className="px-4 py-2">
              <span className="mr-2">2</span> Select Template
            </Badge>
            <ChevronRightIcon className="h-4 w-4 text-gray-400" />
            <Badge variant={step === 3 ? "default" : "outline"} className="px-4 py-2">
              <span className="mr-2">3</span> Edit Content
            </Badge>
          </div>
          
          <Link href="/pdf-test" className="text-sm text-primary-600 hover:underline">
            PDF Test Page
          </Link>
        </div>
      
        <div className="h-2 bg-gray-100 rounded-full">
          <div
            className={`h-full bg-primary-600 rounded-full transition-all duration-300 ${
              step === 1 ? 'w-1/3' : step === 2 ? 'w-2/3' : 'w-full'
            }`}
          ></div>
        </div>
      </div>

      {renderStepContent()}

      <div className="mt-10 flex justify-center">
        <Link href="/pdf-test" className="inline-flex items-center rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700">
          <DocumentTextIcon className="mr-2 h-5 w-5" />
          Preview PDF
        </Link>
      </div>
    </div>
  );
} 
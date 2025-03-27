import React, { useRef, useState, useEffect } from 'react';
import { ResumeData } from '@/types/resume';
import { getTemplateById } from '@/lib/resumeTemplates';

interface ResumePreviewProps {
  resumeData: ResumeData;
  templateId: string;
  scale?: number;
}

const ResumePreview: React.FC<ResumePreviewProps> = ({ 
  resumeData, 
  templateId = 'modern',
  scale = 1 
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [fontSize, setFontSize] = useState(1);
  const [contentOverflow, setContentOverflow] = useState(false);
  
  // Get template configuration
  const template = getTemplateById(templateId);
  
  // Function to format dates
  const formatDate = (date?: string) => {
    if (!date) return '';
    if (date.toLowerCase() === 'present') return 'Present';
    return date;
  };
  
  // Calculate font size scaling based on content amount
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Reset font size for measurement
    containerRef.current.style.fontSize = '1rem';
    
    // Check if content overflows the page height (11 inches = 1056px at 96dpi)
    const maxHeight = 1056; // 11 inches
    const currentHeight = containerRef.current.scrollHeight;
    
    if (currentHeight > maxHeight) {
      setContentOverflow(true);
      // Calculate scaling factor (with a minimum to prevent too small text)
      const newScale = Math.max(0.75, maxHeight / currentHeight);
      setFontSize(newScale);
    } else {
      setContentOverflow(false);
      setFontSize(1);
    }
  }, [resumeData, templateId]);
  
  // Render the appropriate layout based on template
  return (
    <div className="relative max-w-[8.5in] mx-auto shadow-lg border border-gray-200 bg-white">
      {/* Show overflow warning if content doesn't fit on one page */}
      {contentOverflow && (
        <div className="absolute top-0 right-0 bg-warning-100 text-warning-700 text-xs px-2 py-1 rounded-bl-md z-10">
          Content may overflow one page
        </div>
      )}
      
      <div 
        ref={containerRef}
        className="relative w-full aspect-[8.5/11] bg-white overflow-hidden"
        style={{
          transform: `scale(${scale})`,
          transformOrigin: 'top left',
          fontSize: `${fontSize}rem`,
        }}
      >
        {template.sections.contactInfo.position === 'sidebar' ? (
          <div className="flex h-full">
            {/* Sidebar layout */}
            <div className="w-1/3 bg-gray-50 text-gray-800 p-6 border-r border-gray-200">
              {/* Contact information */}
              {template.sections.contactInfo.visible && (
                <div className="mb-8">
                  <h1 className="text-2xl font-bold mb-2">{resumeData.contactInfo.name}</h1>
                  <div className="space-y-1 text-sm">
                    {resumeData.contactInfo.email && (
                      <div>{resumeData.contactInfo.email}</div>
                    )}
                    {resumeData.contactInfo.phone && (
                      <div>{resumeData.contactInfo.phone}</div>
                    )}
                    {resumeData.contactInfo.location && (
                      <div>{resumeData.contactInfo.location}</div>
                    )}
                    {resumeData.contactInfo.linkedin && (
                      <div className="truncate">{resumeData.contactInfo.linkedin}</div>
                    )}
                    {resumeData.contactInfo.github && (
                      <div className="truncate">{resumeData.contactInfo.github}</div>
                    )}
                    {resumeData.contactInfo.portfolio && (
                      <div className="truncate">{resumeData.contactInfo.portfolio}</div>
                    )}
                  </div>
                </div>
              )}
              
              {/* Skills section (if positioned in sidebar) */}
              {template.sections.skills.visible && template.sections.skills.position === 'sidebar' && (
                <div className="mb-8">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Skills</h2>
                  <div className="space-y-3">
                    {resumeData.skills.categories.map((category, idx) => (
                      <div key={idx}>
                        <h3 className="font-medium text-sm">{category.name}</h3>
                        <ul className="text-sm mt-1">
                          {category.skills.map((skill, skillIdx) => (
                            <li key={skillIdx} className="mb-1">
                              {skill}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            {/* Main content area */}
            <div className="w-2/3 p-6 overflow-hidden">
              {/* Summary */}
              {template.sections.summary.visible && template.sections.summary.position === 'main' && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Summary</h2>
                  <p className="text-sm">{resumeData.summary}</p>
                </div>
              )}
              
              {/* Experience */}
              {template.sections.experience.visible && template.sections.experience.position === 'main' && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Experience</h2>
                  <div className="space-y-4">
                    {resumeData.experience.map((exp) => (
                      <div key={exp.id} className="text-sm">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-medium">{exp.title}</h3>
                            <div>{exp.company}</div>
                          </div>
                          <div className="text-right text-xs">
                            <div>{formatDate(exp.startDate)} - {formatDate(exp.endDate)}</div>
                            {exp.location && <div>{exp.location}</div>}
                          </div>
                        </div>
                        <ul className="mt-1 pl-5 list-disc space-y-1 text-sm">
                          {exp.bullets.map((bullet, idx) => (
                            <li key={idx}>{bullet}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Education */}
              {template.sections.education.visible && template.sections.education.position === 'main' && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Education</h2>
                  <div className="space-y-4">
                    {resumeData.education.map((edu) => (
                      <div key={edu.id} className="text-sm">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-medium">{edu.institution}</h3>
                            <div>{edu.degree}{edu.field ? `, ${edu.field}` : ''}</div>
                          </div>
                          <div className="text-right text-xs">
                            <div>{formatDate(edu.startDate)} - {formatDate(edu.endDate)}</div>
                            {edu.location && <div>{edu.location}</div>}
                            {edu.gpa && <div>GPA: {edu.gpa}</div>}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Skills (if positioned in main) */}
              {template.sections.skills.visible && template.sections.skills.position === 'main' && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Skills</h2>
                  <div className="space-y-2">
                    {resumeData.skills.categories.map((category, idx) => (
                      <div key={idx} className="text-sm">
                        <div className="font-medium">{category.name}:</div>
                        <div>{category.skills.join(', ')}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Projects */}
              {template.sections.projects.visible && resumeData.projects.length > 0 && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Projects</h2>
                  <div className="space-y-4">
                    {resumeData.projects.map((project) => (
                      <div key={project.id} className="text-sm">
                        <div className="flex justify-between items-start">
                          <h3 className="font-medium">{project.name}</h3>
                          {(project.startDate || project.endDate) && (
                            <div className="text-xs">
                              {formatDate(project.startDate)} - {formatDate(project.endDate)}
                            </div>
                          )}
                        </div>
                        {project.description && <p className="text-sm">{project.description}</p>}
                        {project.bullets.length > 0 && (
                          <ul className="mt-1 pl-5 list-disc space-y-1 text-sm">
                            {project.bullets.map((bullet, idx) => (
                              <li key={idx}>{bullet}</li>
                            ))}
                          </ul>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Certifications */}
              {template.sections.certifications.visible && resumeData.certifications.length > 0 && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Certifications</h2>
                  <div className="space-y-2">
                    {resumeData.certifications.map((cert) => (
                      <div key={cert.id} className="text-sm">
                        <div className="flex justify-between">
                          <span className="font-medium">{cert.name}</span>
                          {cert.date && <span className="text-xs">{cert.date}</span>}
                        </div>
                        {cert.issuer && <div className="text-sm">{cert.issuer}</div>}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Additional Sections */}
              {template.sections.additionalSections.visible && resumeData.additionalSections.length > 0 && (
                <>
                  {resumeData.additionalSections.map((section, idx) => (
                    <div key={idx} className="mb-6">
                      <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">{section.title}</h2>
                      
                      {section.content ? (
                        <div className="text-sm whitespace-pre-line">{section.content}</div>
                      ) : section.items && section.items.length > 0 ? (
                        <div className="space-y-3">
                          {section.items.map((item) => (
                            <div key={item.id} className="text-sm">
                              <h3 className="font-medium">{item.title}</h3>
                              {item.bullets && item.bullets.length > 0 && (
                                <ul className="mt-1 pl-5 list-disc space-y-1">
                                  {item.bullets.map((bullet, bulletIdx) => (
                                    <li key={bulletIdx}>{bullet}</li>
                                  ))}
                                </ul>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-sm text-gray-500 italic">No content</div>
                      )}
                    </div>
                  ))}
                </>
              )}
            </div>
          </div>
        ) : (
          // Header layout (default)
          <div className="h-full flex flex-col">
            {/* Header with contact information */}
            {template.sections.contactInfo.visible && (
              <div className="bg-gray-50 p-6 border-b border-gray-200">
                <h1 className="text-3xl font-bold text-center">{resumeData.contactInfo.name}</h1>
                <div className="flex justify-center flex-wrap gap-x-4 mt-2 text-sm text-gray-600">
                  {resumeData.contactInfo.email && (
                    <div>{resumeData.contactInfo.email}</div>
                  )}
                  {resumeData.contactInfo.phone && (
                    <div>{resumeData.contactInfo.phone}</div>
                  )}
                  {resumeData.contactInfo.location && (
                    <div>{resumeData.contactInfo.location}</div>
                  )}
                </div>
                <div className="flex justify-center flex-wrap gap-x-4 mt-1 text-sm text-gray-600">
                  {resumeData.contactInfo.linkedin && (
                    <div className="truncate">{resumeData.contactInfo.linkedin}</div>
                  )}
                  {resumeData.contactInfo.github && (
                    <div className="truncate">{resumeData.contactInfo.github}</div>
                  )}
                  {resumeData.contactInfo.portfolio && (
                    <div className="truncate">{resumeData.contactInfo.portfolio}</div>
                  )}
                </div>
              </div>
            )}
            
            {/* Main content */}
            <div className="flex-1 p-6 overflow-hidden">
              {/* Summary */}
              {template.sections.summary.visible && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Summary</h2>
                  <p className="text-sm">{resumeData.summary}</p>
                </div>
              )}
              
              {/* Experience */}
              {template.sections.experience.visible && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Experience</h2>
                  <div className="space-y-4">
                    {resumeData.experience.map((exp) => (
                      <div key={exp.id} className="text-sm">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-medium">{exp.title}</h3>
                            <div>{exp.company}</div>
                          </div>
                          <div className="text-right text-xs">
                            <div>{formatDate(exp.startDate)} - {formatDate(exp.endDate)}</div>
                            {exp.location && <div>{exp.location}</div>}
                          </div>
                        </div>
                        <ul className="mt-1 pl-5 list-disc space-y-1 text-sm">
                          {exp.bullets.map((bullet, idx) => (
                            <li key={idx}>{bullet}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Education */}
              {template.sections.education.visible && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Education</h2>
                  <div className="space-y-4">
                    {resumeData.education.map((edu) => (
                      <div key={edu.id} className="text-sm">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-medium">{edu.institution}</h3>
                            <div>{edu.degree}{edu.field ? `, ${edu.field}` : ''}</div>
                          </div>
                          <div className="text-right text-xs">
                            <div>{formatDate(edu.startDate)} - {formatDate(edu.endDate)}</div>
                            {edu.location && <div>{edu.location}</div>}
                            {edu.gpa && <div>GPA: {edu.gpa}</div>}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Skills */}
              {template.sections.skills.visible && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Skills</h2>
                  <div className="space-y-2">
                    {resumeData.skills.categories.map((category, idx) => (
                      <div key={idx} className="text-sm">
                        <div className="font-medium">{category.name}:</div>
                        <div>{category.skills.join(', ')}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Projects */}
              {template.sections.projects.visible && resumeData.projects.length > 0 && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Projects</h2>
                  <div className="space-y-4">
                    {resumeData.projects.map((project) => (
                      <div key={project.id} className="text-sm">
                        <div className="flex justify-between items-start">
                          <h3 className="font-medium">{project.name}</h3>
                          {(project.startDate || project.endDate) && (
                            <div className="text-xs">
                              {formatDate(project.startDate)} - {formatDate(project.endDate)}
                            </div>
                          )}
                        </div>
                        {project.description && <p className="text-sm">{project.description}</p>}
                        {project.bullets.length > 0 && (
                          <ul className="mt-1 pl-5 list-disc space-y-1 text-sm">
                            {project.bullets.map((bullet, idx) => (
                              <li key={idx}>{bullet}</li>
                            ))}
                          </ul>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Certifications */}
              {template.sections.certifications.visible && resumeData.certifications.length > 0 && (
                <div className="mb-6">
                  <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">Certifications</h2>
                  <div className="space-y-2">
                    {resumeData.certifications.map((cert) => (
                      <div key={cert.id} className="text-sm">
                        <div className="flex justify-between">
                          <span className="font-medium">{cert.name}</span>
                          {cert.date && <span className="text-xs">{cert.date}</span>}
                        </div>
                        {cert.issuer && <div className="text-sm">{cert.issuer}</div>}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Additional Sections */}
              {template.sections.additionalSections.visible && resumeData.additionalSections.length > 0 && (
                <>
                  {resumeData.additionalSections.map((section, idx) => (
                    <div key={idx} className="mb-6">
                      <h2 className="text-lg font-bold border-b border-gray-300 pb-1 mb-3">{section.title}</h2>
                      
                      {section.content ? (
                        <div className="text-sm whitespace-pre-line">{section.content}</div>
                      ) : section.items && section.items.length > 0 ? (
                        <div className="space-y-3">
                          {section.items.map((item) => (
                            <div key={item.id} className="text-sm">
                              <h3 className="font-medium">{item.title}</h3>
                              {item.bullets && item.bullets.length > 0 && (
                                <ul className="mt-1 pl-5 list-disc space-y-1">
                                  {item.bullets.map((bullet, bulletIdx) => (
                                    <li key={bulletIdx}>{bullet}</li>
                                  ))}
                                </ul>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-sm text-gray-500 italic">No content</div>
                      )}
                    </div>
                  ))}
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumePreview; 
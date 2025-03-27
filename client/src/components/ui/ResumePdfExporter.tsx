import React, { useState } from 'react';

interface ResumePdfExporterProps {
  content: string;
  originalFormat?: any; // Original format metadata
  filename?: string;
  version?: string; // Which version is being exported
}

// Define types
type ContentType = Array<any>;
type StylesType = Record<string, any>;

/**
 * ResumePdfExporter - Component to export resume as a professionally formatted PDF
 * 
 * This component creates a PDF document that matches the displayed resume format exactly
 */
const ResumePdfExporter: React.FC<ResumePdfExporterProps> = ({ 
  content, 
  originalFormat, 
  filename = 'resume.pdf',
  version = 'optimized'
}) => {
  const [isLoading, setIsLoading] = useState(false);

  // Generate and download PDF
  const generatePdf = async () => {
    setIsLoading(true);
    
    try {
      // Use simple approach to add pdfmake script
      const script = document.createElement('script');
      script.src = 'https://unpkg.com/pdfmake@0.2.7/build/pdfmake.min.js';
      script.onload = () => {
        const vfsScript = document.createElement('script');
        vfsScript.src = 'https://unpkg.com/pdfmake@0.2.7/build/vfs_fonts.js';
        vfsScript.onload = () => {
          try {
            // Now create PDF content
            const contentArr = parseResumeContent(content);
            const styles = generateStyles();
            
            // Create document definition
            const docDefinition = {
              content: contentArr,
              styles: styles,
              pageSize: 'LETTER',
              pageMargins: [30, 20, 30, 20],
              defaultStyle: {
                font: 'Roboto',
                fontSize: 9,
                lineHeight: 1,
                color: '#333333'
              },
              info: {
                title: `Resume - ${version.charAt(0).toUpperCase() + version.slice(1)}`,
                author: extractAuthorName(content),
                subject: 'Professional Resume',
                keywords: 'resume, CV, professional'
              }
            };
            
            // Create and download PDF
            // @ts-ignore
            window.pdfMake.createPdf(docDefinition).download(filename);
            setIsLoading(false);
          } catch (innerError) {
            console.error('Error creating PDF:', innerError);
            downloadTextFallback();
          }
        };
        
        vfsScript.onerror = () => {
          console.error('Error loading vfs_fonts.js');
          downloadTextFallback();
        };
        
        document.body.appendChild(vfsScript);
      };
      
      script.onerror = () => {
        console.error('Error loading pdfmake.min.js');
        downloadTextFallback();
      };
      
      document.body.appendChild(script);
      
    } catch (error) {
      console.error('Error in PDF generation process:', error);
      downloadTextFallback();
    }
  };
  
  // Fallback function for downloading as text
  const downloadTextFallback = () => {
    try {
      const element = document.createElement('a');
      const file = new Blob([content], { type: 'text/plain' });
      element.href = URL.createObjectURL(file);
      element.download = filename.replace('.pdf', '.txt');
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      alert('PDF generation failed. Downloading as text file instead.');
    } catch (fallbackError) {
      console.error('Even fallback download failed:', fallbackError);
      alert('Could not generate PDF. Please try again or contact support.');
    } finally {
      setIsLoading(false);
    }
  };
  
  // Extract author name from resume content for PDF metadata
  const extractAuthorName = (text: string): string => {
    // Typically, the author name is in the first line of the resume
    const lines = text.split('\n');
    if (lines.length > 0) {
      const firstLine = lines[0].trim();
      // Remove any formatting markers
      return firstLine.replace(/<[^>]+>/g, '').trim();
    }
    return 'Resume';
  };
  
  // Parse resume content into pdfMake format
  const parseResumeContent = (text: string): ContentType => {
    const result: ContentType = [];
    
    // IMPORTANT: Filter out any "Skills Emphasized" line
    const filteredLines = text.split('\n')
      .filter(line => !line.includes('Skills Emphasized'));
    
    // Check if this contains our formatting markers
    const hasFormatting = text.includes('<HEADER>') || text.includes('</HEADER>') || text.includes('<BULLET>') || text.includes('<INDENT');
    
    // Extract name and contact info from the beginning of the resume
    let name = '';
    let contactInfo = '';
    let contentStartIndex = 0;
    
    for (let i = 0; i < Math.min(5, filteredLines.length); i++) {
      const line = filteredLines[i].trim();
      if (!line) continue;
      
      if (name === '') {
        name = line.replace(/<[^>]+>/g, '').trim();
        contentStartIndex = i + 1;
        continue;
      }
      
      if (contactInfo === '') {
        contactInfo = line.replace(/<[^>]+>/g, '').trim();
        contentStartIndex = i + 1;
        break;
      }
    }
    
    // Add name at the top with proper styling
    if (name) {
      result.push({
        text: name,
        style: 'name',
        alignment: 'center'
      });
    }
    
    // Add contact info with proper styling
    if (contactInfo) {
      result.push({
        text: contactInfo,
        style: 'contactInfo',
        alignment: 'center'
      });
    }
    
    // Process each section of the resume
    let currentSection = '';
    let inBulletList = false;
    let bulletItems: any[] = [];
    
    for (let i = contentStartIndex; i < filteredLines.length; i++) {
      const line = filteredLines[i].trim();
      if (!line) continue;
      
      // Clean up any formatting markers
      const cleanLine = line
        .replace(/<HEADER>(.*?)<\/HEADER>/g, '$1')
        .replace(/<SUBHEADER>(.*?)<\/SUBHEADER>/g, '$1')
        .replace(/<BULLET>/g, '')
        .replace(/<INDENT level="(\d+)">(.*?)<\/INDENT>/g, '$2');
      
      // Is this a section header? (EDUCATION, EXPERIENCE, SKILLS, etc.)
      if (/^[A-Z][A-Z\s]+$/.test(cleanLine) && 
          (cleanLine === 'EDUCATION' || 
           cleanLine === 'EXPERIENCE' || 
           cleanLine === 'SKILLS' || 
           cleanLine === 'PROJECTS' ||
           cleanLine === 'CERTIFICATIONS' ||
           cleanLine === 'AWARDS')) {
        
        // Close any open bullet list
        if (inBulletList) {
          result.push({
            ul: bulletItems,
            style: 'bulletList'
          });
          bulletItems = [];
          inBulletList = false;
        }
        
        currentSection = cleanLine;
        
        // Add section header
        result.push({
          text: cleanLine,
          style: 'header'
        });
        
        // Add divider line
        result.push({
          canvas: [{ 
            type: 'line', 
            x1: 0, 
            y1: 0, 
            x2: 515, 
            y2: 0, 
            lineWidth: 1, 
            lineColor: '#888888' 
          }],
          margin: [0, 2, 0, 5]
        });
        
        continue;
      }
      
      // Handle bullet points
      if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*')) {
        if (!inBulletList) {
          inBulletList = true;
          bulletItems = [];
        }
        
        bulletItems.push({
          text: cleanLine.substring(1).trim(),
          margin: [0, 0, 0, 2]
        });
        
        continue;
      }
      
      // Close bullet list if we're not on a bullet point anymore
      if (inBulletList && !(line.startsWith('•') || line.startsWith('-') || line.startsWith('*'))) {
        result.push({
          ul: bulletItems,
          style: 'bulletList'
        });
        bulletItems = [];
        inBulletList = false;
      }
      
      // Handle company/organization names
      if (currentSection === 'EXPERIENCE' && line === line.toUpperCase() && line.length > 3) {
        // Company name with location
        result.push({
          text: cleanLine,
          style: 'companyName'
        });
        continue;
      }
      
      // Handle job titles with dates (typically follows company name)
      if (currentSection === 'EXPERIENCE' && /\d{4}\s*-\s*\d{4}/.test(cleanLine)) {
        // Format with job title and date
        const dateMatch = cleanLine.match(/\d{4}\s*-\s*\d{4}/);
        if (dateMatch) {
          const dateIndex = cleanLine.indexOf(dateMatch[0]);
          if (dateIndex > 0) {
            const title = cleanLine.substring(0, dateIndex).trim();
            const date = dateMatch[0];
            
            result.push({
              columns: [
                {
                  text: title,
                  style: 'jobTitle',
                  width: '*',
                  italics: true
                },
                {
                  text: date,
                  style: 'jobDate',
                  width: 'auto',
                  alignment: 'right'
                }
              ],
              margin: [0, 2, 0, 4]
            });
            continue;
          }
        }
      }
      
      // Handle project titles with dates
      if ((currentSection === 'PROJECTS' || /who paid who|olympus|memento|socialsync/i.test(currentSection)) && 
          (/\d{4}\s*-\s*\d{4}/.test(cleanLine) || 
           /(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*-/.test(cleanLine))) {
        
        // If it's a standalone date line, add it right-aligned
        if (/^\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*-/.test(cleanLine) ||
            /^\s*\d{4}\s*-\s*\d{4}\s*$/.test(cleanLine)) {
          result.push({
            text: cleanLine,
            style: 'projectDate',
            alignment: 'right'
          });
        } else {
          // It's a project title with date
          const dateMatch = cleanLine.match(/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*-.*\d{4}/) || 
                           cleanLine.match(/\d{4}\s*-\s*\d{4}/);
          
          if (dateMatch) {
            const dateIndex = cleanLine.indexOf(dateMatch[0]);
            if (dateIndex > 0) {
              const projectName = cleanLine.substring(0, dateIndex).trim();
              const date = dateMatch[0];
              
              result.push({
                columns: [
                  {
                    text: projectName,
                    style: 'projectName',
                    width: '*'
                  },
                  {
                    text: date,
                    style: 'projectDate',
                    width: 'auto',
                    alignment: 'right'
                  }
                ],
                margin: [0, 4, 0, 2]
              });
              continue;
            }
          }
        }
      }
      
      // Handle degree information
      if (currentSection === 'EDUCATION' && (/bachelor|master|b\.s\.|m\.s\.|ph\.?d|gpa/i.test(cleanLine))) {
        result.push({
          text: cleanLine,
          style: 'degreeInfo'
        });
        continue;
      }
      
      // Default handling for any other text
      result.push({
        text: cleanLine,
        style: 'regularText'
      });
    }
    
    // Close any remaining open bullet list
    if (inBulletList && bulletItems.length > 0) {
      result.push({
        ul: bulletItems,
        style: 'bulletList'
      });
    }
    
    return result;
  };
  
  // Generate styles based on the displayed format
  const generateStyles = (): StylesType => {
    const styles: StylesType = {
      name: {
        fontSize: 16,
        bold: true,
        margin: [0, 0, 0, 2],
        color: '#1a1a1a'
      },
      contactInfo: {
        fontSize: 9,
        color: '#505050',
        margin: [0, 2, 0, 10]
      },
      header: {
        fontSize: 12,
        bold: true,
        margin: [0, 6, 0, 2],
        color: '#1a1a1a'
      },
      companyName: {
        fontSize: 10,
        bold: true,
        margin: [0, 6, 0, 2]
      },
      jobTitle: {
        fontSize: 10,
        italics: true,
        margin: [0, 1, 0, 1]
      },
      jobDate: {
        fontSize: 9,
        italics: true,
        color: '#505050'
      },
      projectName: {
        fontSize: 10,
        bold: true,
        margin: [0, 2, 0, 1]
      },
      projectDate: {
        fontSize: 9,
        italics: true,
        color: '#505050'
      },
      degreeInfo: {
        fontSize: 10,
        margin: [0, 1, 0, 2]
      },
      regularText: {
        fontSize: 9,
        margin: [0, 1, 0, 2]
      },
      bulletList: {
        margin: [10, 0, 0, 4]
      }
    };
    
    return styles;
  };
  
  return (
    <button 
      onClick={generatePdf}
      disabled={isLoading}
      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        className="h-5 w-5 mr-2" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      {isLoading ? 'Generating PDF...' : `Download ${version.charAt(0).toUpperCase() + version.slice(1)} PDF`}
    </button>
  );
};

// Add a declaration for the pdfMake global
declare global {
  interface Window {
    pdfMake: any;
  }
}

export default ResumePdfExporter; 
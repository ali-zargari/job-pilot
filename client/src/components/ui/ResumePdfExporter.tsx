import React, { useEffect, useState } from 'react';

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
 * This component creates a PDF document that aims to match the original PDF's formatting
 * as closely as possible, while incorporating the optimized content.
 */
const ResumePdfExporter: React.FC<ResumePdfExporterProps> = ({ 
  content, 
  originalFormat, 
  filename = 'resume.pdf',
  version = 'optimized'
}) => {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  // Parse content and convert to pdfMake format
  const generatePdf = async () => {
    if (typeof window === 'undefined') return;

    // Dynamically import pdfMake only on the client side
    const pdfMake = (await import('pdfmake/build/pdfmake')).default;
    const pdfFonts = (await import('pdfmake/build/vfs_fonts')).default;
    
    // Initialize fonts
    pdfMake.vfs = pdfFonts.pdfMake.vfs;
    
    const contentArr = parseResumeContent(content);
    const styles = generateStyles(originalFormat);
    
    // Create a professional-looking document definition
    const docDefinition = {
      content: contentArr,
      styles: styles,
      pageSize: 'LETTER',
      pageMargins: [50, 40, 50, 40], // Slightly wider margins for a more professional look
      defaultStyle: {
        font: 'Roboto',
        fontSize: 10,
        lineHeight: 1.3,
        color: '#333333'
      },
      info: {
        title: `Resume - ${version.charAt(0).toUpperCase() + version.slice(1)}`,
        author: extractAuthorName(content),
        subject: 'Professional Resume',
        keywords: 'resume, CV, professional'
      }
    };
    
    // Generate and download PDF
    pdfMake.createPdf(docDefinition).download(filename);
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
    const lines = text.split('\n');
    
    // Check if this contains our formatting markers
    const hasFormatting = text.includes('<HEADER>') || text.includes('</HEADER>') || text.includes('<BULLET>') || text.includes('<INDENT');
    
    // Function to determine if a line is a header (all caps)
    const isHeader = (line: string): boolean => {
      return /^[A-Z][A-Z\s]+$/.test(line.trim());
    };
    
    // Function to determine if a line is a subheader (mixed case with trailing colon)
    const isSubheader = (line: string): boolean => {
      return /^([A-Za-z][a-z\s]+ ?)+:$/.test(line.trim()) || 
             /^(.+?)[_]{3,}/.test(line.trim()); // Match text with multiple underscores
    };
    
    // Function to determine if a line is a bullet point
    const isBullet = (line: string): boolean => {
      return line.trim().startsWith('•') || line.trim().startsWith('-') || line.trim().startsWith('*');
    };
    
    // Special handling for the user's resume format
    let seenFirstHeader = false;
    let inHeaderTag = false;
    let nameFound = false;
    
    // First pass to extract the name and contact info
    let name = '';
    let contactInfo = '';
    
    for (let i = 0; i < Math.min(5, lines.length); i++) {
      const line = lines[i].trim();
      if (!line) continue;
      
      if (!nameFound) {
        name = line.replace(/<[^>]+>/g, '').trim();
        nameFound = true;
        continue;
      }
      
      // Assume the second non-empty line is contact info
      contactInfo = line.replace(/<[^>]+>/g, '').trim();
      break;
    }
    
    // Add name at the top
    if (name) {
      result.push({
        text: name,
        style: 'name',
        alignment: 'center'
      });
    }
    
    // Add contact info
    if (contactInfo) {
      result.push({
        text: contactInfo,
        style: 'contactInfo',
        alignment: 'center',
        margin: [0, 5, 0, 15]
      });
    }
    
    // Process each line for main content
    let inBulletList = false;
    let currentBulletItems: ContentType = [];
    let inProjectTitle = false;
    let projectTitle = '';
    let projectDate = '';
    
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i].trim();
      if (!line) continue;
      
      // Skip the name and contact info lines already processed
      if (i < 2 && (line === name || line === contactInfo)) continue;
      
      // Process header tags
      if (line.includes('<HEADER>')) {
        inHeaderTag = true;
        // Extract header text
        const headerText = line.replace(/<HEADER>(.+?)(<\/HEADER>)?/g, '$1').trim();
        
        // End any open bullet list
        if (inBulletList) {
          result.push({
            ul: currentBulletItems,
            style: 'bulletList'
          });
          inBulletList = false;
          currentBulletItems = [];
        }
        
        // Add section header
        result.push({
          text: headerText,
          style: 'header',
          margin: [0, 15, 0, 5]
        });
        
        // Add a dividing line
        result.push({
          canvas: [{ type: 'line', x1: 0, y1: 2, x2: 515, y2: 2, lineWidth: 1, lineColor: '#888888' }],
          margin: [0, 0, 0, 8]
        });
        
        seenFirstHeader = true;
        continue;
      }
      
      // Handle closing header tag
      if (line.includes('</HEADER>')) {
        inHeaderTag = false;
        continue;
      }
      
      // Process project titles with underscores
      if (/(.+?)_{3,}(.+?)$/.test(line)) {
        // This looks like "Project Name_______________Date"
        const parts = line.split(/_{3,}/);
        if (parts.length >= 2) {
          projectTitle = parts[0].trim();
          projectDate = parts[1].trim();
          
          // End any open bullet list
          if (inBulletList) {
            result.push({
              ul: currentBulletItems,
              style: 'bulletList'
            });
            inBulletList = false;
            currentBulletItems = [];
          }
          
          // Add project title with date
          result.push({
            columns: [
              {
                text: projectTitle,
                style: 'subheader',
                width: '*'
              },
              {
                text: projectDate,
                style: 'projectDate',
                width: 'auto',
                alignment: 'right'
              }
            ],
            margin: [0, 10, 0, 3]
          });
          
          inProjectTitle = true;
          continue;
        }
      }
      
      // Clean up any formatting markers for regular content
      let cleanLine = line
        .replace(/<HEADER>(.*?)<\/HEADER>/g, '$1')
        .replace(/<SUBHEADER>(.*?)<\/SUBHEADER>/g, '$1')
        .replace(/<BULLET>/g, '')
        .replace(/<INDENT level="(\d+)">(.*?)<\/INDENT>/g, '$2');
      
      // Bullet points
      if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*')) {
        // Start bullet list if not already in one
        if (!inBulletList) {
          inBulletList = true;
          currentBulletItems = [];
        }
        
        // Add bullet item
        const bulletText = cleanLine.replace(/^[•\-*]\s*/, '');
        currentBulletItems.push({
          text: bulletText,
          margin: [0, 1, 0, 1]
        });
        continue;
      }
      
      // Regular text or subheaders that don't match our patterns
      if (!inBulletList) {
        // If it's a company name or institution (preceded by header usually)
        if (seenFirstHeader && /^[A-Z]/.test(cleanLine) && cleanLine === cleanLine.toUpperCase() && !line.includes('<HEADER>')) {
          result.push({
            text: cleanLine,
            style: 'companyName',
            margin: [0, 8, 0, 2]
          });
        } 
        // If it looks like a job title or position (follows company name)
        else if (!/^[A-Z]{2,}/.test(cleanLine) && !inProjectTitle) {
          result.push({
            text: cleanLine,
            style: 'regularText',
            margin: [0, 2, 0, 2]
          });
        }
      } else {
        // If we get a non-bullet line but are in a bullet list, check if it's a continuation
        if (!cleanLine.startsWith('•') && !cleanLine.startsWith('-') && !cleanLine.startsWith('*')) {
          // Just add to the last bullet point
          if (currentBulletItems.length > 0) {
            const lastItem = currentBulletItems[currentBulletItems.length - 1];
            lastItem.text += ' ' + cleanLine;
          } else {
            // Not in a bullet list anymore
            result.push({
              text: cleanLine,
              margin: [0, 2, 0, 2]
            });
            inBulletList = false;
          }
        }
      }
    }
    
    // Close any open bullet list
    if (inBulletList && currentBulletItems.length > 0) {
      result.push({
        ul: currentBulletItems,
        style: 'bulletList'
      });
    }
    
    return result;
  };
  
  // Generate styles based on original format
  const generateStyles = (formatMetadata?: any): StylesType => {
    // Improved styles for a professional look
    const styles: StylesType = {
      name: {
        fontSize: 16,
        bold: true,
        margin: [0, 0, 0, 4],
        color: '#1a1a1a'
      },
      contactInfo: {
        fontSize: 10, 
        color: '#505050',
        margin: [0, 2, 0, 8]
      },
      header: {
        fontSize: 12,
        bold: true,
        margin: [0, 12, 0, 4],
        color: '#1a1a1a'
      },
      subheader: {
        fontSize: 11,
        bold: true,
        margin: [0, 5, 0, 2],
        color: '#333333'
      },
      companyName: {
        fontSize: 10.5,
        bold: true,
        margin: [0, 8, 0, 1]
      },
      projectDate: {
        fontSize: 10,
        italic: true,
        color: '#505050'
      },
      regularText: {
        fontSize: 10,
        margin: [0, 1, 0, 1]
      },
      bulletList: {
        margin: [15, 0, 0, 8]
      }
    };
    
    return styles;
  };
  
  // Only render the button on the client side to avoid hydration errors
  if (!isClient) {
    return null;
  }
  
  return (
    <button 
      onClick={generatePdf}
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
      Download {version.charAt(0).toUpperCase() + version.slice(1)} PDF
    </button>
  );
};

export default ResumePdfExporter; 
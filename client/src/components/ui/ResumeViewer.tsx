import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Edit2Icon, CheckIcon, XIcon } from 'lucide-react';

// Interface for the ResumeViewer component props
interface ResumeViewerProps {
  content: string;
  onUpdate?: (newContent: string) => void;
  isEditable?: boolean;
  maxHeight?: string;
  pageSize?: 'letter' | 'a4';
}

/**
 * ResumeViewer - A component that displays resume content in a PDF-like format
 * with optional inline editing capabilities.
 */
const ResumeViewer: React.FC<ResumeViewerProps> = ({
  content,
  onUpdate,
  isEditable = false,
  maxHeight = '1056px', // Default letter page height (11 inches * 96 dpi)
  pageSize = 'letter'
}) => {
  const [editMode, setEditMode] = useState(false);
  const [editContent, setEditContent] = useState(content);
  const editRef = useRef<HTMLDivElement>(null);
  
  // Update editContent when content prop changes
  useEffect(() => {
    setEditContent(content);
  }, [content]);
  
  // Calculate page dimensions
  const getPageDimensions = () => {
    if (pageSize === 'letter') {
      return {
        width: '8.5in',
        height: '11in',
        maxWidth: '816px' // 8.5 inches * 96 dpi
      };
    } else {
      return {
        width: '210mm',
        height: '297mm',
        maxWidth: '795px' // 210mm in pixels
      };
    }
  };
  
  const pageDimensions = getPageDimensions();
  
  // Format the content to preserve bullet points and formatting
  const formatContent = (text: string) => {
    // Split into lines
    const lines = text.split('\n');
    const formattedLines = [];
    
    // Process the content line by line for enhanced formatting
    let nameProcessed = false;
    let contactInfoLines = [];
    let inSection = false;
    let inSubSection = false;
    let seenFirstHeader = false;
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      if (!line) {
        formattedLines.push(<div key={`empty-${i}`} className="h-3"></div>); // Reduced empty space
        continue;
      }
      
      // Clean up any formatting markers if present
      let cleanLine = line
        .replace(/<HEADER>(.*?)<\/HEADER>/g, '$1')
        .replace(/<SUBHEADER>(.*?)<\/SUBHEADER>/g, '$1')
        .replace(/<BULLET>/g, '')
        .replace(/<INDENT level="\d+">(.*?)<\/INDENT>/g, '$1');
      
      // Get indentation level if present
      let indentLevel = 0;
      const indentMatch = line.match(/<INDENT level="(\d+)">/);
      if (indentMatch) {
        indentLevel = parseInt(indentMatch[1]);
      }
      
      // Special case: Check for SKILLS as a standalone word or at the end of a line
      if (line === "SKILLS" || line.endsWith(" SKILLS") || 
          (line.includes("<HEADER>") && line.includes("SKILLS"))) {
        seenFirstHeader = true;
        formattedLines.push(
          <div 
            key={`header-skills-${i}`} 
            className="text-base font-bold mt-4 mb-1 text-gray-800 border-b border-gray-300 pb-1"
          >
            SKILLS
          </div>
        );
        continue;
      }
      
      // Check for headers (all caps)
      const isHeader = line.includes('<HEADER>') || 
                    (line === line.toUpperCase() && line.length > 2 && line.length <= 30);
      
      // Check for sub-headers (usually ending with colon)
      const isSubHeader = line.includes('<SUBHEADER>') || 
                       (line.endsWith(':') || line.endsWith('_')) && line.length < 50;
      
      // Check for bullet points
      const isBulletPoint = line.startsWith('•') || line.startsWith('-') || line.startsWith('*');
      
      // Handle name (first line)
      if (!nameProcessed) {
        formattedLines.push(
          <div key="name" className="text-lg font-bold text-center mb-1">
            {cleanLine}
          </div>
        );
        nameProcessed = true;
        continue;
      }
      
      // Handle contact info (next few lines until a header)
      if (nameProcessed && contactInfoLines.length < 2 && !isHeader) {
        contactInfoLines.push(cleanLine);
        
        // If next line is a header or we're at the end, render contact info
        if (i + 1 >= lines.length || 
            lines[i+1].includes('<HEADER>') || 
            lines[i+1].toUpperCase() === lines[i+1]) {
          formattedLines.push(
            <div key="contact-info" className="text-xs text-gray-600 text-center mb-3">
              {contactInfoLines.join(' • ')}
            </div>
          );
          
          // Reset for the rest of the resume
          contactInfoLines = [];
        }
        continue;
      }
      
      // Handle section headers (all caps)
      if (isHeader) {
        inSection = true;
        inSubSection = false;
        seenFirstHeader = true;
        
        // Extract header text if it's in a tag
        const headerText = line.replace(/<HEADER>(.+?)(<\/HEADER>)?/g, '$1').trim();
        
        formattedLines.push(
          <div 
            key={`header-${i}`} 
            className="text-base font-bold mt-4 mb-1 text-gray-800 border-b border-gray-300 pb-1"
          >
            {headerText}
          </div>
        );
        continue;
      }
      
      // Skip </HEADER> closing tags
      if (line.includes('</HEADER>')) {
        continue;
      }
      
      // Handle project titles with underscores
      if (/(.+?)_{3,}(.+?)$/.test(line)) {
        // This looks like "Project Name_______________Date"
        const parts = line.split(/_{3,}/);
        if (parts.length >= 2) {
          const projectTitle = parts[0].trim();
          const projectDate = parts[1].trim();
          
          formattedLines.push(
            <div key={`project-${i}`} className="flex justify-between items-center mt-3 mb-1">
              <span className="font-semibold text-gray-700">{projectTitle}</span>
              <span className="text-xs text-gray-600 italic">{projectDate}</span>
            </div>
          );
          continue;
        }
      }
      
      // Handle subsection headers
      if (isSubHeader && !line.includes('_____')) {
        inSubSection = true;
        
        // Remove trailing underscores for display
        const displayLine = cleanLine.replace(/_{3,}$/, '');
        
        formattedLines.push(
          <div 
            key={`subheader-${i}`} 
            className="font-semibold mt-2 mb-1 text-gray-700"
          >
            <span>{displayLine}</span>
          </div>
        );
        continue;
      }
      
      // Handle company names and job titles (all caps after first header)
      if (seenFirstHeader && !isBulletPoint && cleanLine === cleanLine.toUpperCase() && cleanLine.length > 2) {
        formattedLines.push(
          <div 
            key={`company-${i}`}
            className="font-semibold mt-3 mb-1 text-gray-800"
          >
            {cleanLine}
          </div>
        );
        continue;
      }
      
      // Handle job title or position (not all caps, follows company)
      if (seenFirstHeader && !isBulletPoint && cleanLine !== cleanLine.toUpperCase() && 
          i > 0 && lines[i-1].toUpperCase() === lines[i-1]) {
        formattedLines.push(
          <div
            key={`position-${i}`}
            className="mb-1 text-sm"
          >
            {cleanLine}
          </div>
        );
        continue;
      }
      
      // Handle bullet points
      if (isBulletPoint) {
        const bulletText = cleanLine.substring(1).trim();
        formattedLines.push(
          <div key={`bullet-${i}`} className="pl-4 relative my-1 text-xs">
            <span className="absolute left-0">{cleanLine.charAt(0)}</span>
            <span>{bulletText}</span>
          </div>
        );
        continue;
      }
      
      // Handle indented text
      if (indentLevel > 0) {
        formattedLines.push(
          <div 
            key={`indent-${i}`} 
            className="text-xs my-1" 
            style={{ marginLeft: `${indentLevel * 12}px` }}
          >
            {cleanLine}
          </div>
        );
        continue;
      }
      
      // Regular text
      formattedLines.push(
        <div key={`text-${i}`} className="my-1 text-xs">
          {cleanLine}
        </div>
      );
    }
    
    return formattedLines;
  };
  
  // Handle saving edits
  const handleSave = () => {
    if (editRef.current && onUpdate) {
      // Get the edited content
      const newContent = editRef.current.innerText;
      onUpdate(newContent);
    }
    setEditMode(false);
  };
  
  // Cancel edits
  const handleCancel = () => {
    setEditContent(content);
    setEditMode(false);
  };
  
  return (
    <div className="relative">
      {isEditable && (
        <div className="absolute top-2 right-2 z-10 flex gap-2">
          {editMode ? (
            <>
              <Button
                size="sm"
                variant="outline"
                onClick={handleSave}
                className="bg-white"
              >
                <CheckIcon className="h-4 w-4 mr-1" />
                Save
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={handleCancel}
                className="bg-white"
              >
                <XIcon className="h-4 w-4 mr-1" />
                Cancel
              </Button>
            </>
          ) : (
            <Button
              size="sm"
              variant="outline"
              onClick={() => setEditMode(true)}
              className="bg-white"
            >
              <Edit2Icon className="h-4 w-4 mr-1" />
              Edit
            </Button>
          )}
        </div>
      )}
      
      <Card className="overflow-hidden shadow-xl">
        <div 
          className="bg-white border border-gray-200 mx-auto"
          style={{
            width: pageDimensions.width,
            maxWidth: pageDimensions.maxWidth,
            height: pageDimensions.height,
            maxHeight: maxHeight,
            overflow: 'auto',
            padding: '0.5in',
            fontFamily: 'Arial, sans-serif',
            fontSize: '11px',
            lineHeight: '1.2',
            position: 'relative'
          }}
        >
          {editMode ? (
            <div
              ref={editRef}
              contentEditable
              suppressContentEditableWarning
              className="h-full outline-none"
              style={{
                whiteSpace: 'pre-wrap'
              }}
            >
              {editContent}
            </div>
          ) : (
            <div className="h-full">
              {formatContent(content)}
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export default ResumeViewer; 
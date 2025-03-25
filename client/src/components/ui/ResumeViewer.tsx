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
    
    // Process each line to identify bullet points, sections, etc.
    return lines.map((line, index) => {
      line = line.trim();
      
      if (!line) {
        return <div key={index} className="h-4"></div>;
      }
      
      // Format section headers (all caps)
      if (line.toUpperCase() === line && line.length > 2 && line.length <= 30) {
        return (
          <div key={index} className="text-lg font-bold mt-4 mb-2 text-gray-800">
            {line}
          </div>
        );
      }
      
      // Format subsection headers (typically mixed case, likely to have trailing ':')
      if ((line.endsWith(':') || line.endsWith('_')) && line.length < 50) {
        return (
          <div key={index} className="font-semibold mt-3 mb-1 text-gray-700">
            {line}
          </div>
        );
      }
      
      // Handle bullet points
      if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*')) {
        return (
          <div key={index} className="pl-5 relative my-1 text-sm">
            <span className="absolute left-0">{line.charAt(0)}</span>
            <span>{line.substring(1).trim()}</span>
          </div>
        );
      }
      
      // Handle numbered bullet points
      if (/^\d+[.)]/.test(line)) {
        const match = line.match(/^(\d+[.)])\s*(.*)$/);
        if (match) {
          return (
            <div key={index} className="pl-5 relative my-1 text-sm">
              <span className="absolute left-0">{match[1]}</span>
              <span>{match[2]}</span>
            </div>
          );
        }
      }
      
      // Regular text
      return <div key={index} className="my-1 text-sm">{line}</div>;
    });
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
            padding: '0.75in',
            fontFamily: 'Arial, sans-serif',
            fontSize: '12px',
            lineHeight: '1.3',
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
import { NextRequest, NextResponse } from 'next/server';
import pdfParse from 'pdf-parse';
import { parse as docxParse } from 'docx-parser';

export const dynamic = 'force-dynamic'; // No caching

export async function POST(request: NextRequest) {
  console.log('API: extract-resume-text route called');
  
  try {
    // Get form data from the request
    const formData = await request.formData();
    console.log('API: Form data received');
    
    // Get the resume file from the form data
    const resumeFile = formData.get('resume') as File | null;
    
    if (!resumeFile) {
      console.error('API: No resume file provided');
      return NextResponse.json({ error: 'No resume file provided' }, { status: 400 });
    }
    
    console.log('API: File received', {
      name: resumeFile.name,
      type: resumeFile.type,
      size: resumeFile.size
    });

    let text = '';

    // Handle different file types
    if (resumeFile.type === 'application/pdf') {
      console.log('API: Processing PDF file');
      try {
        // Convert file to ArrayBuffer
        const arrayBuffer = await resumeFile.arrayBuffer();
        console.log('API: PDF file converted to ArrayBuffer', arrayBuffer.byteLength, 'bytes');
        
        // Parse the PDF with pdf-parse
        const pdfData = await pdfParse(Buffer.from(arrayBuffer));
        console.log('API: PDF successfully parsed, text length:', pdfData.text.length);
        
        // Extract text from the PDF
        text = pdfData.text;
        
        // Log a sample of extracted text for debugging
        console.log('API: Raw PDF text sample:', text.substring(0, 200));
        
        // Improve text handling to preserve formatting, bullet points, and headers
        text = cleanPdfText(text);
        
        console.log('API: Cleaned text length:', text.length);
        console.log('API: Cleaned text sample:', text.substring(0, 200));
      } catch (error) {
        console.error('API: Error parsing PDF:', error);
        return NextResponse.json({ 
          error: 'Failed to parse PDF file', 
          details: error instanceof Error ? error.message : String(error)
        }, { status: 500 });
      }
    } else if (resumeFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
      console.log('API: Processing DOCX file');
      try {
        const arrayBuffer = await resumeFile.arrayBuffer();
        const result = await docxParse(arrayBuffer);
        text = result.text;
        console.log('API: DOCX processed successfully');
      } catch (error) {
        console.error('API: Error parsing DOCX:', error);
        return NextResponse.json({ 
          error: 'Failed to parse DOCX file. Please try another format.' 
        }, { status: 400 });
      }
    } else if (resumeFile.type === 'application/msword') {
      console.log('API: Processing DOC file');
      return NextResponse.json({ 
        error: 'DOC format is not fully supported. Please convert to PDF or DOCX and try again.' 
      }, { status: 400 });
    } else if (resumeFile.type === 'text/plain') {
      console.log('API: Processing plain text file');
      text = await resumeFile.text();
      console.log('API: Text extracted from plain text file, length:', text.length);
    } else {
      // For other types like DOC/DOCX, try to extract as text, but this likely won't work well
      console.log('API: Attempting to process as plain text:', resumeFile.type);
      try {
        text = await resumeFile.text();
        console.log('API: Text extracted, length:', text.length);
      } catch (error) {
        console.error('API: Error extracting text from file:', error);
        return NextResponse.json(
          { error: 'Unsupported file format. Please upload a PDF, DOCX, or TXT file.' },
          { status: 400 }
        );
      }
    }

    // Structure the extracted text
    const structuredText = structureResumeText(text);
    
    // Return the extracted text
    console.log('API: Returning extracted text successfully');
    return NextResponse.json({ 
      text: structuredText,
      original: text,
      message: 'Resume text extracted successfully.'
    });
  } catch (error) {
    console.error('API: Server error in extract-resume-text:', error);
    return NextResponse.json({
      error: 'Internal server error while processing the resume',
      details: error instanceof Error ? error.message : String(error)
    }, { status: 500 });
  }
}

/**
 * Clean and preprocess PDF text to improve structure and readability
 */
function cleanPdfText(text: string): string {
  let cleanedText = text;
  
  // Normalize newlines
  cleanedText = cleanedText.replace(/\r\n/g, '\n');
  
  // Preserve bullet points
  cleanedText = cleanedText.replace(/•\s*/g, '\n• ');
  cleanedText = cleanedText.replace(/\*\s*/g, '\n* ');
  cleanedText = cleanedText.replace(/[\-–]\s+/g, '\n- ');
  cleanedText = cleanedText.replace(/o\s+(?=[A-Z][a-z])/g, '\no '); // Detect "o" bullets
  
  // Fix common PDF extraction issues
  cleanedText = cleanedText
    // Fix lines split in the middle
    .replace(/([a-z])- ?([a-z])/g, '$1$2')
    
    // Remove excessive whitespace but preserve paragraph breaks
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    
    // Fix weird character encoding issues
    .replace(/[\u2022\u2023\u25E6\u2043\u2219]/g, '•')
    .replace(/[\u2013\u2014]/g, '-')
    
    // Fix spacing around headers (all caps words)
    .replace(/([^\n])((?:[A-Z][A-Z\s&]+){3,})/g, '$1\n\n$2')
    .replace(/((?:[A-Z][A-Z\s&]+){3,})([^\n])/g, '$1\n$2');
  
  // Identify section headers (common patterns in resumes)
  const sectionPatterns = [
    // ALL CAPS HEADERS
    /\n\s*([A-Z][A-Z\s&]+[A-Z])\s*(?:\n|\:|$)/g,
    
    // Title Case Headers with underlining
    /\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,})\n[\-=_]{3,}\n/g,
    
    // Headers with colons
    /\n\s*([A-Z][a-zA-Z\s]+):[^\n]*\n/g,
    
    // Numbered headers
    /\n\s*(\d+\.?\s+[A-Z][a-zA-Z\s]+)(?:\n|\:)/g,
  ];
  
  // Mark the identified section headers
  sectionPatterns.forEach(pattern => {
    cleanedText = cleanedText.replace(pattern, '\n\n$1\n');
  });
  
  // Make sure bullets are on their own lines 
  cleanedText = cleanedText.replace(/([^\n])([•\*\-])/g, '$1\n$2');
  
  // Make sure all bullet lines start with a bullet character
  cleanedText = cleanedText.replace(/\n\s*([A-Za-z])/g, (match, p1) => {
    // If line starts with lowercase, it might be a continuation
    if (p1.match(/[a-z]/)) {
      return match;
    }
    // If it's a sentence after a bullet, it's likely a new bullet
    if (p1.match(/[A-Z]/)) {
      return '\n• ' + p1;
    }
    return match;
  });
  
  return cleanedText.trim();
}

/**
 * Structure the resume text into sections
 */
function structureResumeText(text: string): string {
  // Identify common resume section headers
  const sectionHeaders = [
    'EDUCATION', 'EXPERIENCE', 'WORK EXPERIENCE', 'EMPLOYMENT',
    'PROFESSIONAL EXPERIENCE', 'PROFESSIONAL SUMMARY', 'CAREER EXPERIENCE',
    'SKILLS', 'TECHNICAL SKILLS', 'PROFICIENCIES', 'EXPERTISE',
    'PROJECTS', 'CERTIFICATIONS', 'ACHIEVEMENTS', 'AWARDS',
    'SUMMARY', 'PROFILE', 'OBJECTIVE', 'CAREER OBJECTIVE', 'PROFESSIONAL PROFILE',
    'PUBLICATIONS', 'LANGUAGES', 'INTERESTS', 'ACTIVITIES', 'VOLUNTEER',
    'REFERENCES', 'PROFESSIONAL DEVELOPMENT'
  ];
  
  // Add section markers
  let structured = text;
  
  // First, try to identify the contact info at the top
  const lines = structured.split('\n');
  
  if (lines.length > 2) {
    // Assume first line is the name
    structured = `<HEADER>${lines[0]}</HEADER>\n${lines.slice(1).join('\n')}`;
  }
  
  // Look for contact information patterns in the first few lines
  const contactPatterns = [
    /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/, // Email
    /\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b/, // Phone
    /linkedin\.com\/in\/[\w-]+/, // LinkedIn
    /github\.com\/[\w-]+/, // GitHub
    /\b(?:[A-Za-z]+,\s*[A-Za-z]+|[A-Za-z]+\s+[A-Za-z]+,\s*[A-Za-z]{2})\b/ // City, State
  ];
  
  // Mark contact info with tags
  let contactSection = '';
  for (let i = 1; i < Math.min(lines.length, 6); i++) {
    for (const pattern of contactPatterns) {
      if (pattern.test(lines[i])) {
        contactSection += lines[i] + '\n';
        break;
      }
    }
  }
  
  if (contactSection) {
    structured = structured.replace(contactSection, `<CONTACT_INFO>${contactSection}</CONTACT_INFO>`);
  }
  
  // Add section markers based on common header patterns
  sectionHeaders.forEach(header => {
    // Look for variations of the section header
    const patterns = [
      new RegExp(`\\b${header}\\b`, 'i'),
      new RegExp(`\\b${header}:`, 'i'),
      new RegExp(`\\n\\s*${header}\\s*\\n`, 'i')
    ];
    
    patterns.forEach(pattern => {
      structured = structured.replace(pattern, `\n\n<SECTION>${header.toUpperCase()}</SECTION>\n`);
    });
  });
  
  // Format bullet points
  structured = structured.replace(/^\s*[-•⋅∙⁃⦁●]|^\s*[*o]\s+/gm, '<BULLET> ');
  
  // Handle hyphens or dashes at the beginning of lines
  structured = structured.replace(/^\s*[-–—]\s+/gm, '<BULLET> ');
  
  // Try to identify experience items (dates followed by company names)
  const datePatterns = [
    /(\b\d{1,2}\/\d{4}\s*[-–—]\s*\d{1,2}\/\d{4}|\b\d{1,2}\/\d{4}\s*[-–—]\s*(?:Present|Current|Now))/gi,
    /(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–—]\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}/gi,
    /(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–—]\s*(?:Present|Current|Now)/gi,
    /\b\d{4}\s*[-–—]\s*\d{4}|\b\d{4}\s*[-–—]\s*(?:Present|Current|Now)/gi
  ];
  
  datePatterns.forEach(pattern => {
    structured = structured.replace(pattern, '\n<DATE>$1</DATE>');
  });
  
  // Ensure bullet points are on their own lines
  structured = structured.replace(/([.;:])\s*<BULLET>/g, '$1\n<BULLET>');
  
  // Clean up excess whitespace
  structured = structured.replace(/\n{3,}/g, '\n\n');
  
  return structured.trim();
} 
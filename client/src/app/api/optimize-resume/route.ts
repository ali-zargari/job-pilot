import { NextResponse } from 'next/server';
import axios from 'axios';
import pdfParse from 'pdf-parse';

// Ensure the API route is properly exported
export const dynamic = 'force-dynamic'; // No caching

export async function POST(request: Request) {
  console.log("API route called at", new Date().toISOString());
  
  try {
    // Parse the form data from the request
    const formData = await request.formData();
    const resumeFile = formData.get('resume') as File;
    const jobDescription = formData.get('job_description') as string || '';
    
    console.log("Form data received:", 
      resumeFile ? `File: ${resumeFile.name} (${resumeFile.type})` : "No file", 
      `Job description length: ${jobDescription?.length || 0}`
    );
    
    if (!resumeFile) {
      return NextResponse.json(
        { error: 'Resume file is required' },
        { status: 400 }
      );
    }
    
    // Extract text from the resume file
    let resumeText = '';
    try {
      // Handle different file types
      if (resumeFile.type === 'application/pdf') {
        try {
          // Convert File to ArrayBuffer
          const arrayBuffer = await resumeFile.arrayBuffer();
          const buffer = Buffer.from(arrayBuffer);
          
          // Parse PDF file
          console.log("Parsing PDF file...");
          const pdfData = await pdfParse(buffer);
          resumeText = pdfData.text;
          console.log("PDF parsed successfully, text length:", resumeText.length);
          
        } catch (pdfError) {
          console.error('Error parsing PDF:', pdfError);
          // Return mock data for testing
          console.log("Returning mock data due to PDF parsing error");
          return NextResponse.json({
            score: 75,
            issues: [
              "⚠️ PDF parsing error - returning mock data",
              "⚠️ Consider replacing weak verbs with stronger alternatives",
              "⚠️ Add more quantifiable achievements"
            ],
            optimized: "This is a mock optimized version of your resume.",
            original: "This is where your original resume would be shown.",
            draft: "This is a mock draft version."
          });
        }
      } else {
        // For other file types, get text directly
        console.log("Non-PDF file, getting text directly");
        resumeText = await resumeFile.text();
        console.log("File text extracted, length:", resumeText.length);
      }
      
      // Clean up the resume text
      const cleanedText = resumeText
        .replace(/\r\n/g, '\n')
        .replace(/\n\s*\n\s*\n/g, '\n\n')
        .trim();
      
      // Now actually call the backend API instead of local processing
      console.log("Calling Python backend API...");
      try {
        // Set the API URL based on the environment
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';
        console.log("Backend API URL:", apiUrl);
        
        // Create request payload
        const payload = {
          resume_text: cleanedText,
          job_description: jobDescription
        };
        console.log("Request payload size:", JSON.stringify(payload).length, "characters");
        
        // Make the API call to our Python backend
        console.log(`Making API request to ${apiUrl}/optimize...`);
        const response = await axios.post(`${apiUrl}/optimize`, payload, {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 60000 // 60 second timeout since AI processing might take time
        });
        
        console.log("Backend API responded successfully with status:", response.status);
        console.log("Response data keys:", Object.keys(response.data));
        
        // Return the backend response directly
        return NextResponse.json({
          ...response.data,
          optimized_with_ai: true  // Add this explicitly since we successfully used the AI
        });
      } catch (apiError: any) {
        console.error("Error calling backend API:", apiError.message);
        console.error("Full error:", apiError);
        
        if (apiError.code === 'ECONNREFUSED') {
          console.error("Connection refused. Is the Python backend running at the correct URL?");
        }
        
        // Fall back to local processing if backend is unreachable
        console.log("Falling back to local processing...");
        const draftText = enhanceResumeDraft(cleanedText, jobDescription);
        const optimizedText = enhanceResumeOptimized(cleanedText, jobDescription);
        
        return NextResponse.json({
          score: 82,
          issues: [
            "⚠️ AI backend unavailable - using local enhancements",
            "⚠️ Consider quantifying your achievements with specific numbers",
            "⚠️ Use more action verbs at the beginning of bullet points"
          ],
          optimized: optimizedText,
          original: cleanedText,
          draft: draftText,
          optimized_with_ai: false
        });
      }
      
    } catch (error) {
      console.error('Error reading resume file:', error);
      return NextResponse.json(
        { error: 'Could not read resume file. Please try again with a different file.' },
        { status: 400 }
      );
    }
  } catch (error) {
    console.error('Error in resume optimization API route:', error);
    return NextResponse.json(
      { error: 'Failed to optimize resume. Server error.' },
      { status: 500 }
    );
  }
}

// Function to create a draft enhancement of the resume
function enhanceResumeDraft(resumeText: string, jobDescription: string): string {
  // This is a simplified version that would normally use AI
  // Just doing some basic improvements for demonstration
  let enhancedText = resumeText
    .replace(/responsible for/gi, 'led')
    .replace(/helped with/gi, 'contributed to')
    .replace(/worked on/gi, 'developed')
    .replace(/in charge of/gi, 'managed')
    .replace(/assisted in/gi, 'supported');
    
  // Capitalize sentences
  enhancedText = capitalizeSentences(enhancedText);
  
  return enhancedText;
}

// Function to create an optimized version of the resume
function enhanceResumeOptimized(resumeText: string, jobDescription: string): string {
  // In a real implementation, this would use more advanced techniques
  // and would consider the job description
  let enhancedText = resumeText
    .replace(/responsible for/gi, 'led')
    .replace(/helped with/gi, 'collaborated on')
    .replace(/worked on/gi, 'engineered')
    .replace(/in charge of/gi, 'directed')
    .replace(/assisted in/gi, 'facilitated')
    .replace(/developed/gi, 'architected and implemented')
    .replace(/created/gi, 'designed and delivered')
    .replace(/managed/gi, 'orchestrated')
    .replace(/improved/gi, 'optimized');
    
  // Add a tailored skills section if it doesn't exist
  if (!enhancedText.includes("SKILLS") && jobDescription) {
    const relevantSkills = extractRelevantSkills(resumeText, jobDescription);
    if (relevantSkills.length > 0) {
      enhancedText += "\n\nSKILLS\n" + relevantSkills.join(", ");
    }
  }
  
  // Capitalize sentences
  enhancedText = capitalizeSentences(enhancedText);
  
  return enhancedText;
}

// Function to extract relevant skills from resume text and job description
function extractRelevantSkills(resumeText: string, jobDescription: string): string[] {
  // This would normally use NLP to match skills between resume and job description
  // Using a simple approach for demonstration
  const commonTechnicalSkills = [
    "JavaScript", "TypeScript", "React", "Node.js", "Python", "SQL", "AWS", 
    "Docker", "Kubernetes", "CI/CD", "Git", "REST API", "GraphQL",
    "Machine Learning", "Data Analysis", "Java", "C++", "C#"
  ];
  
  const skills: string[] = [];
  
  // Check which skills are mentioned in both resume and job description
  commonTechnicalSkills.forEach(skill => {
    if (resumeText.includes(skill) && jobDescription.includes(skill)) {
      skills.push(skill);
    } else if (resumeText.includes(skill)) {
      // Add skills from resume even if not in job description
      skills.push(skill);
    }
  });
  
  return skills;
}

// Function to properly capitalize sentences in resume text
function capitalizeSentences(text: string): string {
  // Split into lines
  const lines = text.split('\n');
  const capitalizedLines = lines.map(line => {
    if (!line.trim()) return line;
    
    // Split the line into parts based on bullet points/markers
    const parts = line.split(/^(\s*[-•*]\s*)/);
    if (parts.length > 1) {
      // If line starts with a bullet point
      const bullet = parts[1];
      const content = parts.slice(2).join('');
      
      if (content && content.length > 0) {
        // Capitalize the first letter after the bullet
        return bullet + content.charAt(0).toUpperCase() + content.slice(1);
      }
    }
    
    // For non-bullet lines, capitalize the first character if it's a letter
    if (/^[a-z]/i.test(line)) {
      return line.charAt(0).toUpperCase() + line.slice(1);
    }
    
    return line;
  });
  
  return capitalizedLines.join('\n');
} 
'use client';

import { useState, useRef } from 'react';
import Link from 'next/link';
import { useResumeStore } from '@/app/store/resumeStore';

export default function OptimizePage() {
  const [step, setStep] = useState(1);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const { 
    file, 
    jobDescription, 
    isLoading, 
    result, 
    setFile, 
    setJobDescription, 
    startOptimization, 
    setResult, 
    setError 
  } = useResumeStore();
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };
  
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };
  
  const handleJobDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setJobDescription(e.target.value);
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) return;
    
    startOptimization();
    
    try {
      // Create form data for file upload
      const formData = new FormData();
      formData.append('resume', file);
      formData.append('job_description', jobDescription);
      
      // For API call implementation:
      // const response = await fetch('/api/optimize-resume', {
      //   method: 'POST',
      //   body: formData,
      // });
      // 
      // if (!response.ok) {
      //   throw new Error('Failed to optimize resume');
      // }
      // 
      // const data = await response.json();
      // setResult(data);
      
      // Simulate API response
      setTimeout(() => {
        // Mock response data
        setResult({
          score: 85,
          issues: [
            "⚠️ Consider rewriting: 'The project was completed by me' (Passive voice detected)",
            "⚠️ Replace 'responsible for' in bullet points (Use action verbs)",
            "⚠️ Consider adding quantifiable achievements (Use numbers)"
          ],
          optimized: `# John Doe
**Software Engineer | john.doe@example.com | (555) 123-4567**

## Professional Experience

### Senior Software Engineer | ABC Tech | 2020 - Present
* Led development of cloud infrastructure, reducing deployment time by 40%
* Improved system reliability by implementing automated testing, decreasing bugs by 25%
* Spearheaded adoption of DevOps practices, resulting in 30% faster release cycles

### Software Developer | XYZ Solutions | 2018 - 2020
* Developed e-commerce platform handling $2M in annual transactions
* Optimized database queries, reducing load times by 50%
* Mentored 5 junior developers, improving team productivity by 15%`,
          original: `# John Doe
**Software Engineer | john.doe@example.com | (555) 123-4567**

## Professional Experience

### Senior Software Engineer | ABC Tech | 2020 - Present
* Was responsible for development of cloud infrastructure
* The project was completed by me
* Helped with adoption of DevOps practices

### Software Developer | XYZ Solutions | 2018 - 2020
* Worked on e-commerce platform
* In charge of database optimization
* Assisted in mentoring junior developers`
        });
        
        setStep(3);
      }, 2000);
      
    } catch (error) {
      console.error('Error optimizing resume:', error);
      setError('Failed to optimize resume. Please try again.');
    }
  };
  
  const renderStepContent = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Upload Your Resume</h2>
            
            <div 
              className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:border-indigo-500 transition-colors"
              onClick={handleUploadClick}
            >
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept=".pdf,.doc,.docx,.txt"
                className="hidden"
              />
              
              {file ? (
                <div>
                  <div className="text-sm text-gray-500 mb-1">Selected file:</div>
                  <div className="text-lg font-medium text-indigo-600">{file.name}</div>
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      setFile(null);
                    }}
                    className="mt-2 text-sm text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <div>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <p className="mt-4 text-sm text-gray-500">
                    Drag and drop your resume here, or <span className="text-indigo-600 font-medium">browse files</span>
                  </p>
                  <p className="mt-1 text-xs text-gray-400">
                    Supported formats: PDF, DOC, DOCX, TXT
                  </p>
                </div>
              )}
            </div>
            
            <div className="flex justify-end">
              <button
                onClick={() => file && setStep(2)}
                disabled={!file}
                className={`px-6 py-3 rounded-lg font-medium ${
                  file 
                    ? 'bg-indigo-600 text-white hover:bg-indigo-700' 
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                Continue
              </button>
            </div>
          </div>
        );
        
      case 2:
        return (
          <form onSubmit={handleSubmit} className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Add Job Description</h2>
            <p className="text-gray-600">
              For better optimization, paste the job description you're applying for. This helps our AI tailor your resume to the specific role.
            </p>
            
            <div>
              <label htmlFor="job-description" className="block text-sm font-medium text-gray-700 mb-1">
                Job Description (Optional)
              </label>
              <textarea
                id="job-description"
                value={jobDescription}
                onChange={handleJobDescriptionChange}
                placeholder="Paste the job description here..."
                className="w-full h-64 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            
            <div className="flex justify-between">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="px-6 py-3 rounded-lg font-medium text-gray-700 border border-gray-300 hover:bg-gray-50"
              >
                Back
              </button>
              
              <button
                type="submit"
                className="px-6 py-3 rounded-lg font-medium bg-indigo-600 text-white hover:bg-indigo-700"
              >
                Optimize Resume
              </button>
            </div>
          </form>
        );
        
      case 3:
        return (
          <div className="space-y-8">
            <h2 className="text-2xl font-bold text-gray-900">Optimization Results</h2>
            
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="p-6 bg-indigo-50 border-b border-indigo-100">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">Resume Score</h3>
                  <div className="flex items-center">
                    <div className="text-2xl font-bold text-indigo-600">{result?.score}/100</div>
                    <svg className="w-6 h-6 ml-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <div className="p-6 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Improvement Areas</h3>
                <ul className="space-y-2">
                  {result?.issues.map((issue: string, index: number) => (
                    <li key={index} className="text-gray-700">{issue}</li>
                  ))}
                </ul>
              </div>
              
              <div className="p-6 border-b border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Original Resume</h3>
                    <div className="bg-gray-50 p-4 rounded-lg prose max-w-none text-sm">
                      <pre className="whitespace-pre-wrap">{result?.original}</pre>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Optimized Resume</h3>
                    <div className="bg-blue-50 p-4 rounded-lg prose max-w-none text-sm">
                      <pre className="whitespace-pre-wrap">{result?.optimized}</pre>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="p-6 bg-gray-50">
                <div className="flex justify-between">
                  <button
                    onClick={() => setStep(1)}
                    className="px-5 py-2 rounded-lg font-medium text-gray-700 border border-gray-300 hover:bg-gray-100"
                  >
                    Upload Another Resume
                  </button>
                  
                  <button
                    className="px-5 py-2 rounded-lg font-medium bg-indigo-600 text-white hover:bg-indigo-700"
                  >
                    Download Optimized Resume
                  </button>
                </div>
              </div>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-10 text-center">
          <Link href="/" className="inline-block mb-6">
            <span className="text-2xl font-bold text-indigo-600">ResumePilot</span>
          </Link>
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            {isLoading ? 'Optimizing Your Resume...' : 'Resume Optimizer'}
          </h1>
          <p className="mt-2 text-lg text-gray-600">
            {isLoading 
              ? 'Our AI is analyzing your resume to make it shine.' 
              : 'Upload your resume and let our AI make it stand out.'}
          </p>
        </div>
        
        {/* Step Indicator */}
        {!isLoading && (
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step >= 1 ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-500'
                }`}>
                  1
                </div>
                <div className={`h-1 w-12 sm:w-24 ${
                  step >= 2 ? 'bg-indigo-600' : 'bg-gray-200'
                }`}></div>
              </div>
              
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step >= 2 ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-500'
                }`}>
                  2
                </div>
                <div className={`h-1 w-12 sm:w-24 ${
                  step >= 3 ? 'bg-indigo-600' : 'bg-gray-200'
                }`}></div>
              </div>
              
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                step >= 3 ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-500'
              }`}>
                3
              </div>
            </div>
            
            <div className="flex justify-between mt-2 text-sm text-gray-500">
              <span>Upload Resume</span>
              <span>Job Description</span>
              <span>Results</span>
            </div>
          </div>
        )}
        
        {/* Main Content */}
        <div className="bg-white rounded-xl shadow-sm p-6 sm:p-8">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12">
              <div className="w-16 h-16 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <p className="mt-4 text-lg font-medium text-gray-700">Processing your resume...</p>
              <p className="mt-2 text-sm text-gray-500">This might take a minute.</p>
            </div>
          ) : (
            renderStepContent()
          )}
        </div>
      </div>
    </div>
  );
} 
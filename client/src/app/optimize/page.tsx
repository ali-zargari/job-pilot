'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useResumeStore } from '@/app/store/resumeStore';
import { useDropzone } from 'react-dropzone';
import { ArrowUpTrayIcon, DocumentTextIcon, ArrowPathIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Progress } from '@/components/ui/Progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import axios from 'axios';

export default function OptimizePage() {
  const [step, setStep] = useState(1);
  const { 
    file, 
    jobDescription, 
    isLoading, 
    result, 
    currentView,
    setFile, 
    setJobDescription, 
    startOptimization, 
    setResult, 
    setError,
    setCurrentView
  } = useResumeStore();
  
  // Reset state when navigating away
  useEffect(() => {
    return () => {
      // Cleanup function that runs when component unmounts
      setFile(null);
      setJobDescription('');
    };
  }, [setFile, setJobDescription]);
  
  // File Dropzone
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1,
    onDrop: acceptedFiles => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
      }
    }
  });
  
  const handleJobDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setJobDescription(e.target.value);
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) return;
    
    startOptimization();
    
    try {
      console.log("Submitting resume:", file.name);
      
      // Create form data for file upload
      const formData = new FormData();
      formData.append('resume', file);
      formData.append('job_description', jobDescription);
      
      // Make API call
      console.log("Sending request to /api/optimize-resume");
      const response = await axios.post('/api/optimize-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log("Response received:", response.status);
      
      if (response.status !== 200) {
        throw new Error(`Failed to optimize resume: ${response.status}`);
      }
      
      // Set result data
      console.log("Setting result data");
      setResult(response.data);
      setStep(3);
    } catch (error: any) {
      console.error('Error optimizing resume:', error);
      setError(error.message || 'Failed to optimize resume. Please try again.');
    }
  };
  
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
  };
  
  const renderStepContent = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Optimize Your Resume</h1>
              <p className="text-gray-500 max-w-2xl mx-auto">
                Upload your resume and we'll help you improve it with our AI-powered optimization system.
              </p>
            </div>
            
            <Card>
              <CardHeader>
                <CardTitle>Upload Your Resume</CardTitle>
                <CardDescription>
                  We support PDF, DOC, DOCX, and TXT formats
                </CardDescription>
              </CardHeader>
              <CardContent>
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
                    </div>
                  ) : (
                    <div>
                      <div className="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center mx-auto">
                        <ArrowUpTrayIcon className="h-8 w-8 text-gray-400" />
                      </div>
                      <p className="mt-4 text-gray-500">
                        Drag and drop your resume here, or <span className="text-primary-600 font-medium">browse files</span>
                      </p>
                      <p className="mt-1 text-xs text-gray-400">
                        Supported formats: PDF, DOC, DOCX, TXT
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
              <CardFooter className="flex justify-end">
                <Button
                  onClick={() => file && setStep(2)}
                  disabled={!file}
                >
                  Continue
                </Button>
              </CardFooter>
            </Card>
          </div>
        );
        
      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Add Job Description</h1>
              <p className="text-gray-500 max-w-2xl mx-auto">
                For better optimization, paste the job description you're applying for. This helps our AI tailor your resume.
              </p>
            </div>
            
            <Card>
              <form onSubmit={handleSubmit}>
                <CardHeader>
                  <CardTitle>Job Description</CardTitle>
                  <CardDescription>
                    Paste the job description to help us tailor your resume (optional but recommended)
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <textarea
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                    placeholder="Paste the job description here..."
                    className="w-full h-64 p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setStep(1)}
                  >
                    Back
                  </Button>
                  
                  <Button
                    type="submit"
                  >
                    {isLoading ? (
                      <>
                        <ArrowPathIcon className="h-4 w-4 mr-2 animate-spin" />
                        Processing with AI...
                      </>
                    ) : (
                      'Optimize Resume'
                    )}
                  </Button>
                </CardFooter>
              </form>
            </Card>
          </div>
        );
        
      case 3:
        return (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Optimization Results</h1>
              <p className="text-gray-500 max-w-2xl mx-auto">
                Here's your optimized resume with improvements suggested by our AI.
              </p>
            </div>
            
            {result && (
              <>
                <Card>
                  <CardHeader className="bg-primary-50">
                    <div className="flex items-center justify-between">
                      <CardTitle>Resume Score</CardTitle>
                      <div className="flex items-center gap-2">
                        <Badge variant={getScoreColor(result.score)}>
                          {result.score}/100
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="pt-6">
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium">Overall Score</span>
                          <span className="text-sm font-medium">{result.score}%</span>
                        </div>
                        <Progress value={result.score} variant={getScoreColor(result.score)} showValue />
                      </div>
                      
                      <div className="border-t border-gray-100 pt-4 mt-6">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Resume Analysis</h3>
                        {result.lint_results?.issues ? (
                          <>
                            {/* Positive feedback section */}
                            <div className="mb-6">
                              <h4 className="text-md font-medium text-gray-700 mb-3">Strengths</h4>
                              <ul className="space-y-3">
                                {result.lint_results.issues
                                  .filter(issue => issue.severity === 'positive')
                                  .map((issue, index) => (
                                    <li key={index} className="flex flex-col bg-green-50 p-3 rounded-lg border border-green-100">
                                      <div className="flex items-start">
                                        <span className="inline-flex items-center justify-center flex-shrink-0 w-5 h-5 mr-2 text-green-500">
                                          <CheckCircleIcon className="w-5 h-5" />
                                        </span>
                                        <span className="text-green-700">
                                          {issue.message.includes("Examples:") 
                                            ? issue.message.split("Examples:")[0] + "Examples:"
                                            : issue.message}
                                        </span>
                                      </div>
                                      
                                      {issue.message.includes("Examples:") && (
                                        <div className="mt-2 ml-7 bg-green-100 p-2 rounded">
                                          <ul className="list-disc pl-5 text-sm text-green-700">
                                            {issue.message
                                              .split("Examples:")[1]
                                              .split(";")
                                              .filter(ex => ex.trim().length > 0)
                                              .map((example, i) => (
                                                <li key={i}>{example.replace("This helps demonstrate your impact.", "").trim()}</li>
                                              ))}
                                          </ul>
                                        </div>
                                      )}
                                    </li>
                                  ))}
                                {result.lint_results.issues.filter(issue => issue.severity === 'positive').length === 0 && (
                                  <li className="text-gray-500 italic p-3">No strengths identified. Let's improve your resume!</li>
                                )}
                              </ul>
                            </div>

                            {/* Improvement suggestions section */}
                            <div>
                              <h4 className="text-md font-medium text-gray-700 mb-3">Areas to Improve</h4>
                              <ul className="space-y-3">
                                {result.lint_results.issues
                                  .filter(issue => issue.severity !== 'positive')
                                  .map((issue, index) => (
                                    <li key={index} className="flex items-start bg-red-50 p-3 rounded-lg border border-red-100">
                                      <span className="inline-flex items-center justify-center flex-shrink-0 w-5 h-5 mr-2 text-red-500">
                                        <XCircleIcon className="w-5 h-5" />
                                      </span>
                                      <span className="text-red-700">{issue.message}</span>
                                    </li>
                                  ))}
                                {result.lint_results.issues.filter(issue => issue.severity !== 'positive').length === 0 && (
                                  <li className="text-gray-700 p-3 bg-gray-50 rounded-lg border border-gray-100">
                                    No issues found. Your resume looks great!
                                  </li>
                                )}
                              </ul>
                            </div>
                          </>
                        ) : result.issues?.length ? (
                          // Old API format with direct issues array
                          <ul className="space-y-3">
                            {result.issues.map((issue: string, index: number) => (
                              <li key={index} className="flex items-start bg-gray-50 p-3 rounded-lg">
                                {issue.startsWith('✅') ? (
                                  <span className="inline-flex items-center justify-center flex-shrink-0 w-5 h-5 mr-2 text-green-500">
                                    <CheckCircleIcon className="w-5 h-5" />
                                  </span>
                                ) : (
                                  <span className="inline-flex items-center justify-center flex-shrink-0 w-5 h-5 mr-2 text-red-500">
                                    <XCircleIcon className="w-5 h-5" />
                                  </span>
                                )}
                                <span className={issue.startsWith('✅') ? 'text-green-700' : 'text-red-700'}>
                                  {issue.replace(/^(✅|❌|⚠️)\s*/, '')}
                                </span>
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <div className="rounded-lg bg-gray-50 p-4 border border-gray-200">
                            <p className="text-gray-500 text-center">No analysis available. Try uploading a different resume.</p>
                          </div>
                        )}
                      </div>
                      
                      {/* Rule-based suggestions section */}
                      {result.suggestions && (
                        <div className="border-t border-gray-100 pt-4 mt-6">
                          <h3 className="text-lg font-semibold text-gray-900 mb-4">Rule-Based Suggestions</h3>
                          
                          {result.suggestions.weak_verbs.length > 0 && (
                            <div className="mb-6 rounded-lg bg-orange-50 p-4 border border-orange-200">
                              <div className="flex items-center mb-3">
                                <span className="inline-block w-8 h-8 rounded-full bg-orange-100 mr-2 flex items-center justify-center">
                                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 text-orange-500">
                                    <path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z" />
                                  </svg>
                                </span>
                                <h4 className="text-md font-medium text-orange-700">Weak Verbs to Replace</h4>
                              </div>
                              <ul className="space-y-2 ml-10">
                                {result.suggestions.weak_verbs.map((suggestion, index) => {
                                  // Extract the verb to replace and context
                                  const verbMatch = suggestion.match(/Replace '([^']+)' with '([^']+)' in context: '([^']+)'/);
                                  if (verbMatch) {
                                    const [_, weakVerb, strongVerb, context] = verbMatch;
                                    return (
                                      <li key={index} className="text-orange-700 text-sm">
                                        <div className="flex flex-col">
                                          <span>
                                            Replace <span className="font-bold text-red-600">{weakVerb}</span> with <span className="font-bold text-green-600">{strongVerb}</span>
                                          </span>
                                          <span className="mt-1 pl-2 border-l-2 border-orange-300 italic bg-orange-100/50 p-1 rounded">
                                            {context}
                                          </span>
                                        </div>
                                      </li>
                                    );
                                  }
                                  return (
                                    <li key={index} className="text-orange-700 text-sm">
                                      {suggestion}
                                    </li>
                                  );
                                })}
                              </ul>
                            </div>
                          )}
                          
                          {result.suggestions.formatting_issues.length > 0 && (
                            <div className="mb-6 rounded-lg bg-blue-50 p-4 border border-blue-200">
                              <div className="flex items-center mb-3">
                                <span className="inline-block w-8 h-8 rounded-full bg-blue-100 mr-2 flex items-center justify-center">
                                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 text-blue-500">
                                    <path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z" />
                                  </svg>
                                </span>
                                <h4 className="text-md font-medium text-blue-700">Formatting Issues</h4>
                              </div>
                              <ul className="space-y-2 ml-10">
                                {result.suggestions.formatting_issues.map((suggestion, index) => (
                                  <li key={index} className="text-blue-700 text-sm">
                                    {suggestion}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                          
                          {result.suggestions.content_improvements.length > 0 && (
                            <div className="mb-6 rounded-lg bg-green-50 p-4 border border-green-200">
                              <div className="flex items-center mb-3">
                                <span className="inline-block w-8 h-8 rounded-full bg-green-100 mr-2 flex items-center justify-center">
                                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 text-green-500">
                                    <path d="M11.625 16.5a1.875 1.875 0 100-3.75 1.875 1.875 0 000 3.75z" />
                                    <path fillRule="evenodd" d="M5.625 1.5H9a3.75 3.75 0 013.75 3.75v1.875c0 1.036.84 1.875 1.875 1.875H16.5a3.75 3.75 0 013.75 3.75v7.875c0 1.035-.84 1.875-1.875 1.875H5.625a1.875 1.875 0 01-1.875-1.875V3.375c0-1.036.84-1.875 1.875-1.875zm6 16.5c.66 0 1.277-.19 1.797-.518l1.048 1.048a.75.75 0 001.06-1.06l-1.047-1.048A3.375 3.375 0 1011.625 18z" clipRule="evenodd" />
                                    <path d="M14.25 5.25a5.23 5.23 0 00-1.279-3.434 9.768 9.768 0 016.963 6.963A5.23 5.23 0 0016.5 7.5h-1.875a.375.375 0 01-.375-.375V5.25z" />
                                  </svg>
                                </span>
                                <h4 className="text-md font-medium text-green-700">Content Improvements</h4>
                              </div>
                              <ul className="space-y-2 ml-10">
                                {result.suggestions.content_improvements.map((suggestion, index) => {
                                  // Try to extract the content to improve
                                  const contentMatch = suggestion.match(/(Add quantifiable metrics to|Expand on this point to be more descriptive): '([^']+)'/);
                                  if (contentMatch) {
                                    const [_, action, context] = contentMatch;
                                    return (
                                      <li key={index} className="text-green-700 text-sm">
                                        <div className="flex flex-col">
                                          <span className="font-semibold">{action}</span>
                                          <span className="mt-1 pl-2 border-l-2 border-green-300 italic bg-green-100/50 p-1 rounded">
                                            {context}
                                          </span>
                                        </div>
                                      </li>
                                    );
                                  }
                                  return (
                                    <li key={index} className="text-green-700 text-sm">
                                      {suggestion}
                                    </li>
                                  );
                                })}
                              </ul>
                            </div>
                          )}
                          
                          {result.suggestions.weak_verbs.length === 0 && 
                           result.suggestions.formatting_issues.length === 0 && 
                           result.suggestions.content_improvements.length === 0 && (
                            <div className="rounded-lg bg-gray-50 p-4 border border-gray-200">
                              <p className="text-gray-500 text-center">No rule-based suggestions found. Your resume is already well-optimized!</p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader>
                    <CardTitle>Resume Versions</CardTitle>
                    <CardDescription>
                      Compare your original resume with the AI-improved version
                      {result?.optimized_with_ai === false && (
                        <Badge className="ml-2 bg-yellow-500">Rule-based mode</Badge>
                      )}
                      {result?.optimized_with_ai === true && (
                        <Badge className="ml-2 bg-green-500">AI-enhanced</Badge>
                      )}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Tabs defaultValue="optimized" className="w-full" onValueChange={(value) => setCurrentView(value as any)}>
                      <TabsList className="mb-4">
                        <TabsTrigger value="original">Original</TabsTrigger>
                        {result.draft && (
                          <TabsTrigger value="draft">Initial Draft</TabsTrigger>
                        )}
                        <TabsTrigger value="optimized">Final Version</TabsTrigger>
                      </TabsList>
                      
                      <TabsContent value="original" className="space-y-4">
                        <div className="bg-gray-50 p-6 rounded-lg prose max-w-none">
                          <pre className="whitespace-pre-wrap">{result.original}</pre>
                        </div>
                      </TabsContent>
                      
                      {result.draft && (
                        <TabsContent value="draft" className="space-y-4">
                          <div className="bg-gray-50 p-6 rounded-lg prose max-w-none">
                            <pre className="whitespace-pre-wrap">{result.draft}</pre>
                          </div>
                        </TabsContent>
                      )}
                      
                      <TabsContent value="optimized" className="space-y-4">
                        <div className="bg-gray-50 p-6 rounded-lg prose max-w-none">
                          <pre className="whitespace-pre-wrap">{result.optimized}</pre>
                        </div>
                      </TabsContent>
                    </Tabs>
                  </CardContent>
                  <CardFooter className="flex justify-between">
                    <Button
                      variant="outline"
                      onClick={() => {
                        setFile(null);
                        setJobDescription('');
                        setStep(1);
                      }}
                    >
                      Start Over
                    </Button>
                    
                    <div className="flex gap-2">
                      <Button
                        onClick={() => {
                          if (!result || !currentView || !result[currentView]) return;
                          
                          const element = document.createElement('a');
                          const content = String(result[currentView] || '');
                          const file = new Blob([content], { type: 'text/plain' });
                          element.href = URL.createObjectURL(file);
                          element.download = `resume-${currentView}.txt`;
                          document.body.appendChild(element);
                          element.click();
                          document.body.removeChild(element);
                        }}
                      >
                        Download {(currentView || 'optimized').charAt(0).toUpperCase() + (currentView || 'optimized').slice(1)} Version
                      </Button>
                    </div>
                  </CardFooter>
                </Card>
              </>
            )}
          </div>
        );
        
      default:
        return null;
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {renderStepContent()}
    </div>
  );
} 
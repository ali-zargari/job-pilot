'use client';

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { DocumentTextIcon } from '@heroicons/react/24/outline';

export default function TestPdfPage() {
  const [file, setFile] = useState<File | null>(null);
  const [extractedText, setExtractedText] = useState<string>('');
  const [apiResponse, setApiResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    maxFiles: 1,
    accept: {
      'application/pdf': ['.pdf'],
    },
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        console.log('File dropped:', acceptedFiles[0].name, 'Type:', acceptedFiles[0].type);
        setFile(acceptedFiles[0]);
        setExtractedText('');
        setApiResponse(null);
        setError(null);
      }
    }
  });

  const handleExtractText = async () => {
    if (!file) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // Create form data for file upload
      const formData = new FormData();
      formData.append('resume', file);
      console.log('Sending file to API...');
      
      // Extract text via API
      const response = await axios.post('/api/extract-resume-text', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log('API response:', response.status, response.data);
      setApiResponse(response.data);
      
      if (response.status === 200 && response.data.text) {
        setExtractedText(response.data.text);
      } else {
        setError('API response did not contain text');
      }
    } catch (error: any) {
      console.error('Error extracting text:', error);
      setError(`Error: ${error.message || 'Unknown error occurred'}`);
      
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        setApiResponse(error.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">PDF Parser Test Page</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Upload PDF for Testing</CardTitle>
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
                </div>
              ) : (
                <div className="space-y-2">
                  <DocumentTextIcon className="h-12 w-12 mx-auto text-gray-400" />
                  <p className="text-gray-500">
                    Drag and drop your PDF file here, or click to browse
                  </p>
                  <p className="text-xs text-gray-400">
                    PDF files only
                  </p>
                </div>
              )}
            </div>
          </CardContent>
          
          <CardFooter>
            <Button 
              onClick={handleExtractText} 
              disabled={!file || loading}
              className="w-full"
            >
              {loading ? 'Processing...' : 'Extract Text from PDF'}
            </Button>
          </CardFooter>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Extracted Text</CardTitle>
          </CardHeader>
          
          <CardContent className="max-h-[600px] overflow-auto">
            {error && (
              <div className="p-4 mb-4 bg-danger-50 text-danger-700 rounded-md">
                {error}
              </div>
            )}
            
            {apiResponse && (
              <div className="mb-4">
                <h3 className="text-sm font-medium mb-2">API Response:</h3>
                <pre className="bg-gray-100 p-3 rounded text-xs overflow-auto max-h-[200px]">
                  {JSON.stringify(apiResponse, null, 2)}
                </pre>
              </div>
            )}
            
            {extractedText ? (
              <pre className="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-4 rounded">
                {extractedText}
              </pre>
            ) : !loading && !error ? (
              <div className="text-center text-gray-500 my-8">
                Upload a PDF file and click "Extract Text" to see the results
              </div>
            ) : null}
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 
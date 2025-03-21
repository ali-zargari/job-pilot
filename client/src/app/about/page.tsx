import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-indigo-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Link href="/" className="inline-block mb-4">
            <span className="text-2xl font-bold text-white">ResumePilot</span>
          </Link>
          <h1 className="text-4xl font-extrabold text-white sm:text-5xl sm:tracking-tight">
            How Our Resume Optimization Works
          </h1>
          <p className="mt-5 max-w-3xl mx-auto text-xl text-indigo-100">
            The science and AI behind creating perfect resumes that get you interviews.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
        <div className="prose prose-lg prose-indigo mx-auto">
          <h2>Our 4-Step Resume Optimization Process</h2>
          
          <p>
            Our system uses a hybrid approach that combines rule-based analysis with advanced AI to 
            create resumes that are both ATS-friendly and appealing to human recruiters.
          </p>

          <div className="my-12 border rounded-xl overflow-hidden shadow-sm">
            <div className="bg-white px-6 py-8">
              <h3 className="text-2xl font-bold text-gray-900 flex items-center">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 mr-4">1</span>
                Rule-Based Resume Preprocessing
              </h3>
              <p className="mt-4 text-gray-600">
                Before AI touches your resume, we apply hard-coded rules to:
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Detect weak resume points (passive voice, missing achievements, weak phrasing)</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Flag non-ATS-friendly elements (tables, images, complex formatting)</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Ensure action verbs & impact-driven bullet points are used</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="my-12 border rounded-xl overflow-hidden shadow-sm">
            <div className="bg-white px-6 py-8">
              <h3 className="text-2xl font-bold text-gray-900 flex items-center">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 mr-4">2</span>
                Fine-Tuned AI Model
              </h3>
              <p className="mt-4 text-gray-600">
                We've fine-tuned a specialized transformer model on thousands of before-and-after resume improvements:
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Trained on T5 or LLama model framework with resume-specific knowledge</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Ensures AI follows strict resume writing best practices</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Prevents generation of generic or robotic-sounding content</span>
                </li>
              </ul>

              <div className="mt-6 bg-gray-50 p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900">Example Transformation:</h4>
                <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Before:</p>
                    <p className="text-sm bg-white p-3 rounded border border-gray-200">
                      "Responsible for managing social media accounts."
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 mb-1">After:</p>
                    <p className="text-sm bg-indigo-50 p-3 rounded border border-indigo-200">
                      "Increased engagement by 40% in 3 months through targeted social media campaigns."
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="my-12 border rounded-xl overflow-hidden shadow-sm">
            <div className="bg-white px-6 py-8">
              <h3 className="text-2xl font-bold text-gray-900 flex items-center">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 mr-4">3</span>
                Job-Resume Matching
              </h3>
              <p className="mt-4 text-gray-600">
                Our system uses embeddings to match your resume to the job description:
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Converts resumes & job descriptions into vector embeddings</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Compares against high-performing job applications</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Recommends proven bullet points instead of randomly generating text</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="my-12 border rounded-xl overflow-hidden shadow-sm">
            <div className="bg-white px-6 py-8">
              <h3 className="text-2xl font-bold text-gray-900 flex items-center">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 mr-4">4</span>
                Final AI Polish
              </h3>
              <p className="mt-4 text-gray-600">
                After strict, rule-based optimization, we use GPT-4 to add a final layer of polish:
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Ensures resume sounds natural & human-like</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Fixes grammar & readability issues</span>
                </li>
                <li className="flex items-start">
                  <svg className="h-5 w-5 text-green-500 mr-2 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Only refines what's already high-quality—doesn't rewrite randomly</span>
                </li>
              </ul>
            </div>
          </div>

          <h2>Why Our Approach Is Better</h2>
          <p>
            Unlike generic AI tools that randomly generate content, our hybrid approach ensures:
          </p>
          <ul>
            <li><strong>Factual Accuracy</strong> - We don't invent achievements or experience</li>
            <li><strong>ATS Compatibility</strong> - Optimized for Applicant Tracking Systems</li>
            <li><strong>Human Appeal</strong> - Resumes that impress both algorithms and recruiters</li>
            <li><strong>Industry-Specific</strong> - Tailored optimization for your career field</li>
          </ul>

          <div className="mt-12 text-center">
            <Link 
              href="/optimize" 
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Try It Now
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
} 
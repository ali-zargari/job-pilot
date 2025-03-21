import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative w-full bg-gradient-to-r from-indigo-600 to-purple-600 py-20 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:20px_20px]" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
        <div className="relative max-w-5xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Your Resume, <span className="text-yellow-300">Perfected by AI</span>
          </h1>
          <p className="text-xl text-white/90 mb-10 max-w-3xl mx-auto">
            Unlock better job opportunities with our AI-powered resume optimization system. 
            Get more interviews with a resume that stands out.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/optimize"
              className="bg-white text-indigo-600 hover:bg-white/90 font-semibold px-6 py-3 rounded-lg shadow-lg transition-all transform hover:scale-105"
            >
              Optimize My Resume
            </Link>
            <Link 
              href="/about"
              className="bg-transparent border-2 border-white text-white hover:bg-white/10 font-semibold px-6 py-3 rounded-lg transition-all"
            >
              Learn How It Works
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">How Our System Optimizes Your Resume</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-gray-50 p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Rule-Based Analysis</h3>
              <p className="text-gray-600">
                Our system first analyzes your resume for common issues like passive voice, weak phrases, and ATS compatibility.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-gray-50 p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Enhancement</h3>
              <p className="text-gray-600">
                Our fine-tuned model transforms your resume with powerful action verbs and quantifiable achievements.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-gray-50 p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Job Matching</h3>
              <p className="text-gray-600">
                We use advanced embedding technology to align your resume with your target job descriptions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Success Stories</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Testimonial 1 */}
            <div className="bg-white p-8 rounded-xl shadow-sm">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gray-200 rounded-full overflow-hidden">
                  <div className="w-full h-full bg-indigo-100 flex items-center justify-center">
                    <span className="text-indigo-600 font-bold">JD</span>
                  </div>
                </div>
                <div className="ml-4">
                  <h4 className="text-lg font-semibold">John Doe</h4>
                  <p className="text-gray-500">Software Engineer</p>
                </div>
              </div>
              <p className="text-gray-600 italic">
                "After optimizing my resume, I received 3x more interview calls. The AI made my achievements sound more impactful without exaggerating."
              </p>
            </div>

            {/* Testimonial 2 */}
            <div className="bg-white p-8 rounded-xl shadow-sm">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gray-200 rounded-full overflow-hidden">
                  <div className="w-full h-full bg-indigo-100 flex items-center justify-center">
                    <span className="text-indigo-600 font-bold">AS</span>
                  </div>
                </div>
                <div className="ml-4">
                  <h4 className="text-lg font-semibold">Anna Smith</h4>
                  <p className="text-gray-500">Marketing Manager</p>
                </div>
              </div>
              <p className="text-gray-600 italic">
                "The resume optimizer helped me quantify my achievements with specific metrics. I landed my dream job within two weeks of using the service."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-indigo-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to Transform Your Resume?</h2>
          <p className="text-xl text-white/90 mb-8">
            Join thousands of job seekers who have boosted their career prospects with our AI-powered resume optimization.
          </p>
          <Link 
            href="/optimize"
            className="bg-white text-indigo-600 hover:bg-white/90 font-semibold px-8 py-4 rounded-lg shadow-lg inline-block transition-all transform hover:scale-105"
          >
            Get Started Now
          </Link>
        </div>
      </section>
    </div>
  );
}

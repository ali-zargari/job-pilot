import Link from "next/link";
import Image from "next/image";
import { ArrowRight, Sparkles, FileCheck, Zap, BarChart3, Check, Star } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Progress } from "@/components/ui/Progress";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative w-full bg-gradient-to-r from-primary-600 to-secondary-600 py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 bg-grid-white bg-[size:20px_20px] opacity-20" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
        
        {/* Floating UI Elements - for visual flair */}
        <div className="absolute top-20 left-10 w-40 h-40 bg-white/5 rounded-3xl rotate-12 backdrop-blur-xl hidden lg:block"></div>
        <div className="absolute bottom-10 right-10 w-60 h-60 bg-white/5 rounded-3xl -rotate-12 backdrop-blur-xl hidden lg:block"></div>
        
        <div className="relative max-w-5xl mx-auto text-center">
          <Badge variant="warning" className="mb-4 animate-bounce-slow">Just Launched</Badge>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 tracking-tight">
            Land more interviews with <span className="text-warning-300">AI-optimized</span> resumes
          </h1>
          <p className="text-xl text-white/90 mb-10 max-w-3xl mx-auto">
            Rewrite your resume in seconds with GPT-powered feedback that makes recruiters notice. 
            Get detailed insights and ATS-proof improvements instantly.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="xl" className="group flex items-center gap-2 bg-secondary-600 text-white hover:bg-secondary-700">
              Try it free <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button size="xl" variant="outline" className="bg-white/10 text-white border-white/20 hover:bg-white/20">
              See how it works
            </Button>
          </div>
          
          {/* Social proof */}
          <div className="mt-14 flex flex-col items-center">
            <div className="flex -space-x-2">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="inline-block h-10 w-10 rounded-full ring-2 ring-white bg-gray-100 flex items-center justify-center text-xs font-medium">
                  {['JD', 'MP', 'AK', 'TW', 'SR'][i-1]}
                </div>
              ))}
            </div>
            <p className="mt-3 text-sm text-white/80">Joined by 12,000+ job seekers this month</p>
          </div>
        </div>
      </section>

      {/* Benefits Grid Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <Badge variant="default" className="mb-4">Key Features</Badge>
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">Everything you need to upgrade your resume</h2>
            <p className="text-xl text-gray-500 max-w-3xl mx-auto">
              Our AI-powered system analyzes your resume and provides detailed improvements that help you stand out to recruiters and pass ATS systems.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <Card className="border-gray-200 hover:border-primary-300 transition-colors hover:shadow-hover">
              <CardHeader>
                <div className="h-12 w-12 bg-primary-100 text-primary-700 rounded-lg flex items-center justify-center mb-4">
                  <FileCheck className="h-6 w-6" />
                </div>
                <CardTitle>ATS-Proof Format</CardTitle>
                <CardDescription>
                  Ensure your resume can be properly parsed by Applicant Tracking Systems that companies use.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Compatibility Score</span>
                  <span className="text-sm text-success-600 font-medium">92%</span>
                </div>
                <Progress value={92} variant="success" showValue />
              </CardContent>
            </Card>

            {/* Feature 2 */}
            <Card className="border-gray-200 hover:border-primary-300 transition-colors hover:shadow-hover">
              <CardHeader>
                <div className="h-12 w-12 bg-secondary-100 text-secondary-700 rounded-lg flex items-center justify-center mb-4">
                  <Sparkles className="h-6 w-6" />
                </div>
                <CardTitle>Smart Rewrites</CardTitle>
                <CardDescription>
                  Transform weak phrases and passive voice into powerful, action-oriented statements.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="rounded-lg bg-gray-50 p-3 text-sm">
                  <div className="font-medium text-danger-600 line-through mb-2">Was responsible for developing the company website</div>
                  <div className="font-medium text-success-600">Developed and launched company website, increasing user engagement by 40%</div>
                </div>
              </CardContent>
            </Card>

            {/* Feature 3 */}
            <Card className="border-gray-200 hover:border-primary-300 transition-colors hover:shadow-hover">
              <CardHeader>
                <div className="h-12 w-12 bg-warning-100 text-warning-700 rounded-lg flex items-center justify-center mb-4">
                  <Zap className="h-6 w-6" />
                </div>
                <CardTitle>Achievement Metrics</CardTitle>
                <CardDescription>
                  Quantify your work experience with specific metrics that recruiters look for.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-2">
                  <Badge variant="success" size="sm">Added</Badge>
                  <span className="text-sm">Increased sales by 27% in first quarter</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="success" size="sm">Added</Badge>
                  <span className="text-sm">Reduced customer response time by 50%</span>
                </div>
              </CardContent>
            </Card>

            {/* Feature 4 */}
            <Card className="border-gray-200 hover:border-primary-300 transition-colors hover:shadow-hover">
              <CardHeader>
                <div className="h-12 w-12 bg-success-100 text-success-700 rounded-lg flex items-center justify-center mb-4">
                  <BarChart3 className="h-6 w-6" />
                </div>
                <CardTitle>Recruiter Insights</CardTitle>
                <CardDescription>
                  Get data on how recruiters read your resume and what they focus on first.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-24 w-full bg-gray-50 rounded-lg flex items-center justify-center">
                  <Badge variant="secondary">Premium Feature</Badge>
                </div>
              </CardContent>
            </Card>

            {/* Feature 5 */}
            <Card className="border-gray-200 hover:border-primary-300 transition-colors hover:shadow-hover">
              <CardHeader>
                <div className="h-12 w-12 bg-danger-100 text-danger-700 rounded-lg flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
                    <rect x="8" y="2" width="8" height="4" rx="1" ry="1" />
                    <path d="M12 11h4" />
                    <path d="M12 16h4" />
                    <path d="M8 11h.01" />
                    <path d="M8 16h.01" />
                  </svg>
                </div>
                <CardTitle>Job Match Analysis</CardTitle>
                <CardDescription>
                  See how well your resume matches the job descriptions you're targeting.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Software Engineer</span>
                    <span className="text-sm font-medium">86%</span>
                  </div>
                  <Progress value={86} variant="warning" size="sm" />
                  
                  <div className="flex justify-between items-center mt-2">
                    <span className="text-sm">Product Manager</span>
                    <span className="text-sm font-medium">54%</span>
                  </div>
                  <Progress value={54} variant="warning" size="sm" />
                </div>
              </CardContent>
            </Card>

            {/* Feature 6 */}
            <Card className="border-gray-200 hover:border-primary-300 transition-colors hover:shadow-hover">
              <CardHeader>
                <div className="h-12 w-12 bg-gray-100 text-gray-700 rounded-lg flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="4" y="4" width="16" height="16" rx="2" />
                    <rect x="9" y="9" width="6" height="6" />
                    <path d="M15 2v2" />
                    <path d="M15 20v2" />
                    <path d="M2 15h2" />
                    <path d="M20 15h2" />
                  </svg>
                </div>
                <CardTitle>AI Cover Letters</CardTitle>
                <CardDescription>
                  Generate customized cover letters that match the job description in seconds.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button fullWidth>Generate Cover Letter</Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Resume Builder Promo Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <Badge variant="warning" className="mb-4">New Feature</Badge>
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
                Build beautiful resumes with our template builder
              </h2>
              <p className="text-xl text-gray-500 mb-6">
                Choose from professionally designed templates, customize every detail, and export a polished resume in minutes. Our template builder makes it easy to create a stunning resume that stands out.
              </p>
              <ul className="space-y-3 mb-8">
                {[
                  'Modern, professional templates designed by experts',
                  'Easy drag-and-drop customization for all sections',
                  'Export to PDF in one click',
                  'ATS-friendly formatting guaranteed'
                ].map((feature, i) => (
                  <li key={i} className="flex items-center gap-3">
                    <div className="h-6 w-6 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center flex-shrink-0">
                      <Check className="h-4 w-4" />
                    </div>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <Link href="/resume-builder">
                <Button size="lg" className="group flex items-center gap-2">
                  Try Template Builder <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            </div>
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              {/* Placeholder for resume template preview */}
              <div className="aspect-[8.5/11] bg-white rounded-lg overflow-hidden shadow-sm border border-gray-100 flex flex-col">
                <div className="h-24 bg-primary-600 p-6">
                  <div className="h-8 w-48 bg-white/20 rounded-md"></div>
                </div>
                <div className="flex-grow p-6 space-y-4">
                  <div className="h-4 w-32 bg-gray-200 rounded-md"></div>
                  <div className="space-y-2">
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                    <div className="h-3 w-3/4 bg-gray-100 rounded-md"></div>
                  </div>
                  
                  <div className="h-4 w-24 bg-gray-200 rounded-md mt-6"></div>
                  <div className="space-y-2">
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                  </div>
                  
                  <div className="h-4 w-20 bg-gray-200 rounded-md mt-6"></div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                    <div className="h-3 w-full bg-gray-100 rounded-md"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonial Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <Badge variant="secondary" className="mb-4">Testimonials</Badge>
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">Success stories from our users</h2>
            <p className="text-xl text-gray-500 max-w-3xl mx-auto">
              Thousands of job seekers have improved their career prospects with our AI-powered resume optimization.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Testimonial 1 */}
            <Card className="bg-white shadow-soft border-0">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className="flex-shrink-0">
                    <div className="h-12 w-12 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-bold">
                      JD
                    </div>
                  </div>
                  <div>
                    <CardTitle className="text-lg">John Doe</CardTitle>
                    <CardDescription>Software Engineer</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex mb-2">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <Star key={i} className="h-4 w-4 text-warning-400 fill-warning-400" />
                  ))}
                </div>
                <p className="text-gray-600">
                  "After optimizing my resume with JobPilot AI, I received 3x more interview calls. The AI improvements made my achievements sound much more impactful without exaggerating."
                </p>
              </CardContent>
              <CardFooter className="text-xs text-gray-400">
                Posted 2 weeks ago
              </CardFooter>
            </Card>

            {/* Testimonial 2 */}
            <Card className="bg-white shadow-soft border-0">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className="flex-shrink-0">
                    <div className="h-12 w-12 rounded-full bg-secondary-100 flex items-center justify-center text-secondary-700 font-bold">
                      SM
                    </div>
                  </div>
                  <div>
                    <CardTitle className="text-lg">Sarah Miller</CardTitle>
                    <CardDescription>Marketing Manager</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex mb-2">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <Star key={i} className="h-4 w-4 text-warning-400 fill-warning-400" />
                  ))}
                </div>
                <p className="text-gray-600">
                  "The resume optimizer helped me quantify my achievements with specific metrics that I hadn't thought to include. I landed my dream job within two weeks of using the service."
                </p>
              </CardContent>
              <CardFooter className="text-xs text-gray-400">
                Posted 1 month ago
              </CardFooter>
            </Card>

            {/* Testimonial 3 */}
            <Card className="bg-white shadow-soft border-0">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className="flex-shrink-0">
                    <div className="h-12 w-12 rounded-full bg-success-100 flex items-center justify-center text-success-700 font-bold">
                      RJ
                    </div>
                  </div>
                  <div>
                    <CardTitle className="text-lg">Robert Johnson</CardTitle>
                    <CardDescription>Product Manager</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex mb-2">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <Star key={i} className="h-4 w-4 text-warning-400 fill-warning-400" />
                  ))}
                </div>
                <p className="text-gray-600">
                  "I was skeptical at first, but the improvements were impressive. The AI identified weak phrases and passive voice that I'd never noticed. My resume now reads more confidently."
                </p>
              </CardContent>
              <CardFooter className="text-xs text-gray-400">
                Posted 3 weeks ago
              </CardFooter>
            </Card>
          </div>
        </div>
      </section>

      {/* Pricing Preview */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <Badge variant="default" className="mb-4">Pricing</Badge>
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">Simple, transparent pricing</h2>
            <p className="text-xl text-gray-500 max-w-3xl mx-auto">
              Choose the plan that best fits your needs. All plans include access to our core features.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free Plan */}
            <Card className="border-gray-200 bg-white">
              <CardHeader>
                <CardTitle>Free Plan</CardTitle>
                <div className="mt-4 flex items-baseline text-gray-900">
                  <span className="text-5xl font-extrabold tracking-tight">$0</span>
                  <span className="ml-1 text-xl font-semibold">/month</span>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="mt-6 space-y-4">
                  {["3 resume optimizations", "ATS compatibility check", "Basic phrase improvements", "Export as PDF"].map((feature) => (
                    <li key={feature} className="flex">
                      <Check className="h-5 w-5 text-success-500 flex-shrink-0 mr-2" />
                      <span className="text-gray-600">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter>
                <Button fullWidth>Get Started</Button>
              </CardFooter>
            </Card>

            {/* Pro Plan */}
            <Card className="border-primary-200 bg-white relative">
              <div className="absolute top-0 right-0 transform translate-x-2 -translate-y-2">
                <Badge variant="secondary">Most Popular</Badge>
              </div>
              <CardHeader>
                <CardTitle>Pro Plan</CardTitle>
                <div className="mt-4 flex items-baseline text-gray-900">
                  <span className="text-5xl font-extrabold tracking-tight">$12</span>
                  <span className="ml-1 text-xl font-semibold">/month</span>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="mt-6 space-y-4">
                  {["Unlimited resume optimizations", "ATS compatibility check", "Advanced phrase improvements", "Metrics suggestions", "Cover letter generator", "Export in all formats"].map((feature) => (
                    <li key={feature} className="flex">
                      <Check className="h-5 w-5 text-success-500 flex-shrink-0 mr-2" />
                      <span className="text-gray-600">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter>
                <Button fullWidth variant="premium">Upgrade to Pro</Button>
              </CardFooter>
            </Card>

            {/* Enterprise Plan */}
            <Card className="border-gray-200 bg-white">
              <CardHeader>
                <CardTitle>Enterprise</CardTitle>
                <div className="mt-4 flex items-baseline text-gray-900">
                  <span className="text-5xl font-extrabold tracking-tight">$29</span>
                  <span className="ml-1 text-xl font-semibold">/month</span>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="mt-6 space-y-4">
                  {["Everything in Pro plan", "Recruiter tracking analytics", "Job match scoring", "Interview preparation", "Priority support", "Career coaching discounts"].map((feature) => (
                    <li key={feature} className="flex">
                      <Check className="h-5 w-5 text-success-500 flex-shrink-0 mr-2" />
                      <span className="text-gray-600">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter>
                <Button fullWidth variant="outline">Contact Sales</Button>
              </CardFooter>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-600 to-secondary-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-white bg-[size:20px_20px] opacity-10" />
        <div className="absolute -right-40 -top-40 h-80 w-80 bg-white/10 rounded-full blur-3xl"></div>
        <div className="absolute -left-20 -bottom-20 h-60 w-60 bg-white/10 rounded-full blur-3xl"></div>
        
        <div className="max-w-4xl mx-auto text-center relative">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to transform your resume?</h2>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Join thousands of job seekers who have boosted their career prospects with our AI-powered resume optimization.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" animated variant="default" className="bg-white text-primary-600 hover:bg-gray-100">
              Try it free
            </Button>
            <Button size="lg" variant="outline" className="bg-transparent border-white text-white hover:bg-white/10">
              Learn more
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}

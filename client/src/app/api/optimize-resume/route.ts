import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    // Parse the form data from the request
    const formData = await request.formData();
    const resume = formData.get('resume');
    const jobDescription = formData.get('job_description');
    
    // Normally, you would call your backend API here
    // For now, we'll mock a response
    
    // Mock API call to our backend
    // const response = await fetch('http://localhost:8000/api/optimize', {
    //   method: 'POST',
    //   body: JSON.stringify({
    //     resume_text: await resume.text(),
    //     job_description: jobDescription
    //   }),
    //   headers: {
    //     'Content-Type': 'application/json'
    //   }
    // });
    // const data = await response.json();
    
    // For demo purposes, create a mock response
    const mockResponse = {
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
    };
    
    // Simulate API processing delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return NextResponse.json(mockResponse);
  } catch (error) {
    console.error('Error in resume optimization:', error);
    return NextResponse.json(
      { error: 'Failed to optimize resume' },
      { status: 500 }
    );
  }
} 
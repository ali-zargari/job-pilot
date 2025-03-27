import { NextResponse } from 'next/server';
import puppeteer from 'puppeteer';
import { getTemplateById, getDefaultDesignOptions } from '@/lib/resumeTemplates';
import { parseResumeText } from '@/lib/resumeParser';
import { ResumeData, ResumeTemplate, ResumeDesignOptions } from '@/types/resume';

export const dynamic = 'force-dynamic'; // No caching

export async function POST(request: Request) {
  try {
    // Parse the request body
    const body = await request.json();
    const { resumeText, templateId, designOptions } = body;
    
    if (!resumeText) {
      return NextResponse.json(
        { error: 'Resume text is required' },
        { status: 400 }
      );
    }
    
    // Parse the resume text into structured data
    const resumeData = parseResumeText(resumeText);
    
    // Get the selected template
    const template = getTemplateById(templateId || 'modern');
    
    // Get design options (use provided or defaults)
    const finalDesignOptions = designOptions || getDefaultDesignOptions(template.id);
    
    // Generate HTML for the PDF
    const html = generateResumeHTML(resumeData, template, finalDesignOptions);
    
    // Launch Puppeteer and generate PDF
    const browser = await puppeteer.launch({ 
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    // Set the HTML content
    await page.setContent(html, { waitUntil: 'networkidle0' });
    
    // Generate the PDF
    const pdf = await page.pdf({
      format: 'Letter', // US Letter size (8.5" x 11")
      printBackground: true,
      margin: {
        top: '0.4in',
        right: '0.4in',
        bottom: '0.4in',
        left: '0.4in'
      }
    });
    
    await browser.close();
    
    // Return the PDF as a response
    return new NextResponse(pdf, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename=resume.pdf'
      }
    });
    
  } catch (error) {
    console.error('Error generating PDF:', error);
    return NextResponse.json(
      { error: 'Failed to generate PDF' },
      { status: 500 }
    );
  }
}

// Function to generate HTML for the resume based on template structure
function generateResumeHTML(resumeData: ResumeData, template: ResumeTemplate, designOptions: ResumeDesignOptions) {
  // Helper function to format dates
  const formatDate = (date?: string) => {
    if (!date) return '';
    if (date.toLowerCase() === 'present') return 'Present';
    return date;
  };
  
  // Generate CSS based on the template and design options
  const css = `
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Roboto:wght@400;500;700&family=Georgia&family=Montserrat:wght@400;500;700&family=Source+Code+Pro:wght@400;600&display=swap');
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    
    body {
      font-family: ${designOptions.fontFamily};
      font-size: ${designOptions.fontSize.normal}px;
      line-height: ${designOptions.lineSpacing};
      color: #333;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    
    .resume-container {
      max-width: 8.5in;
      height: 11in;
      margin: 0 auto;
      position: relative;
      overflow: hidden;
    }
    
    h1, h2, h3, h4 {
      margin: 0;
      padding: 0;
      font-weight: 600;
    }
    
    ul {
      list-style-type: disc;
      padding-left: 1.5em;
      margin-top: 0.25em;
    }
    
    /* Template-specific styles */
    ${template.sections.contactInfo.position === 'sidebar' ? `
      .resume-layout {
        display: flex;
        height: 100%;
      }
      
      .sidebar {
        width: 30%;
        background-color: #f5f5f5;
        padding: ${designOptions.margins.left}px;
        border-right: 1px solid #ddd;
      }
      
      .main-content {
        width: 70%;
        padding: ${designOptions.margins.right}px;
        overflow: hidden;
      }
    ` : `
      .resume-layout {
        display: flex;
        flex-direction: column;
        height: 100%;
      }
      
      .header {
        padding: ${designOptions.margins.top}px ${designOptions.margins.left}px;
        background-color: #f5f5f5;
        border-bottom: 2px solid ${designOptions.primaryColor};
        text-align: center;
      }
      
      .main-content {
        flex: 1;
        padding: ${designOptions.margins.right}px;
        overflow: hidden;
      }
    `}
    
    .name {
      font-size: ${designOptions.fontSize.name}px;
      font-weight: bold;
      color: ${designOptions.primaryColor};
      margin-bottom: 0.5em;
    }
    
    .contact-info {
      font-size: ${designOptions.fontSize.normal}px;
      margin-bottom: 1.5em;
    }
    
    .section {
      margin-bottom: ${designOptions.sectionSpacing}px;
    }
    
    .section-title {
      font-size: ${designOptions.fontSize.sectionTitle}px;
      color: ${designOptions.primaryColor};
      border-bottom: 1px solid ${designOptions.primaryColor};
      padding-bottom: 0.25em;
      margin-bottom: 0.75em;
    }
    
    .item {
      margin-bottom: 0.75em;
    }
    
    .item-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.25em;
    }
    
    .item-title {
      font-size: ${designOptions.fontSize.itemTitle}px;
      font-weight: 600;
    }
    
    .item-right {
      text-align: right;
      font-size: ${designOptions.fontSize.normal - 1}px;
    }
    
    .item-company, .item-institution {
      font-weight: 500;
    }
    
    .item-subtitle {
      margin-bottom: 0.25em;
    }
    
    .skills-container {
      margin-top: 0.5em;
    }
    
    .skill-category {
      margin-bottom: 0.75em;
    }
    
    .skill-category-name {
      font-weight: 600;
      margin-bottom: 0.25em;
    }
    
    .skills-list {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5em;
    }
    
    .skill-item {
      background-color: #f0f0f0;
      padding: 0.25em 0.5em;
      border-radius: 4px;
      font-size: ${designOptions.fontSize.normal - 1}px;
    }
  `;
  
  // Generate the appropriate HTML based on the template structure
  let contentHTML = '';
  
  if (template.sections.contactInfo.position === 'sidebar') {
    // Sidebar layout
    contentHTML = `
      <div class="resume-layout">
        <div class="sidebar">
          ${template.sections.contactInfo.visible ? `
            <div class="section">
              <h1 class="name">${resumeData.contactInfo.name}</h1>
              <div class="contact-info">
                ${resumeData.contactInfo.email ? `<div>${resumeData.contactInfo.email}</div>` : ''}
                ${resumeData.contactInfo.phone ? `<div>${resumeData.contactInfo.phone}</div>` : ''}
                ${resumeData.contactInfo.location ? `<div>${resumeData.contactInfo.location}</div>` : ''}
                ${resumeData.contactInfo.linkedin ? `<div>${resumeData.contactInfo.linkedin}</div>` : ''}
                ${resumeData.contactInfo.github ? `<div>${resumeData.contactInfo.github}</div>` : ''}
                ${resumeData.contactInfo.portfolio ? `<div>${resumeData.contactInfo.portfolio}</div>` : ''}
              </div>
            </div>
          ` : ''}
          
          ${template.sections.skills.visible && template.sections.skills.position === 'sidebar' ? `
            <div class="section">
              <h2 class="section-title">Skills</h2>
              <div class="skills-container">
                ${resumeData.skills.categories.map(category => `
                  <div class="skill-category">
                    <div class="skill-category-name">${category.name}</div>
                    <ul>
                      ${category.skills.map(skill => `<li>${skill}</li>`).join('')}
                    </ul>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}
        </div>
        
        <div class="main-content">
          ${template.sections.summary.visible && template.sections.summary.position === 'main' ? `
            <div class="section">
              <h2 class="section-title">Summary</h2>
              <p>${resumeData.summary}</p>
            </div>
          ` : ''}
          
          ${template.sections.experience.visible && template.sections.experience.position === 'main' ? `
            <div class="section">
              <h2 class="section-title">Experience</h2>
              ${resumeData.experience.map(exp => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title item-company">${exp.company}</span>
                    <span class="item-right">${formatDate(exp.startDate)} - ${formatDate(exp.endDate)}</span>
                  </div>
                  <div class="item-subtitle">
                    <span>${exp.title}</span>
                    ${exp.location ? `<span class="item-right">${exp.location}</span>` : ''}
                  </div>
                  <ul>
                    ${exp.bullets.map(bullet => `<li>${bullet}</li>`).join('')}
                  </ul>
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.education.visible && template.sections.education.position === 'main' ? `
            <div class="section">
              <h2 class="section-title">Education</h2>
              ${resumeData.education.map(edu => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title item-institution">${edu.institution}</span>
                    <span class="item-right">${formatDate(edu.startDate)} - ${formatDate(edu.endDate)}</span>
                  </div>
                  <div class="item-subtitle">
                    <span>${edu.degree}${edu.field ? `, ${edu.field}` : ''}</span>
                    ${edu.location ? `<span class="item-right">${edu.location}</span>` : ''}
                    ${edu.gpa ? `<span class="item-right">GPA: ${edu.gpa}</span>` : ''}
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.skills.visible && template.sections.skills.position === 'main' ? `
            <div class="section">
              <h2 class="section-title">Skills</h2>
              <div class="skills-container">
                ${resumeData.skills.categories.map(category => `
                  <div class="skill-category">
                    <div class="skill-category-name">${category.name}:</div>
                    <div>${category.skills.join(', ')}</div>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}
          
          ${template.sections.projects.visible && resumeData.projects && resumeData.projects.length > 0 ? `
            <div class="section">
              <h2 class="section-title">Projects</h2>
              ${resumeData.projects.map(project => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title">${project.name}</span>
                    ${project.startDate || project.endDate ? `
                      <span class="item-right">
                        ${formatDate(project.startDate)}${project.endDate ? ` - ${formatDate(project.endDate)}` : ''}
                      </span>
                    ` : ''}
                  </div>
                  ${project.description ? `<p>${project.description}</p>` : ''}
                  ${project.bullets && project.bullets.length > 0 ? `
                    <ul>
                      ${project.bullets.map(bullet => `<li>${bullet}</li>`).join('')}
                    </ul>
                  ` : ''}
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.certifications.visible && resumeData.certifications && resumeData.certifications.length > 0 ? `
            <div class="section">
              <h2 class="section-title">Certifications</h2>
              ${resumeData.certifications.map(cert => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title">${cert.name}</span>
                    ${cert.date ? `<span class="item-right">${cert.date}</span>` : ''}
                  </div>
                  ${cert.issuer ? `<div>${cert.issuer}</div>` : ''}
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.additionalSections.visible && resumeData.additionalSections && resumeData.additionalSections.length > 0 ? `
            ${resumeData.additionalSections.map(section => `
              <div class="section">
                <h2 class="section-title">${section.title}</h2>
                ${section.items.map(item => `
                  <div class="item">
                    ${item.title ? `<div class="item-title">${item.title}</div>` : ''}
                    ${item.bullets && item.bullets.length > 0 ? `
                      <ul>
                        ${item.bullets.map(bullet => `<li>${bullet}</li>`).join('')}
                      </ul>
                    ` : ''}
                  </div>
                `).join('')}
              </div>
            `).join('')}
          ` : ''}
        </div>
      </div>
    `;
  } else {
    // Header layout
    contentHTML = `
      <div class="resume-layout">
        ${template.sections.contactInfo.visible ? `
          <div class="header">
            <h1 class="name">${resumeData.contactInfo.name}</h1>
            <div class="contact-info">
              ${resumeData.contactInfo.email ? `<span>${resumeData.contactInfo.email}</span> • ` : ''}
              ${resumeData.contactInfo.phone ? `<span>${resumeData.contactInfo.phone}</span> • ` : ''}
              ${resumeData.contactInfo.location ? `<span>${resumeData.contactInfo.location}</span>` : ''}
            </div>
            <div class="contact-info">
              ${resumeData.contactInfo.linkedin ? `<span>${resumeData.contactInfo.linkedin}</span> • ` : ''}
              ${resumeData.contactInfo.github ? `<span>${resumeData.contactInfo.github}</span> • ` : ''}
              ${resumeData.contactInfo.portfolio ? `<span>${resumeData.contactInfo.portfolio}</span>` : ''}
            </div>
          </div>
        ` : ''}
        
        <div class="main-content">
          ${template.sections.summary.visible ? `
            <div class="section">
              <h2 class="section-title">Summary</h2>
              <p>${resumeData.summary}</p>
            </div>
          ` : ''}
          
          ${template.sections.experience.visible ? `
            <div class="section">
              <h2 class="section-title">Experience</h2>
              ${resumeData.experience.map(exp => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title item-company">${exp.company}</span>
                    <span class="item-right">${formatDate(exp.startDate)} - ${formatDate(exp.endDate)}</span>
                  </div>
                  <div class="item-subtitle">
                    <span>${exp.title}</span>
                    ${exp.location ? `<span class="item-right">${exp.location}</span>` : ''}
                  </div>
                  <ul>
                    ${exp.bullets.map(bullet => `<li>${bullet}</li>`).join('')}
                  </ul>
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.education.visible ? `
            <div class="section">
              <h2 class="section-title">Education</h2>
              ${resumeData.education.map(edu => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title item-institution">${edu.institution}</span>
                    <span class="item-right">${formatDate(edu.startDate)} - ${formatDate(edu.endDate)}</span>
                  </div>
                  <div class="item-subtitle">
                    <span>${edu.degree}${edu.field ? `, ${edu.field}` : ''}</span>
                    ${edu.location ? `<span class="item-right">${edu.location}</span>` : ''}
                    ${edu.gpa ? `<span class="item-right">GPA: ${edu.gpa}</span>` : ''}
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.skills.visible ? `
            <div class="section">
              <h2 class="section-title">Skills</h2>
              <div class="skills-container">
                ${resumeData.skills.categories.map(category => `
                  <div class="skill-category">
                    <div class="skill-category-name">${category.name}:</div>
                    <div>${category.skills.join(', ')}</div>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}
          
          ${template.sections.projects.visible && resumeData.projects && resumeData.projects.length > 0 ? `
            <div class="section">
              <h2 class="section-title">Projects</h2>
              ${resumeData.projects.map(project => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title">${project.name}</span>
                    ${project.startDate || project.endDate ? `
                      <span class="item-right">
                        ${formatDate(project.startDate)}${project.endDate ? ` - ${formatDate(project.endDate)}` : ''}
                      </span>
                    ` : ''}
                  </div>
                  ${project.description ? `<p>${project.description}</p>` : ''}
                  ${project.bullets && project.bullets.length > 0 ? `
                    <ul>
                      ${project.bullets.map(bullet => `<li>${bullet}</li>`).join('')}
                    </ul>
                  ` : ''}
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.certifications.visible && resumeData.certifications && resumeData.certifications.length > 0 ? `
            <div class="section">
              <h2 class="section-title">Certifications</h2>
              ${resumeData.certifications.map(cert => `
                <div class="item">
                  <div class="item-header">
                    <span class="item-title">${cert.name}</span>
                    ${cert.date ? `<span class="item-right">${cert.date}</span>` : ''}
                  </div>
                  ${cert.issuer ? `<div>${cert.issuer}</div>` : ''}
                </div>
              `).join('')}
            </div>
          ` : ''}
          
          ${template.sections.additionalSections.visible && resumeData.additionalSections && resumeData.additionalSections.length > 0 ? `
            ${resumeData.additionalSections.map(section => `
              <div class="section">
                <h2 class="section-title">${section.title}</h2>
                ${section.items.map(item => `
                  <div class="item">
                    ${item.title ? `<div class="item-title">${item.title}</div>` : ''}
                    ${item.bullets && item.bullets.length > 0 ? `
                      <ul>
                        ${item.bullets.map(bullet => `<li>${bullet}</li>`).join('')}
                      </ul>
                    ` : ''}
                  </div>
                `).join('')}
              </div>
            `).join('')}
          ` : ''}
        </div>
      </div>
    `;
  }

  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>${resumeData.contactInfo.name || 'Resume'}</title>
      <style>${css}</style>
    </head>
    <body>
      <div class="resume-container">
        ${contentHTML}
      </div>
    </body>
    </html>
  `;
} 
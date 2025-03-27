import React from 'react';
import { ResumeData, Experience, Education, Project, Certification, SkillCategory } from '@/types/resume';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { v4 as uuidv4 } from 'uuid';
import { PlusIcon, TrashIcon, ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/outline';

interface ResumeEditorProps {
  resumeData: ResumeData;
  onUpdateResumeData: (data: ResumeData) => void;
  activeSection: string | null;
  setActiveSection: (section: string) => void;
}

const ResumeEditor: React.FC<ResumeEditorProps> = ({
  resumeData,
  onUpdateResumeData,
  activeSection,
  setActiveSection
}) => {
  // Handler for text input changes
  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    section: string,
    field: string,
    index?: number,
    nestedField?: string
  ) => {
    const { value } = e.target;
    const updatedData = { ...resumeData };
    
    if (section === 'contactInfo') {
      updatedData.contactInfo = {
        ...updatedData.contactInfo,
        [field]: value
      };
    } else if (section === 'summary') {
      updatedData.summary = value;
    } else if (section === 'experience' && typeof index === 'number') {
      const experiences = [...updatedData.experience];
      
      if (nestedField) {
        experiences[index] = {
          ...experiences[index],
          [nestedField]: value
        };
      } else {
        experiences[index][field as keyof Experience] = value as any;
      }
      
      updatedData.experience = experiences;
    } else if (section === 'education' && typeof index === 'number') {
      const educations = [...updatedData.education];
      
      if (nestedField) {
        educations[index] = {
          ...educations[index],
          [nestedField]: value
        };
      } else {
        educations[index][field as keyof Education] = value as any;
      }
      
      updatedData.education = educations;
    } else if (section === 'skills' && typeof index === 'number') {
      const categories = [...updatedData.skills.categories];
      
      if (field === 'name') {
        categories[index].name = value;
      } else if (field === 'skill' && typeof nestedField === 'string') {
        const skillIndex = parseInt(nestedField, 10);
        const skills = [...categories[index].skills];
        skills[skillIndex] = value;
        categories[index].skills = skills;
      }
      
      updatedData.skills.categories = categories;
    } else if (section === 'projects' && typeof index === 'number' && updatedData.projects) {
      const projects = [...updatedData.projects];
      
      if (nestedField) {
        projects[index] = {
          ...projects[index],
          [nestedField]: value
        };
      } else {
        projects[index][field as keyof Project] = value as any;
      }
      
      updatedData.projects = projects;
    } else if (section === 'certifications' && typeof index === 'number' && updatedData.certifications) {
      const certifications = [...updatedData.certifications];
      
      if (nestedField) {
        certifications[index] = {
          ...certifications[index],
          [nestedField]: value
        };
      } else {
        certifications[index][field as keyof Certification] = value as any;
      }
      
      updatedData.certifications = certifications;
    }
    
    onUpdateResumeData(updatedData);
  };
  
  // Add a new item to a section
  const handleAddItem = (section: string) => {
    const updatedData = { ...resumeData };
    
    if (section === 'experience') {
      const newExperience: Experience = {
        id: uuidv4(),
        company: 'New Company',
        title: 'Position Title',
        startDate: '',
        endDate: 'Present',
        location: '',
        bullets: ['Accomplishment or responsibility']
      };
      
      updatedData.experience = [...updatedData.experience, newExperience];
    } else if (section === 'education') {
      const newEducation: Education = {
        id: uuidv4(),
        institution: 'University/College Name',
        degree: 'Degree Type',
        field: 'Field of Study',
        startDate: '',
        endDate: '',
        location: '',
        gpa: ''
      };
      
      updatedData.education = [...updatedData.education, newEducation];
    } else if (section === 'skills') {
      const newCategory: SkillCategory = {
        name: 'New Category',
        skills: ['New Skill']
      };
      
      updatedData.skills.categories.push(newCategory);
    } else if (section === 'projects') {
      const newProject: Project = {
        id: uuidv4(),
        name: 'Project Name',
        description: '',
        startDate: '',
        endDate: '',
        bullets: ['Project detail or achievement']
      };
      
      if (!updatedData.projects) {
        updatedData.projects = [];
      }
      
      updatedData.projects = [...updatedData.projects, newProject];
    } else if (section === 'certifications') {
      const newCertification: Certification = {
        id: uuidv4(),
        name: 'Certification Name',
        issuer: 'Issuing Organization',
        date: '',
        url: ''
      };
      
      if (!updatedData.certifications) {
        updatedData.certifications = [];
      }
      
      updatedData.certifications = [...updatedData.certifications, newCertification];
    }
    
    onUpdateResumeData(updatedData);
  };
  
  // Remove an item from a section
  const handleRemoveItem = (section: string, index: number) => {
    const updatedData = { ...resumeData };
    
    if (section === 'experience') {
      const experiences = [...updatedData.experience];
      experiences.splice(index, 1);
      updatedData.experience = experiences;
    } else if (section === 'education') {
      const educations = [...updatedData.education];
      educations.splice(index, 1);
      updatedData.education = educations;
    } else if (section === 'skills') {
      const categories = [...updatedData.skills.categories];
      
      // Don't remove the last category
      if (categories.length > 1) {
        categories.splice(index, 1);
        updatedData.skills.categories = categories;
      }
    } else if (section === 'projects' && updatedData.projects) {
      const projects = [...updatedData.projects];
      projects.splice(index, 1);
      updatedData.projects = projects;
    } else if (section === 'certifications' && updatedData.certifications) {
      const certifications = [...updatedData.certifications];
      certifications.splice(index, 1);
      updatedData.certifications = certifications;
    }
    
    onUpdateResumeData(updatedData);
  };
  
  // Add a bullet point or skill to an item
  const handleAddDetail = (section: string, index: number) => {
    const updatedData = { ...resumeData };
    
    if (section === 'experience') {
      const experiences = [...updatedData.experience];
      experiences[index].bullets = [...experiences[index].bullets, 'New bullet point'];
      updatedData.experience = experiences;
    } else if (section === 'skills') {
      const categories = [...updatedData.skills.categories];
      categories[index].skills = [...categories[index].skills, 'New Skill'];
      updatedData.skills.categories = categories;
    } else if (section === 'projects' && updatedData.projects) {
      const projects = [...updatedData.projects];
      projects[index].bullets = [...projects[index].bullets, 'New project detail'];
      updatedData.projects = projects;
    }
    
    onUpdateResumeData(updatedData);
  };
  
  // Update a bullet point
  const handleDetailChange = (section: string, itemIndex: number, detailIndex: number, value: string) => {
    const updatedData = { ...resumeData };
    
    if (section === 'experience') {
      const experiences = [...updatedData.experience];
      const bullets = [...experiences[itemIndex].bullets];
      bullets[detailIndex] = value;
      experiences[itemIndex].bullets = bullets;
      updatedData.experience = experiences;
    } else if (section === 'skills') {
      const categories = [...updatedData.skills.categories];
      const skills = [...categories[itemIndex].skills];
      skills[detailIndex] = value;
      categories[itemIndex].skills = skills;
      updatedData.skills.categories = categories;
    } else if (section === 'projects' && updatedData.projects) {
      const projects = [...updatedData.projects];
      const bullets = [...projects[itemIndex].bullets];
      bullets[detailIndex] = value;
      projects[itemIndex].bullets = bullets;
      updatedData.projects = projects;
    }
    
    onUpdateResumeData(updatedData);
  };
  
  // Remove a bullet point or skill
  const handleRemoveDetail = (section: string, itemIndex: number, detailIndex: number) => {
    const updatedData = { ...resumeData };
    
    if (section === 'experience') {
      const experiences = [...updatedData.experience];
      const bullets = [...experiences[itemIndex].bullets];
      
      // Don't remove the last bullet point
      if (bullets.length > 1) {
        bullets.splice(detailIndex, 1);
        experiences[itemIndex].bullets = bullets;
        updatedData.experience = experiences;
      }
    } else if (section === 'skills') {
      const categories = [...updatedData.skills.categories];
      const skills = [...categories[itemIndex].skills];
      
      // Don't remove the last skill
      if (skills.length > 1) {
        skills.splice(detailIndex, 1);
        categories[itemIndex].skills = skills;
        updatedData.skills.categories = categories;
      }
    } else if (section === 'projects' && updatedData.projects) {
      const projects = [...updatedData.projects];
      const bullets = [...projects[itemIndex].bullets];
      
      // Don't remove the last bullet point
      if (bullets.length > 1) {
        bullets.splice(detailIndex, 1);
        projects[itemIndex].bullets = bullets;
        updatedData.projects = projects;
      }
    }
    
    onUpdateResumeData(updatedData);
  };
  
  // Move an item up or down to reorder
  const handleMoveItem = (section: string, index: number, direction: 'up' | 'down') => {
    if ((direction === 'up' && index === 0) || 
        (direction === 'down' && 
         ((section === 'experience' && index === resumeData.experience.length - 1) ||
          (section === 'education' && index === resumeData.education.length - 1) ||
          (section === 'skills' && index === resumeData.skills.categories.length - 1) ||
          (section === 'projects' && resumeData.projects && index === resumeData.projects.length - 1) ||
          (section === 'certifications' && resumeData.certifications && index === resumeData.certifications.length - 1)))) {
      return; // Can't move further in this direction
    }
    
    const updatedData = { ...resumeData };
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    
    if (section === 'experience') {
      const experiences = [...updatedData.experience];
      [experiences[index], experiences[newIndex]] = [experiences[newIndex], experiences[index]];
      updatedData.experience = experiences;
    } else if (section === 'education') {
      const educations = [...updatedData.education];
      [educations[index], educations[newIndex]] = [educations[newIndex], educations[index]];
      updatedData.education = educations;
    } else if (section === 'skills') {
      const categories = [...updatedData.skills.categories];
      [categories[index], categories[newIndex]] = [categories[newIndex], categories[index]];
      updatedData.skills.categories = categories;
    } else if (section === 'projects' && updatedData.projects) {
      const projects = [...updatedData.projects];
      [projects[index], projects[newIndex]] = [projects[newIndex], projects[index]];
      updatedData.projects = projects;
    } else if (section === 'certifications' && updatedData.certifications) {
      const certifications = [...updatedData.certifications];
      [certifications[index], certifications[newIndex]] = [certifications[newIndex], certifications[index]];
      updatedData.certifications = certifications;
    }
    
    onUpdateResumeData(updatedData);
  };
  
  // Render the contact info editor
  const renderContactInfo = () => {
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Full Name</label>
            <Input
              value={resumeData.contactInfo.name}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'contactInfo', 'name')}
              placeholder="John Doe"
              maxLength={50}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Location</label>
            <Input
              value={resumeData.contactInfo.location}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'contactInfo', 'location')}
              placeholder="City, State"
              maxLength={100}
            />
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <Input
              type="email"
              value={resumeData.contactInfo.email}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'contactInfo', 'email')}
              placeholder="email@example.com"
              maxLength={100}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Phone</label>
            <Input
              value={resumeData.contactInfo.phone}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'contactInfo', 'phone')}
              placeholder="(123) 456-7890"
              maxLength={20}
            />
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">LinkedIn</label>
            <Input
              value={resumeData.contactInfo.linkedin}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'contactInfo', 'linkedin')}
              placeholder="linkedin.com/in/username"
              maxLength={100}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">GitHub</label>
            <Input
              value={resumeData.contactInfo.github}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'contactInfo', 'github')}
              placeholder="github.com/username"
              maxLength={100}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Portfolio/Website</label>
            <Input
              value={resumeData.contactInfo.portfolio}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'contactInfo', 'portfolio')}
              placeholder="yourwebsite.com"
              maxLength={100}
            />
          </div>
        </div>
      </div>
    );
  };
  
  // Render the summary editor
  const renderSummary = () => {
    return (
      <div className="space-y-4">
        <label className="block text-sm font-medium mb-1">Professional Summary</label>
        <Textarea
          value={resumeData.summary}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleInputChange(e, 'summary', 'text')}
          placeholder="Brief summary of your qualifications, experience, and career goals..."
          rows={4}
          maxLength={500}
        />
        <p className="text-xs text-gray-500 text-right">
          {resumeData.summary.length}/500 characters
        </p>
      </div>
    );
  };
  
  // Render the experience editor
  const renderExperience = () => {
    return (
      <div className="space-y-6">
        {resumeData.experience.map((exp, index) => (
          <Card key={exp.id} className="overflow-hidden">
            <CardContent className="p-4 space-y-4">
              <div className="flex justify-between">
                <h3 className="font-medium">Experience #{index + 1}</h3>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => handleMoveItem('experience', index, 'up')}
                    disabled={index === 0}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowUpIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleMoveItem('experience', index, 'down')}
                    disabled={index === resumeData.experience.length - 1}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowDownIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleRemoveItem('experience', index)}
                    className="p-1 text-danger-500 hover:text-danger-700"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Company</label>
                  <Input
                    value={exp.company}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'experience', 'company', index)}
                    placeholder="Company Name"
                    maxLength={100}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Job Title</label>
                  <Input
                    value={exp.title}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'experience', 'title', index)}
                    placeholder="Job Title"
                    maxLength={100}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Start Date</label>
                  <Input
                    value={exp.startDate}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'experience', 'startDate', index)}
                    placeholder="MM/YYYY"
                    maxLength={20}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">End Date</label>
                  <Input
                    value={exp.endDate}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'experience', 'endDate', index)}
                    placeholder="MM/YYYY or Present"
                    maxLength={20}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Location</label>
                  <Input
                    value={exp.location}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'experience', 'location', index)}
                    placeholder="City, State"
                    maxLength={100}
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium">Achievements/Responsibilities</label>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => handleAddDetail('experience', index)}
                    className="h-7 px-2"
                  >
                    <PlusIcon className="h-3 w-3 mr-1" />
                    Add
                  </Button>
                </div>
                
                {exp.bullets.map((bullet, bulletIndex) => (
                  <div key={bulletIndex} className="flex items-start mb-2">
                    <div className="mt-2 mr-2">•</div>
                    <div className="flex-1">
                      <Textarea
                        value={bullet}
                        onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleDetailChange('experience', index, bulletIndex, e.target.value)}
                        placeholder="Describe an achievement or responsibility..."
                        className="resize-none"
                        rows={2}
                        maxLength={250}
                      />
                    </div>
                    <button 
                      onClick={() => handleRemoveDetail('experience', index, bulletIndex)}
                      disabled={exp.bullets.length <= 1}
                      className="mt-2 ml-2 text-danger-500 hover:text-danger-700 disabled:opacity-30"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
        
        <div className="text-center">
          <Button
            variant="outline"
            onClick={() => handleAddItem('experience')}
            className="w-full md:w-auto"
          >
            <PlusIcon className="h-4 w-4 mr-1" />
            Add Experience
          </Button>
        </div>
      </div>
    );
  };
  
  // Render the education editor
  const renderEducation = () => {
    return (
      <div className="space-y-6">
        {resumeData.education.map((edu, index) => (
          <Card key={edu.id} className="overflow-hidden">
            <CardContent className="p-4 space-y-4">
              <div className="flex justify-between">
                <h3 className="font-medium">Education #{index + 1}</h3>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => handleMoveItem('education', index, 'up')}
                    disabled={index === 0}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowUpIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleMoveItem('education', index, 'down')}
                    disabled={index === resumeData.education.length - 1}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowDownIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleRemoveItem('education', index)}
                    className="p-1 text-danger-500 hover:text-danger-700"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Institution</label>
                  <Input
                    value={edu.institution}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'education', 'institution', index)}
                    placeholder="University/College Name"
                    maxLength={100}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Degree</label>
                  <Input
                    value={edu.degree}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'education', 'degree', index)}
                    placeholder="Degree Type"
                    maxLength={100}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Field of Study</label>
                  <Input
                    value={edu.field}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'education', 'field', index)}
                    placeholder="Field of Study"
                    maxLength={100}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Start Date</label>
                  <Input
                    value={edu.startDate}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'education', 'startDate', index)}
                    placeholder="MM/YYYY"
                    maxLength={20}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">End Date</label>
                  <Input
                    value={edu.endDate}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'education', 'endDate', index)}
                    placeholder="MM/YYYY"
                    maxLength={20}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Location</label>
                  <Input
                    value={edu.location}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'education', 'location', index)}
                    placeholder="City, State"
                    maxLength={100}
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium">GPA</label>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => handleInputChange({ target: { value: '' } } as React.ChangeEvent<HTMLInputElement>, 'education', 'gpa', index)}
                    className="h-7 px-2"
                  >
                    {edu.gpa || 'Add GPA'}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
        
        <div className="text-center">
          <Button
            variant="outline"
            onClick={() => handleAddItem('education')}
            className="w-full md:w-auto"
          >
            <PlusIcon className="h-4 w-4 mr-1" />
            Add Education
          </Button>
        </div>
      </div>
    );
  };
  
  // Render the skills editor
  const renderSkills = () => {
    return (
      <div className="space-y-6">
        {resumeData.skills.categories.map((category, index) => (
          <Card key={category.name} className="overflow-hidden">
            <CardContent className="p-4 space-y-4">
              <div className="flex justify-between">
                <h3 className="font-medium">Skill Category #{index + 1}</h3>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => handleMoveItem('skills', index, 'up')}
                    disabled={index === 0}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowUpIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleMoveItem('skills', index, 'down')}
                    disabled={index === resumeData.skills.categories.length - 1}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowDownIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleRemoveItem('skills', index)}
                    className="p-1 text-danger-500 hover:text-danger-700"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Name</label>
                  <Input
                    value={category.name}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'skills', 'name', index)}
                    placeholder="Category Name"
                    maxLength={100}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Skills</label>
                  <Textarea
                    value={category.skills.join('\n')}
                    onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                      const skills = e.target.value.split('\n');
                      handleInputChange(e, 'skills', 'skill', index, skills[0]);
                    }}
                    placeholder="Enter skills separated by new lines"
                    rows={4}
                    maxLength={500}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
        
        <div className="text-center">
          <Button
            variant="outline"
            onClick={() => handleAddItem('skills')}
            className="w-full md:w-auto"
          >
            <PlusIcon className="h-4 w-4 mr-1" />
            Add Skill Category
          </Button>
        </div>
      </div>
    );
  };
  
  // Render the projects editor
  const renderProjects = () => {
    return (
      <div className="space-y-6">
        {resumeData.projects.map((project, index) => (
          <Card key={project.id} className="overflow-hidden">
            <CardContent className="p-4 space-y-4">
              <div className="flex justify-between">
                <h3 className="font-medium">Project #{index + 1}</h3>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => handleMoveItem('projects', index, 'up')}
                    disabled={index === 0}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowUpIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleMoveItem('projects', index, 'down')}
                    disabled={index === resumeData.projects.length - 1}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowDownIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleRemoveItem('projects', index)}
                    className="p-1 text-danger-500 hover:text-danger-700"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Name</label>
                  <Input
                    value={project.name}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'projects', 'name', index)}
                    placeholder="Project Name"
                    maxLength={100}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Description</label>
                  <Textarea
                    value={project.description}
                    onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleInputChange(e, 'projects', 'description', index)}
                    placeholder="Enter project description"
                    rows={4}
                    maxLength={500}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Start Date</label>
                  <Input
                    value={project.startDate}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'projects', 'startDate', index)}
                    placeholder="MM/YYYY"
                    maxLength={20}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">End Date</label>
                  <Input
                    value={project.endDate}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'projects', 'endDate', index)}
                    placeholder="MM/YYYY"
                    maxLength={20}
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium">Details</label>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => handleAddDetail('projects', index)}
                    className="h-7 px-2"
                  >
                    <PlusIcon className="h-3 w-3 mr-1" />
                    Add
                  </Button>
                </div>
                
                {project.bullets.map((bullet, bulletIndex) => (
                  <div key={bulletIndex} className="flex items-start mb-2">
                    <div className="mt-2 mr-2">•</div>
                    <div className="flex-1">
                      <Textarea
                        value={bullet}
                        onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleDetailChange('projects', index, bulletIndex, e.target.value)}
                        placeholder="Enter a project detail or achievement"
                        className="resize-none"
                        rows={2}
                        maxLength={250}
                      />
                    </div>
                    <button 
                      onClick={() => handleRemoveDetail('projects', index, bulletIndex)}
                      disabled={project.bullets.length <= 1}
                      className="mt-2 ml-2 text-danger-500 hover:text-danger-700 disabled:opacity-30"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
        
        <div className="text-center">
          <Button
            variant="outline"
            onClick={() => handleAddItem('projects')}
            className="w-full md:w-auto"
          >
            <PlusIcon className="h-4 w-4 mr-1" />
            Add Project
          </Button>
        </div>
      </div>
    );
  };
  
  // Render the certifications editor
  const renderCertifications = () => {
    return (
      <div className="space-y-6">
        {resumeData.certifications.map((cert, index) => (
          <Card key={cert.id} className="overflow-hidden">
            <CardContent className="p-4 space-y-4">
              <div className="flex justify-between">
                <h3 className="font-medium">Certification #{index + 1}</h3>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => handleMoveItem('certifications', index, 'up')}
                    disabled={index === 0}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowUpIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleMoveItem('certifications', index, 'down')}
                    disabled={index === resumeData.certifications.length - 1}
                    className="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-30"
                  >
                    <ArrowDownIcon className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleRemoveItem('certifications', index)}
                    className="p-1 text-danger-500 hover:text-danger-700"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Name</label>
                  <Input
                    value={cert.name}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'certifications', 'name', index)}
                    placeholder="Certification Name"
                    maxLength={100}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Issuer</label>
                  <Input
                    value={cert.issuer}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'certifications', 'issuer', index)}
                    placeholder="Issuing Organization"
                    maxLength={100}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Date</label>
                  <Input
                    value={cert.date}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'certifications', 'date', index)}
                    placeholder="MM/YYYY"
                    maxLength={20}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">URL</label>
                  <Input
                    value={cert.url}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(e, 'certifications', 'url', index)}
                    placeholder="https://example.com"
                    maxLength={100}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
        
        <div className="text-center">
          <Button
            variant="outline"
            onClick={() => handleAddItem('certifications')}
            className="w-full md:w-auto"
          >
            <PlusIcon className="h-4 w-4 mr-1" />
            Add Certification
          </Button>
        </div>
      </div>
    );
  };
  
  // Render the active section
  const renderActiveSectionContent = () => {
    if (!activeSection || activeSection === 'overview') {
      // Show overview for null, undefined, or explicit 'overview' value
      return (
        <div className="space-y-8">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h3 className="font-medium text-blue-700 mb-2">Your Resume Content</h3>
            <p className="text-sm text-blue-600">
              We've extracted the content from your resume. Click on any section tab above to edit that section in detail.
            </p>
          </div>
          
          <div className="space-y-6">
            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Contact Information</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-2">
                  <div><span className="font-medium">Name:</span> {resumeData.contactInfo.name || <span className="text-gray-400 italic">Not provided</span>}</div>
                  <div><span className="font-medium">Email:</span> {resumeData.contactInfo.email || <span className="text-gray-400 italic">Not provided</span>}</div>
                  <div><span className="font-medium">Phone:</span> {resumeData.contactInfo.phone || <span className="text-gray-400 italic">Not provided</span>}</div>
                  <div><span className="font-medium">Location:</span> {resumeData.contactInfo.location || <span className="text-gray-400 italic">Not provided</span>}</div>
                  {resumeData.contactInfo.linkedin && (
                    <div><span className="font-medium">LinkedIn:</span> {resumeData.contactInfo.linkedin}</div>
                  )}
                  {resumeData.contactInfo.github && (
                    <div><span className="font-medium">GitHub:</span> {resumeData.contactInfo.github}</div>
                  )}
                  {resumeData.contactInfo.portfolio && (
                    <div><span className="font-medium">Portfolio:</span> {resumeData.contactInfo.portfolio}</div>
                  )}
                </div>
                <div className="mt-3 text-right">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => setActiveSection('contactInfo')}
                  >
                    Edit Contact Info
                  </Button>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Professional Summary</h3>
                {resumeData.summary ? (
                  <p className="text-gray-700">{resumeData.summary}</p>
                ) : (
                  <p className="text-gray-400 italic">No summary provided</p>
                )}
                <div className="mt-3 text-right">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => setActiveSection('summary')}
                  >
                    Edit Summary
                  </Button>
                </div>
              </CardContent>
            </Card>
            
            {resumeData.experience.length > 0 ? (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Experience ({resumeData.experience.length} entries)</h3>
                  {resumeData.experience.slice(0, 2).map((exp, index) => (
                    <div key={exp.id} className={`${index > 0 ? 'mt-4 pt-4 border-t' : ''}`}>
                      <div className="flex justify-between">
                        <div className="font-medium text-gray-900">{exp.title || <span className="italic text-gray-400">Position</span>}</div>
                        <div className="text-sm text-gray-500">
                          {exp.startDate && exp.endDate ? 
                            `${exp.startDate} - ${exp.endDate}` : 
                            <span className="italic text-gray-400">No dates provided</span>
                          }
                        </div>
                      </div>
                      <div className="text-gray-700">{exp.company || <span className="italic text-gray-400">Company</span>}{exp.location ? `, ${exp.location}` : ''}</div>
                      {exp.bullets.length > 0 ? (
                        <ul className="mt-2 text-sm text-gray-600 list-disc list-inside">
                          {exp.bullets.slice(0, 2).map((bullet, i) => (
                            <li key={i}>{bullet}</li>
                          ))}
                          {exp.bullets.length > 2 && <li className="text-gray-500 italic">+ {exp.bullets.length - 2} more bullet points</li>}
                        </ul>
                      ) : (
                        <p className="mt-2 text-sm text-gray-400 italic">No bullet points provided</p>
                      )}
                    </div>
                  ))}
                  {resumeData.experience.length > 2 && (
                    <div className="mt-3 text-center">
                      <p className="text-sm text-gray-500 mb-2">+ {resumeData.experience.length - 2} more experiences not shown</p>
                    </div>
                  )}
                  <div className="mt-3 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setActiveSection('experience')}
                    >
                      {resumeData.experience.length > 0 ? 'Edit Experience' : 'Add Experience'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Experience</h3>
                  <p className="text-gray-400 italic">No experience entries found</p>
                  <div className="mt-3 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setActiveSection('experience')}
                    >
                      Add Experience
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
            
            {resumeData.education.length > 0 ? (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Education ({resumeData.education.length} entries)</h3>
                  {resumeData.education.slice(0, 2).map((edu, index) => (
                    <div key={edu.id} className={`${index > 0 ? 'mt-4 pt-4 border-t' : ''}`}>
                      <div className="flex justify-between">
                        <div className="font-medium text-gray-900">{edu.institution || <span className="italic text-gray-400">Institution</span>}</div>
                        <div className="text-sm text-gray-500">
                          {edu.startDate && edu.endDate ? 
                            `${edu.startDate} - ${edu.endDate}` : 
                            <span className="italic text-gray-400">No dates provided</span>
                          }
                        </div>
                      </div>
                      <div className="text-gray-700">
                        {edu.degree ? edu.degree : <span className="italic text-gray-400">Degree</span>}
                        {edu.field ? ` in ${edu.field}` : ''}
                        {edu.gpa ? ` - GPA: ${edu.gpa}` : ''}
                      </div>
                      {edu.location && <div className="text-sm text-gray-600">{edu.location}</div>}
                    </div>
                  ))}
                  {resumeData.education.length > 2 && (
                    <div className="mt-3 text-center">
                      <p className="text-sm text-gray-500 mb-2">+ {resumeData.education.length - 2} more education entries not shown</p>
                    </div>
                  )}
                  <div className="mt-3 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setActiveSection('education')}
                    >
                      {resumeData.education.length > 0 ? 'Edit Education' : 'Add Education'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Education</h3>
                  <p className="text-gray-400 italic">No education entries found</p>
                  <div className="mt-3 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setActiveSection('education')}
                    >
                      Add Education
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
            
            {resumeData.skills.categories.length > 0 && (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Skills</h3>
                  {resumeData.skills.categories.map((category, index) => (
                    <div key={index} className={index > 0 ? 'mt-3' : ''}>
                      {resumeData.skills.categories.length > 1 && (
                        <div className="font-medium text-gray-700">{category.name}:</div>
                      )}
                      {category.skills.length > 0 ? (
                        <div className="flex flex-wrap gap-1 mt-1">
                          {category.skills.slice(0, 10).map((skill, i) => (
                            <span 
                              key={i} 
                              className="bg-gray-100 text-gray-800 px-2 py-1 rounded-md text-sm"
                            >
                              {skill}
                            </span>
                          ))}
                          {category.skills.length > 10 && (
                            <span className="bg-gray-50 text-gray-500 px-2 py-1 rounded-md text-sm italic">
                              + {category.skills.length - 10} more
                            </span>
                          )}
                        </div>
                      ) : (
                        <p className="text-gray-400 italic">No skills found in this category</p>
                      )}
                    </div>
                  ))}
                  <div className="mt-3 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setActiveSection('skills')}
                    >
                      Edit Skills
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
            
            {resumeData.projects && resumeData.projects.length > 0 && (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Projects ({resumeData.projects.length})</h3>
                  {resumeData.projects.slice(0, 1).map((project) => (
                    <div key={project.id}>
                      <div className="font-medium text-gray-900">{project.name}</div>
                      {project.description && <div className="text-sm text-gray-700 mt-1">{project.description}</div>}
                      {project.bullets.length > 0 && (
                        <ul className="mt-2 text-sm text-gray-600 list-disc list-inside">
                          {project.bullets.slice(0, 2).map((bullet, i) => (
                            <li key={i}>{bullet}</li>
                          ))}
                          {project.bullets.length > 2 && <li className="text-gray-500 italic">+ {project.bullets.length - 2} more details</li>}
                        </ul>
                      )}
                    </div>
                  ))}
                  {resumeData.projects.length > 1 && (
                    <div className="mt-3 text-center">
                      <p className="text-sm text-gray-500 mb-2">+ {resumeData.projects.length - 1} more projects not shown</p>
                    </div>
                  )}
                  <div className="mt-3 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setActiveSection('projects')}
                    >
                      Edit Projects
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
            
            {resumeData.certifications && resumeData.certifications.length > 0 && (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Certifications/Awards ({resumeData.certifications.length})</h3>
                  <div className="mt-3 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setActiveSection('certifications')}
                    >
                      Edit Certifications
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
            
            {resumeData.additionalSections.length > 0 && (
              <Card>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-800 border-b pb-2 mb-3">Additional Sections</h3>
                  {resumeData.additionalSections.map((section, i) => (
                    <div key={i} className={`${i > 0 ? 'mt-4 pt-4 border-t' : ''}`}>
                      <div className="font-medium text-gray-900 mb-1">{section.title}</div>
                      <div className="text-sm text-gray-600">
                        {typeof section.content === 'string' ? 
                          (section.content.substring(0, 100) + (section.content.length > 100 ? '...' : '')) : 
                          'Content not available as text'
                        }
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      );
    }

    switch (activeSection) {
      case 'contactInfo':
        return renderContactInfo();
      case 'summary':
        return renderSummary();
      case 'experience':
        return renderExperience();
      case 'education':
        return renderEducation();
      case 'skills':
        return renderSkills();
      case 'projects':
        return renderProjects();
      case 'certifications':
        return renderCertifications();
      default:
        // Show overview as fallback
        return (
          <div className="space-y-8">
            {/* Rest of the overview content ... */}
          </div>
        );
    }
  };
  
  return (
    <div className="space-y-4">
      <Tabs 
        value={activeSection || "overview"} 
        onValueChange={setActiveSection}
        className="flex flex-col md:flex-row"
      >
        <TabsList className="mb-4 grid grid-cols-3 md:grid-cols-7 gap-2">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="contactInfo">Contact Info</TabsTrigger>
          <TabsTrigger value="summary">Summary</TabsTrigger>
          <TabsTrigger value="experience">Experience</TabsTrigger>
          <TabsTrigger value="education">Education</TabsTrigger>
          <TabsTrigger value="skills">Skills</TabsTrigger>
          <TabsTrigger value="projects">Projects</TabsTrigger>
        </TabsList>
        
        <div className="flex-1 p-4 bg-white rounded-md">
          {renderActiveSectionContent()}
        </div>
      </Tabs>
    </div>
  );
};

export default ResumeEditor; 
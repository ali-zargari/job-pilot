#!/usr/bin/env python
"""
Setup script for the ai_processing package.
"""

from setuptools import setup, find_packages

setup(
    name="ai_processing",
    version="0.1.0",
    author="Job Pilot AI Team",
    author_email="support@jobpilotai.com",
    description="AI-powered resume and job application optimization tools",
    long_description="AI-powered resume optimization and job application tools",
    long_description_content_type="text/markdown",
    url="https://github.com/your-organization/job-pilot-ai",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "numpy>=1.20.0",
        "tqdm>=4.62.0",
    ],
    entry_points={
        "console_scripts": [
            "optimize-resume=ai_processing.scripts.optimize_resume:main",
        ],
    },
) 
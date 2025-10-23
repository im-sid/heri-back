"""
Heri-Sci Backend Setup
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="heri-sci-backend",
    version="1.0.0",
    description="AI-Powered Historical Artifact Analysis & Sci-Fi Story Generator Backend",
    author="Heri-Sci Team",
    author_email="your-email@example.com",
    url="https://github.com/im-sid/heri",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    keywords="ai, image-processing, historical-artifacts, gemini, flask",
)

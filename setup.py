#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindCard - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent

with open(here / "README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mindcard-cli",
    version="1.0.0",
    description="MindCard - Terminal AI-Powered Markdown Knowledge Card Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MindCard Team",
    author_email="mindcard@example.com",
    url="https://github.com/gitstq/MindCard",
    py_modules=["mindcard"],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mindcard=mindcard:main",
            "mc=mindcard:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Office/Business :: Scheduling",
    ],
    keywords="knowledge management markdown cli terminal notes productivity",
    license="MIT",
)

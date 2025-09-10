#!/usr/bin/env python
"""
@file : setup.py
"""

from setuptools import setup, find_packages

## For first time setup, use:
#__version__ = "0.1.1"
# Instead of what will work from then on:
from mendeleevspellingbee import __version__

setup(
    name="mendeleevspellingbee",
    version=__version__,
    description="A CLI tool for decoding words using chemical element symbols",
    author="D",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "nltk>=3.8.1"
    ],
    entry_points={
        "console_scripts": [
            "mendeleevspellingbee = mendeleevspellingbee.core:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    extras_require={
        "dev": ["bumpversion", "pytest"]
    },
)


#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup

# build command
setup(
    name="records",
    version="0.0.1",
    author="Jared Meek",
    packages=["records"],
    entry_points={
        'console_scripts': ['records = records.records:Records']
    }
)

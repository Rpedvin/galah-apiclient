#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "galah-apiclient",
    version = read("VERSION").strip(),
    author = "Galah Group LLC and other contributers",
    author_email = "jsull003@ucr.edu",
    description = "A Python script for interacting with Galah.",
    license = "Apache v2.0",
    keywords = "galah",
    url = "https://www.github.com/galah-group/galah-apiclient",
    packages = find_packages(),
    long_description = read("README.md"),
    install_requires = [
        "rauth==0.5.4"
    ],
    classifiers = [
        "License :: OSI Approved :: Apache Software License",
    ]
)

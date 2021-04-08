#! /usr/bin/env python
import os

from setuptools import setup


CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
with open(README_PATH, "r", encoding="utf8") as f:
    README = f.read()

setup(
    name="ariadne_django",
    author="Lexria",
    author_email="noreply@lexria.com",
    description="ariadne_django is a python library for integrating django with ariadne.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="BSD",
    version="0.1.0",
    url="https://github.com/reset-button/ariadne_django",
    packages=["ariadne_django"],
    include_package_data=True,
    install_requires=[
        "django>=2.2.0",
        "ariadne>=0.13.0",
    ],
    classifiers=CLASSIFIERS,
    platforms=["any"],
    zip_safe=False,
)

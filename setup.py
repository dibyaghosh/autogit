import os
import setuptools


def get_readme():
    with open("README.md", "r") as f:
        return f.read()

setuptools.setup(
    name="rlutil",
    version="0.1.0",
    description="Utilities for RL algorithms",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    python_requires=">=3.5.0",
    packages=setuptools.find_packages(),
)
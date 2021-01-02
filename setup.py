import os
import setuptools


def get_readme():
    with open("README.md", "r") as f:
        return f.read()

setuptools.setup(
    name="autogit",
    version="0.1.0",
    description="Programatically progressive backing up a git repo",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6.0",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "autogit-backup = autogit.autogit:main"
        ]
    },
)
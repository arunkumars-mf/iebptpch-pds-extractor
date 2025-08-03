from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iebptpch-pds-extractor",
    version="1.0.1",
    author="Arunkumar Selvam",
    author_email="aruninfy123@gmail.com",
    description="Extract PDS members from IEBPTPCH output files with support for both ASCII and EBCDIC formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arunkumars-mf/iebptpch-pds-extractor",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies - uses standard library only
    ],
    entry_points={
        "console_scripts": [
            "iebptpch-pds-extractor=iebptpch_pds_extractor:main",
        ],
    },
    keywords="mainframe pds iebptpch ebcdic ascii extractor ibm z/os mvs",
    project_urls={
        "Bug Reports": "https://github.com/arunkumars-mf/iebptpch-pds-extractor/issues",
        "Source": "https://github.com/arunkumars-mf/iebptpch-pds-extractor",
        "Documentation": "https://github.com/arunkumars-mf/iebptpch-pds-extractor#readme",
    },
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-blog-truncate",
    version="0.1.0",
    description="MkDocs plugin to automatically truncate blog posts after specified number of lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sohom B",
    url="https://github.com/83bytes/mkdocs-blog-truncate",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mkdocs>=1.0.0",
    ],
    entry_points={
        "mkdocs.plugins": [
            "blog_truncate = mkdocs_blog_truncate.plugin:BlogTruncatePlugin",
        ]
    },
)

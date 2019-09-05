from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="1882-bot",
    version="1.2.0",
    packages=find_packages(),
    description="A moderator bot for r/coys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkdevtoronto/1882-bot",
    author="bkdevtoronto",
    author_email="ben@bkdev.co.uk",
    license="MIT",
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    keywords="coys tottenham spurs moderator mod reddit bot",
    project_urls={
        "Documentation": "https://bkdevtoronto.github.io/1882-Bot/",
        "Source": "https://github.com/bkdevtoronto/1882-Bot"
    },
    python_requires='>=3.6'
)

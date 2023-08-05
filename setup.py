import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

SRC_REPO_NAME = "TextSummarizer"
AUTHOR_USER_NAME = "jjjjjooooo"
GITHUB_REPO_NAME = "TextSummarizer"
AUTHOR_EMAIL = "jinoujoe@gmail.com"
DESCRIPTION = "A small python package for NLP app"

setuptools.setup(
    name=SRC_REPO_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{GITHUB_REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{GITHUB_REPO_NAME}/issues",
    },
    packages=setuptools.find_packages(),
)

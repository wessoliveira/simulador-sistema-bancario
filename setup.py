from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="sistema_bancario",
    version="0.0.1",
    author="Wesley Oliveira",
    author_email="wessoliveira@gmail.com",
    description="Contains a banking system simulator, with the possibility of creating users and accounts. " \
    "Also, it allows for depositing and withdrawing money from the main account of the user.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wessoliveira/simulador-sistema-bancario",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
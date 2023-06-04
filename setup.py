from setuptools import setup, find_packages

setup(
    name="meta",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.2.9",
        "openai>=0.27.7",
        "python-dotenv>=1.0.0",
        "pytest>=7.3.1",
        "RestrictedPython>=6.0",
    ],
)

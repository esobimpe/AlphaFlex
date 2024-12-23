from setuptools import setup, find_packages
import os

# Read the contents of your README.md
def read_readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
        return f.read()

setup(
    name="alpha_flex",
    version="1.14.7",
    description="A Python library for managing a growth-focused portfolio, including portfolio tracking, backtesting, performance analysis, and automated trading with brokerage integration.",
    long_description=read_readme(),  # Use the README.md contents for PyPI
    long_description_content_type="text/markdown",  # Ensure it's recognized as markdown
    author="Eniola Sobimpe",
    author_email="sobimpeeniola@gmail.com",
    url="https://github.com/esobimpe/alpha_flex",
    packages=find_packages(),
    install_requires=[
        "yfinance",
        "numpy",
        "pandas",
        "finvizfinance"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",  # Correct license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

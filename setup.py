from setuptools import setup, find_packages

setup(
    name="alpha_flex",
    version="1.9.0",
    description="A Python library for building growth-focused ETF portfolios.",
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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

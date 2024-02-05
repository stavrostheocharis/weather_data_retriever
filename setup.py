from setuptools import setup, find_packages

with open("LICENSE") as f:
    license = f.read()

long_description = open("README.md", "r").read()

setup(
    name="weather_data_retriever",
    packages=find_packages(exclude="tests"),
    version="0.2.2",
    license=license,
    description="Weather data retriever",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Stavros Theocharis",
    author_email="stavrostheocharis@yahoo.gr",
    url="https://github.com/stavrostheocharis/weather_data_retriever.git",
    keywords=["weather data", "historical data", "meteo data", "nasa data"],
    install_requires=[
        "pandas",
        "geopy",
        "requests",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

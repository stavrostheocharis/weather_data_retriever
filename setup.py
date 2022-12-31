from setuptools import setup, find_packages

with open("LICENSE") as f:
    license = f.read()

setup(
    name="weather_data_retriever",
    version="1.0",
    author="Stavros Theocharis",
    description="Nasa weather data retriever",
    long_description="Nasa weather data retriever",
    url="https://github.com/stavrostheocharis/weather_data_retriever.git",
    packages=find_packages(exclude="tests"),
    install_requires=[
        "pandas",
        "geopy",
        "requests",
    ],
    license=license,
)

from setuptools import setup, find_packages

with open("LICENSE") as f:
    license = f.read()

setup(
    name="weather_data_retriever",
    version="1.1",
    author="Stavros Theocharis",
    description="Weather data retriever",
    long_description="Multiple sources weather data retriever",
    url="https://github.com/stavrostheocharis/weather_data_retriever.git",
    packages=find_packages(exclude="tests"),
    install_requires=[
        "pandas",
        "geopy",
        "requests",
    ],
    license=license,
)

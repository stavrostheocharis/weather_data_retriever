from setuptools import setup, find_packages

with open("LICENSE") as f:
    license = f.read()

long_description = open("README.md", "r").read()

setup(
    name="weather_data_retriever",
    packages=find_packages(exclude="tests"),
    version="0.1.0",
    license=license,
    description="Weather data retriever",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Stavros Theocharis",
    author_email="stavrostheocharis@yahoo.gr",
    url="https://github.com/stavrostheocharis/weather_data_retriever.git",
    keywords=[
        "weather data",
        "historical data",
        "meteo data",
        "nasa data"
    ]
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


[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label

[github_link]: https://github.com/stavrostheocharis/easy_explain

[pypi_badge]: https://badge.fury.io/py/easy-explain.svg

[pypi_link]: https://pypi.org/project/easy-explain/

[download_badge]: https://badgen.net/pypi/dm/easy-explain

[download_link]: https://pypi.org/project/easy-explain/#files

[licence_badge]: https://img.shields.io/github/license/stavrostheocharis/streamlit-token-craft

[licence_link]: LICENSE
<div align="center">

# Weather data retriever
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](#supported-python-versions) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-MIT-informational.svg)](https://github.com/artefactory-global/streamlit_prophet/blob/main/LICENSE)

Retriever of NASA's weather data 

</div>

## Requirements
### Python version
* Main supported version : <strong>3.9</strong> <br>
* Other supported versions : <strong>3.7</strong> & <strong>3.8</strong>

To use the scripts on your computer, please make sure you have one of these versions installed.

### Install environment & dependencies

In order to install the current repo you have 2 options:
- Installation as a project repo
- Pip install it directly from git inside your prefered repo and use it as a package

#### Installation as a project

In order to run the needed scripts you need to have python installed and run the command below.
```
python3 -m venv /path/to/new/virtual/environment
```

To activate your `venv` run `source "env_name"/bin/activate`.

To install dependencies run the command:

```bash
pip install -r requirements.txt
```

#### Installation as a package

In order to use the current repo as a package you need to run the command below inside your project.

```bash
pip install git+https://github.com/stavrostheocharis/weather_data_retriever.git
```

## Information about the functionality

This package is based on [Nasa's weather open API and 'POWER' tools and application](https://power.larc.nasa.gov/docs/). The data that can be fetched are historical. The aggragation cases and the different community cases that can be used are analysed below:

[**Aggregation**](https://power.larc.nasa.gov/docs/services/api/temporal/)
- *Climatology*:	Provides parameters as climatologies for a pre-defined period with monthly average, maximum, and/or minimum values available.
- *Monthly*:	Provides parameters by year; the annual and each month's average, maximum, and/or minimum values.
- *Daily*:	Provides parameters by day with average, maximum, and/or minimum values.
- *Hourly*:	Provides parameters by hour with average values.

[**Communities**](https://power.larc.nasa.gov/docs/methodology/communities/)
- *AG*: The Agroclimatology (AG) solar and meteorological parameters are available as daily mean time series formats. All parameters are provided on the original resolution grid, which is dependent on the parameter. The daily time series include the basic solar and meteorology parameters to support agricultural decision support tools such as the Decision Support System for Agro-technology Transfer. The hourly time series is a smaller subset of the solar and meteorology parameters.
- *RE*: The Renewable Energy (RE) solar and meteorological parameters are available as climatologically and inter-annual (monthly and annual) averaged values, as well as in a daily time series format for user selected grids. All RE parameters are provided on the original resolution grid, which is dependent on the parameter. The climatologically averaged parameters are calculated to support applications such as solar cooking, sizing solar panels, and sizing battery backup systems. The monthly and annually averaged parameters are provided as monthly and annual averaged values by year for each of the base solar and meteorological data parameters. The daily and hourly time series include the basic solar and meteorology parameters as well as additional calculated parameters such as diffuse and direct normal radiation.
- *SB*: The Sustainable Buildings (SB) solar and meteorological parameters are available as climatologically, monthly, and annually average values, as well as in a daily time series format. All parameters are provided on the original resolution grid, which is dependent on the parameter. The climatologically averaged parameters are calculated to support the preliminary design and site selection for building projects. Monthly and annually averaged parameters are provided as monthly and annual averaged values by year. The daily time series include a range of the basic solar and meteorology parameters as well as additional calculated parameters such as diffuse and direct normal radiation, heating and cooling degree days, climate zones, etc. The hourly time series is a smaller subset of the solar and meteorology parameters.

The current implementation of the package also supports "point", or "regional" cases. Point vase be used for cities, or small areas, or for geting data of the center of a country. 

Regional can be used for cases of geting data based on bounded boxes of a country in order to get the different values.

The different variables that can be fetched are:
- **"T2M"**: Temperature at 2 Meters (°C)
- **"T2MDEW"**: Dew/Frost Point at 2 Meters (°C)
- **"T2MWET"**: Wet Bulb Temperature at 2 Meters (°C)
- **"TS"**: Earth Skin Temperature (°C)
- **"T2M_RANGE"**: Temperature at 2 Meters Range (°C)
- **"T2M_MAX"**: Temperature at 2 Meters Maximum (°C)
- **"T2M_MIN"**: Temperature at 2 Meters Minimum (°C)
- **"RH2M: Relative"** Humidity at 2 Meters (%)
- **"PRECTOTCORR"**: Precipitation Corrected (mm/day)
- **"WS2M"**: Wind Speed at 2 Meters (m/s)
- **"ALLSKY_SFC_SW_DWN"**: All Sky Surface Shortwave Downward Irradiance (kW-hr/m^2/day)
## How to contribute?

We welcome any suggestions, problem reports, and contributions!
For any changes you would like to make to this project, we invite you to submit an [issue](https://github.com/stavrostheocharis/weather_data_retriever/issues).

For more information, see [`CONTRIBUTING`](https://github.com/stavrostheocharis/weather_data_retriever/blob/main/CONTRIBUTING.md) instructions.
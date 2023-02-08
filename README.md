<div align="center">

# Weather data retriever
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](#supported-python-versions) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-MIT-informational.svg)](https://github.com/stavrostheocharis/weather_data_retriever/blob/main/LICENSE)

**Retriever of multiple sources weather data**
(NASA's larc-power project, open-meteo) 

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

This package is based on multiple open weather API'sand combines them in a simple form for use. The API's that are being used are listed below:
- [Nasa's weather open API (larc-power) and 'POWER' tools and application](https://power.larc.nasa.gov/docs/). 
- [Open-Meteo's weather API collaborating with national weather services providing open data](https://open-meteo.com/).

### Nasa's weather open API (larc-power)
The data that can be fetched are historical. The aggregation cases and the different community cases that can be used are analysed below:

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

Each aggregation level permits a specific set of variables to be used:
The "T2M", "T2MDEW", "T2MWET", "TS", "RH2M", "PRECTOT", "WS2M", and "ALLSKY SFC SW DWN" variables are the lowest-level variables that can be used in any of the aggregation levels. Additional "T2M RANGE," "T2M MAX," and "T2M MIN" can be utilized at all aggregation levels outside the hourly level.

Statistics and availability of the data can be found at [power dashboard](https://power.larc.nasa.gov/dashboard/).

Please follow the [quick start notebook](larc_power_quick_start.ipynb) in order to understand how to easily get started.

### Open-Meteo's weather API

This part can be used for both historical and forecasted data.

[**Aggregation**](https://power.larc.nasa.gov/docs/services/api/temporal/)
- *Daily*:	Provides parameters by day with average, maximum, and/or minimum values.
- *Hourly*:	Provides parameters by hour with average values.

The main different variables that can be fetched are:
- **temperature_2m**: Temperature at 2 Meters (°C)
- **temperature_2m_max**: Maximum daily air temperature at 2 meters above ground (°C)
- **temperature_2m_min**: Minimum daily air temperature at 2 meters above ground (°C)
- **apparent_temperature**: Apparent temperature (°C)
- **apparent_temperature_max**: Maximum daily apparent temperature (°C)
- **apparent_temperature_min**: Minimum daily apparent temperature (°C)
- **relativehumidity_2m**: Relative humidity at 2 meters above ground (%)
- **dewpoint_2m**: Dew point temperature at 2 meters above ground (°C)
- **sunrise**: Time of sunrise
- **precipitation**: Total precipitation (rain, showers, snow) sum of the preceding hour (mm)
- **precipitation_sum**: Total precipitation sum (rain, showers, snow) (mm)
- **rain_sum**: 	Rain from large scale weather systems of the preceding hour in millimeter
- **snowfall**: Snowfall amount of the preceding hour in centimeters
- **showers**: Showers from convective precipitation in millimeters from the preceding hour
- **showers_sum**: Showers sum from convective precipitation in millimeters
- **snowfall_sum**: Snowfall sum amount in centimeters

Each aggregation level permits a specific set of variables to be used. In addition, more variables than the above are supported by this API. In order to choose your prefered ones to use, have a look at [historical weather api](https://open-meteo.com/en/docs/historical-weather-api) and at [forecast weather api](https://open-meteo.com/en/docs).

Open-Meteo's source code is available on [GitHub](https://github.com/open-meteo/open-meteo).

Please follow the [quick start notebook](open_meteo_quick_start.ipynb) in order to understand how to easily get started.
#### Licence
- Open-Meteo APIs are free for non-commercial use. The access is not restricted, but it is asked for fair use.
- All data is provided as is without any warranty.

API data are offered under [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

You must include a link next to any location, Open-Meteo data are displayed like:

`<a href="https://open-meteo.com/">Weather data by Open-Meteo.com</a>
`


## How to contribute?

We welcome any suggestions, problem reports, and contributions!
For any changes you would like to make to this project, we invite you to submit an [issue](https://github.com/stavrostheocharis/weather_data_retriever/issues).

For more information, see [`CONTRIBUTING`](https://github.com/stavrostheocharis/weather_data_retriever/blob/main/CONTRIBUTING.md) instructions.

## References

1. [How To Create a Python Package for Fetching Weather Data](https://medium.com/towards-artificial-intelligence/how-to-create-a-python-package-for-fetching-weather-data-b17614627f30)

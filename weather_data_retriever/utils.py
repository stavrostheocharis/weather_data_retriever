import pandas as pd
from geopy.geocoders import Nominatim
import requests
from datetime import datetime
import json
from typing import Tuple, List, Dict, Union, Literal


def get_location_from_name(
    name: str, use_bound_box: bool = False
) -> Tuple[str, Tuple[float, float]]:
    nom_loc = Nominatim(user_agent="weather_data_retriever")
    try:
        location = nom_loc.geocode(name)
        if use_bound_box:
            coordinates = location.raw["boundingbox"]
            # Coordinates has sorted the values as [latmin, latmax, lonmin, lonmax]
            return location[0], tuple(coordinates)

        else:
            return location[0], location[1]

    except Exception as e:
        raise ValueError("Error in finding Area & Coordinates.", e)


def format_date_for_larc_power(
    start_date: str,
    end_date: str,
    aggregation: Literal["hourly", "daily", "monthly", "climatology"],
) -> Tuple[str, str]:
    """
    Formats the dates based on the aggregation in order to be ready to be used in Nasa weather request
    """

    if aggregation not in ["hourly", "daily", "monthly", "climatology"]:
        raise ValueError("Invalid aggregation value")

    if (aggregation == "monthly") | (aggregation == "climatology"):
        mod_start_date = start_date[0:4]
        mod_end_date = end_date[0:4]
    else:
        mod_start_date = start_date.replace("-", "")
        mod_end_date = end_date.replace("-", "")

    return mod_start_date, mod_end_date


def convert_str_hour_date_to_datetime(str_hour_date: str) -> datetime:
    """Concerts str hour (eg. "2022050501) to datetime"""
    return datetime.strptime(str_hour_date, "%Y%m%d%H")


def convert_response_larc_power_dict_to_dataframe(
    response_dict: Dict[str, Dict[str, float]], aggregation: str
) -> pd.DataFrame:
    """
    Converts coming dict from response to dataframe based on aggregation
    """

    weather_df = pd.DataFrame(response_dict).reset_index()
    coming_columns = list(response_dict.keys())
    weather_df.columns = ["date"] + coming_columns

    if aggregation == "daily":
        weather_df["date"] = pd.to_datetime(weather_df["date"])
    elif aggregation == "hourly":
        weather_df["date"] = weather_df.apply(
            lambda x: convert_str_hour_date_to_datetime(x["date"]), axis=1
        )
        weather_df["date"] = pd.to_datetime(weather_df["date"])

    return weather_df


def adjust_coordinates_on_limitations(
    longitude_max: Union[float, str], longitude_min: Union[float, str]
) -> str:
    """
    Check if a the max and min values have more than 10 points diff.
    If yes adjust it beacuse the weather API has limitations.
    """
    if float(longitude_max) > float(longitude_min) + 10:
        longitude_max = float(longitude_min) + 10

    return str(longitude_max)


def get_larc_power_weather_data(
    start_date: str,
    end_date: str,
    coordinates: Union[Tuple[float, float], Tuple[float, float, float, float]],
    aggregation: Literal["hourly", "daily", "monthly", "climatology"] = "daily",
    community: Literal["AG", "RE", "SB"] = "RE",
    regional: bool = False,
    variables: List[str] = [
        "T2M",
        "T2MDEW",
        "T2MWET",
        "TS",
        "T2M_RANGE",
        "T2M_MAX",
        "T2M_MIN",
        "RH2M",
        "PRECTOT",
        "WS2M",
        "ALLSKY_SFC_SW_DWN",
    ],
) -> Union[pd.DataFrame, Dict[str, Dict[str, float]]]:
    """
    This function retrieves NASA's historical weather data at a location point
    Args:
        start_date: Starting date to retrieve data (eg. "2021-05-04)
        end_date: Ending date to retrieve data (eg. "2021-06-07)
        coordinates: Coordinated of the desired location (eg. (latitude, longtitude))
        aggregation: The aggregation that the data will have. Possible values are:
            "hourly": Provides parameters by hour with average values
            "daily": Provides parameters by day with average, maximum, and/or minimum values
            "monthly": Provides parameters by year; the annual and each month's average, maximum, and/or minimum values
            "climatology": Provides parameters as climatologies for a pre-defined period with monthly average, maximum, and/or minimum values available

        community: There are supported 3 communities:
            "AG": The Agroclimatology (AG) solar and meteorological parameters are available as daily mean time series formats.
                  All parameters are provided on the original resolution grid, which is dependent on the parameter
            "RE": The Renewable Energy (RE) solar and meteorological parameters are available as climatologically and inter-annual (monthly and annual) averaged values,
                  as well as in a daily time series format for user selected grids. All RE parameters are provided on the original resolution grid, which is dependent
                  on the parameter. The monthly and annually averaged parameters are provided as monthly and annual averaged values by year for each of the base solar
                  and meteorological data parameters.
            "SB": The Sustainable Buildings (SB) solar and meteorological parameters are available as climatologically, monthly, and annually average values, as well as in
                  a daily time series format. All parameters are provided on the original resolution grid, which is dependent on the parameter. The climatologically averaged
                  parameters are calculated to support the preliminary design and site selection for building projects. Monthly and annually averaged parameters are provided
                  as monthly and annual averaged values by year.

        variables: The variables to be returned:
            "T2M: Temperature at 2 Meters (°C)"
            "T2MDEW: Dew/Frost Point at 2 Meters (°C)"
            "T2MWET: Wet Bulb Temperature at 2 Meters (°C)"
            "TS: Earth Skin Temperature (°C)"
            "T2M_RANGE: Temperature at 2 Meters Range (°C)"
            "T2M_MAX: Temperature at 2 Meters Maximum (°C)"
            "T2M_MIN: Temperature at 2 Meters Minimum (°C)"
            "RH2M: Relative Humidity at 2 Meters (%)"
            "PRECTOTCORR: Precipitation Corrected (mm/day)"
            "WS2M: Wind Speed at 2 Meters (m/s)"
            "ALLSKY_SFC_SW_DWN: All Sky Surface Shortwave Downward Irradiance (kW-hr/m^2/day)"

    Returns:
        pd.DataFrame: weather data for the requested time period
    """

    if aggregation not in ["hourly", "daily", "monthly", "climatology"]:
        raise ValueError("Invalid aggregation value")

    if community not in ["AG", "RE", "SB"]:
        raise ValueError("Invalid community value")

    # Basic modifications
    formatted_variables = ",".join(variables)
    mod_start_date, mod_end_date = format_date_for_larc_power(
        start_date, end_date, aggregation
    )

    if regional:
        base_url = r"https://power.larc.nasa.gov/api/temporal/{aggregation}/regional?parameters={parameters}&community={community}&latitude-min={latitude_min}&latitude-max={latitude_max}&longitude-min={longitude_min}&longitude-max={longitude_max}&start={start}&end={end}&format=JSON"
        latitude_min = coordinates[0]
        longitude_min = coordinates[2]
        latitude_max = coordinates[1]
        longitude_max = coordinates[3]
        longitude_max = adjust_coordinates_on_limitations(longitude_max, longitude_min)

        api_request_url = base_url.format(
            latitude_min=latitude_min,
            longitude_min=longitude_min,
            latitude_max=latitude_max,
            longitude_max=longitude_max,
            start=mod_start_date,
            end=mod_end_date,
            aggregation=aggregation,
            community=community,
            parameters=formatted_variables,
        )
    else:
        base_url = r"https://power.larc.nasa.gov/api/temporal/{aggregation}/point?parameters={parameters}&community={community}&longitude={longitude}&latitude={latitude}&start={start}&end={end}&format=JSON"
        latitude = coordinates[0]
        longitude = coordinates[1]
        api_request_url = base_url.format(
            longitude=longitude,
            latitude=latitude,
            start=mod_start_date,
            end=mod_end_date,
            aggregation=aggregation,
            community=community,
            parameters=formatted_variables,
        )

    try:
        response = requests.get(url=api_request_url, verify=True, timeout=30.00)
    except Exception as e:
        print("There is an error with the Nasa weather API. The error is: ", e)
    content = json.loads(response.content.decode("utf-8"))
    if len(content["messages"]) > 0:
        raise InterruptedError(content["messages"])

    if regional:
        return content
    else:
        selected_content_dict = content["properties"]["parameter"]
        weather_df = convert_response_larc_power_dict_to_dataframe(
            selected_content_dict, aggregation
        )
        return weather_df


def build_meteo_request_url(
    aggregation: Literal["hourly", "daily"],
    parameters_str: str,
    longitude: float,
    latitude: float,
    case: Literal["forecast", "historical"],
    start_date: Union[str, None],
    end_date: Union[str, None],
) -> str:

    if case == "historical":
        base_forecast_url = r"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&{aggregation}={parameters_str}&timeformat=unixtime&timezone=auto"
        api_forecast_request_url = base_forecast_url.format(
            aggregation=aggregation,
            parameters_str=parameters_str,
            longitude=longitude,
            latitude=latitude,
            start_date=start_date,
            end_date=end_date,
        )
    else:
        base_forecast_url = r"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&{aggregation}={parameters_str}&timeformat=unixtime&timezone=auto"
        api_forecast_request_url = base_forecast_url.format(
            aggregation=aggregation,
            parameters_str=parameters_str,
            longitude=longitude,
            latitude=latitude,
        )

    return api_forecast_request_url


l_power_base_vars_to_fetch = [
    "T2M",
    "T2MDEW",
    "T2MWET",
    "TS",
    "RH2M",
    "PRECTOT",
    "WS2M",
    "ALLSKY_SFC_SW_DWN",
]

l_power_additional_vars_to_fetch = [
    "T2M_RANGE",
    "T2M_MAX",
    "T2M_MIN",
]


def choose_meteo_default_variables(
    aggregation: Literal["hourly", "daily"], case: Literal["forecast", "historical"]
) -> List[str]:
    if aggregation == "hourly":
        default_variables = [
            "temperature_2m",
            "relativehumidity_2m",
            "dewpoint_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "snowfall",
        ]

        if case == "forecast":
            default_variables.append("showers")
    else:
        default_variables = [
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "sunrise",
            "precipitation_sum",
            "rain_sum",
        ]

        if case == "forecast":
            default_variables.extend(["showers_sum", "snowfall_sum"])

    return default_variables


def get_open_meteo_weather_data(
    coordinates: Tuple[float, float],
    aggregation: Literal["hourly", "daily"],
    case: Literal["forecast", "historical"],
    parameters: List[str] = ["default"],
    start_date: Union[str, None] = None,
    end_date: Union[str, None] = None,
) -> Tuple[
    pd.DataFrame, Dict[str, Union[str, float, Dict[str, Union[List[str], List[float]]]]]
]:
    """
    This function retrieves open-meteo historical or forecasted weather data at a location point

    Args:
        coordinates: Coordinated of the desired location (eg. (latitude, longtitude))
        aggregation: The aggregation that the data will have. Possible values are:
            "hourly": Provides parameters by hour with average values
            "daily": Provides parameters by day with average, min, or max values
        case: Choose if the requested data will be historical or forecasts
        variables: The variables to be returned:
            "temperature_2m: Temperature at 2 Meters (°C)"
            "temperature_2m_max: Maximum daily air temperature at 2 meters above ground (°C)"
            "temperature_2m_min: Minimum daily air temperature at 2 meters above ground (°C)"
            "apparent_temperature: Apparent temperature (°C)"
            "apparent_temperature_max: Maximum daily apparent temperature (°C)"
            "apparent_temperature_min: Minimum daily apparent temperature (°C)"
            "relativehumidity_2m: Relative humidity at 2 meters above ground (%)"
            "dewpoint_2m: Dew point temperature at 2 meters above ground (°C)"
            "sunrise: Time of sunrise"
            "precipitation: Total precipitation (rain, showers, snow) sum of the preceding hour (mm)"
            "precipitation_sum: Total precipitation sum (rain, showers, snow) (mm)"
            "rain_sum: 	Rain from large scale weather systems of the preceding hour in millimeter"
            "snowfall: Snowfall amount of the preceding hour in centimeters"
            "showers: Showers from convective precipitation in millimeters from the preceding hour"
            "showers_sum: Showers sum from convective precipitation in millimeters"
            "snowfall_sum: Snowfall sum amount in centimeters"
        start_date: Starting date to retrieve data (eg. "2021-11-27)
        end_date: Ending date to retrieve data (eg. "2021-12-07)

    Returns:
        pd.DataFrame: weather data for the requested time period
        Dict: The coming dictionary directly from the request
    """

    parameters_str = ",".join(parameters)
    latitude = coordinates[0]
    longitude = coordinates[1]
    api_forecast_request_url = build_meteo_request_url(
        aggregation=aggregation,
        parameters_str=parameters_str,
        longitude=longitude,
        latitude=latitude,
        case=case,
        start_date=start_date,
        end_date=end_date,
    )

    try:
        response = requests.get(
            url=api_forecast_request_url, verify=True, timeout=30.00
        )
    except:
        raise ConnectionAbortedError("Failed to establish connection")

    content = json.loads(response.content.decode("utf-8"))
    weather_data_df = pd.DataFrame(content[aggregation])
    weather_data_df["time"] = weather_data_df.apply(
        lambda x: pd.to_datetime(x["time"], unit="s"), axis=1
    )

    return weather_data_df, content

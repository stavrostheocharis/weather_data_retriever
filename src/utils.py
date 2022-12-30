import pandas as pd
from geopy.geocoders import Nominatim
import requests
from datetime import datetime
import json
from typing import Tuple, List, Dict, Union, Literal


def get_location_from_name(
    name: str, use_bound_box: bool = False
) -> Tuple[str, Tuple[float, float]]:
    nom_loc = Nominatim(user_agent="envio")
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


def format_date_for_nasa(
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


def convert_response_dict_to_dataframe(
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


def get_nasa_weather_data(
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
    This function retrieves NASA's historical weather data at a point
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
    mod_start_date, mod_end_date = format_date_for_nasa(
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

    if regional:
        return content
    else:
        selected_content_dict = content["properties"]["parameter"]
        weather_df = convert_response_dict_to_dataframe(
            selected_content_dict, aggregation
        )
        return weather_df

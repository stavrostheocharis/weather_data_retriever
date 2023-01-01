from weather_data_retriever.utils import get_location_from_name, get_nasa_weather_data
from typing import Tuple, List, Dict, Union, Literal

base_variables_to_fetch = [
    "T2M",
    "T2MDEW",
    "T2MWET",
    "TS",
    "RH2M",
    "PRECTOT",
    "WS2M",
    "ALLSKY_SFC_SW_DWN",
]

additional_variables_to_fetch = [
    "T2M_RANGE",
    "T2M_MAX",
    "T2M_MIN",
]


def fetch_historical_weather_data(
    location_name: str,
    start_date,
    end_date,
    aggregation: Literal["hourly", "daily", "monthly", "climatology"] = "daily",
    community: Literal["AG", "RE", "SB"] = "RE",
    regional: bool = False,
    use_bound_box: bool = False,
    variables_to_fetch: List[str] = ["default"],
):
    location, coordinates = get_location_from_name(location_name, use_bound_box)
    if variables_to_fetch == ["default"]:
        if aggregation == "hourly":
            variables_to_fetch = base_variables_to_fetch
        else:
            variables_to_fetch = base_variables_to_fetch + additional_variables_to_fetch

    return get_nasa_weather_data(
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        community=community,
        regional=regional,
        coordinates=coordinates,
        variables=variables_to_fetch,
    )

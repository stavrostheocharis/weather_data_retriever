from weather_data_retriever.utils import (
    get_location_from_name,
    get_larc_power_weather_data,
    l_power_base_vars_to_fetch,
    l_power_additional_vars_to_fetch,
    get_open_meteo_weather_data,
    choose_meteo_default_variables,
)
from typing import Tuple, List, Dict, Union, Literal
import pandas as pd


def fetch_larc_power_historical_weather_data(
    location_name: str,
    start_date,
    end_date,
    aggregation: Literal["hourly", "daily", "monthly", "climatology"] = "daily",
    community: Literal["AG", "RE", "SB"] = "RE",
    regional: bool = False,
    use_bound_box: bool = False,
    variables_to_fetch: List[str] = ["default"],
) -> Union[pd.DataFrame, Dict[str, Dict[str, float]]]:

    location, coordinates = get_location_from_name(location_name, use_bound_box)
    if variables_to_fetch == ["default"]:
        if aggregation == "hourly":
            variables_to_fetch = l_power_base_vars_to_fetch
        else:
            variables_to_fetch = (
                l_power_base_vars_to_fetch + l_power_additional_vars_to_fetch
            )

    return get_larc_power_weather_data(
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        community=community,
        regional=regional,
        coordinates=coordinates,
        variables=variables_to_fetch,
    )


def fetch_open_meteo_weather_data(
    location_name: str,
    aggregation: Literal["hourly", "daily"],
    case: Literal["forecast", "historical"],
    variables_to_fetch: List[str] = ["default"],
    start_date: Union[str, None] = None,
    end_date: Union[str, None] = None,
) -> Tuple[
    pd.DataFrame, Dict[str, Union[str, float, Dict[str, Union[List[str], List[float]]]]]
]:
    location, coordinates = get_location_from_name(location_name, use_bound_box=False)
    if "default" in variables_to_fetch:
        parameters = choose_meteo_default_variables(aggregation=aggregation, case=case)
    else:
        parameters = variables_to_fetch

    return get_open_meteo_weather_data(
        start_date=start_date,
        end_date=end_date,
        aggregation=aggregation,
        coordinates=coordinates,
        parameters=parameters,
        case=case,
    )

class weather_data_retriever:
    def __init__(self):

        from src.utils import get_location_from_name, get_nasa_weather_data
        import pandas as pd
        from geopy.geocoders import Nominatim
        import requests
        from datetime import datetime
        import json
        from typing import Tuple, List, Dict, Union, Literal

        self.default_variables_to_fetch = [
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
        ]

        def fetch_historical_weather_data(
            self,
            location_name: str,
            start_date,
            end_date,
            aggregation: Literal["hourly", "daily", "monthly", "climatology"] = "daily",
            community: Literal["AG", "RE", "SB"] = "RE",
            regional: bool = False,
            use_bound_box: bool = False,
            variables_to_fetch: List[str] = self.default_variables_to_fetch,
        ):
            location, coordinates = get_location_from_name(location_name, use_bound_box)

            return get_nasa_weather_data(
                start_date=start_date,
                end_date=end_date,
                aggregation=aggregation,
                community=community,
                regional=regional,
                coordinates=coordinates,
                variables=variables_to_fetch,
            )

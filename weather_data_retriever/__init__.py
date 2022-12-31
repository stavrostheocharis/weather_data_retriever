import os
import sys

fpath = os.path.join(os.path.dirname(__file__), "src")
sys.path.append(fpath)

from src.pipelines import fetch_historical_weather_data

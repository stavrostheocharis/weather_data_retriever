import os
import sys

fpath = os.path.join(os.path.dirname(__file__), "src")
sys.path.append(fpath)
print(sys.path)

from pipelines import fetch_historical_weather_data

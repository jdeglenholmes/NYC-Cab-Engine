from enum import Enum
import pandas as pd
import requests

# Define class containing valid journey_type 
# Rationale: updatable structure, compatable with isinstance()
class JourneyType(Enum):
    YELLOW = "yellow"
    GREEN = "green"
    FHV = "fhv"
    FHVHV = "fhvhv"

def fetch_taxi_data(
        journey_type: JourneyType = JourneyType.YELLOW,
        year: int = 2025,
        month: int = 10
        ) -> str:
    """
    Fetch a DataFrame containing NYC taxi journeys based on variables: journey_type, year, month.
        
        :param journey_type: type of journey available for download by NYC Taxi & Limousine Commission (TLC)
        :param year:  year value to filter TLC dataset by
        :param month: month value to filter TLC dataset by
 
    Returns a DataFrame.
    """

    # 1. Error handling
    if not isinstance(journey_type, JourneyType):
        valid_journeys = [j.value for j in JourneyType]
        raise TypeError(f"journey_type must be a valid JourneyType: {valid_journeys}")
              
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError(f"year and month must be integers.")

    month_str = str(month).zfill(2) # Convert to str and pad with leading zero
    
    # 2. Compile URL
    download_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{journey_type.value}_tripdata_{year}-{month_str}.parquet"
    
    # 3. Check if file exits on the sever
    response = requests.head(download_url)

    if response.status_code == 403 or response.status_code == 404:
        print(f"⚠️ Data not available for {journey_type.value} in {month}/{year}")
        print(f"Status Code: {response.status_code} (URL: {download_url})")
        return None

    print(f"✅ File found! Downloading {download_url}...")
    df = pd.read_parquet(download_url)

    return df


# How to call it:
# url = fetch_taxi_data(
#   journey_type = JourneyType.YELLOW, # Use class values
#   year = 2026,
#   month = 1
# )
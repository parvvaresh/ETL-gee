import ee
from calculate_interval_mean import *

def transform_sentinel2(aoi: ee.Geometry, start_date: str, end_date: str, interval_days: int, collectionS2: ee.ImageCollection, collectionS1: ee.ImageCollection) -> ee.ImageCollection:
    """
    Transform Sentinel-2 and Sentinel-1 data into aggregated intervals.

    This function processes Sentinel-2 and Sentinel-1 collections by aggregating them
    over a specified time interval. It calculates mean images for each interval, adds
    spectral indices and auxiliary data (terrain and MODIS LST), and combines the results
    into a single ImageCollection.

    Parameters:
    - aoi (ee.Geometry): 
        Area of interest in Earth Engine Geometry format.
    - start_date (str): 
        Start date for data processing in 'YYYY-MM-DD' format.
    - end_date (str): 
        End date for data processing in 'YYYY-MM-DD' format.
    - interval_days (int): 
        The duration of each time interval in days.
    - collectionS2 (ee.ImageCollection): 
        Pre-filtered Sentinel-2 image collection.
    - collectionS1 (ee.ImageCollection): 
        Pre-filtered Sentinel-1 image collection.

    Returns:
    - ee.ImageCollection: 
        A collection of images where each image represents aggregated data for one interval,
        including Sentinel-2 and Sentinel-1 bands, spectral indices, terrain data, and MODIS LST.
    """
    # Convert start_date and end_date to ee.Date objects
    start_date = ee.Date(start_date)
    end_date = ee.Date(end_date)

    # Calculate the number of intervals
    num_intervals = end_date.difference(start_date, 'day').subtract(interval_days).divide(interval_days).int().getInfo()

    # Initialize a list to store interval mean images
    interval_means = []

    # Iterate through the intervals and calculate mean images
    for i in range(num_intervals):
        # Define the start date for the current interval
        start = start_date.advance(i * interval_days, 'day')

        # Calculate the mean image for the current interval
        interval_mean = calculate_interval_mean(start, interval_days, collectionS2, collectionS1, aoi)

        # Append the calculated mean image to the list
        interval_means.append(interval_mean)

    # Combine the interval images into a single ImageCollection and convert to bands
    return ee.ImageCollection(interval_means).toBands().toFloat()

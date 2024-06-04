# Gee get data

## Overview

The `gee` library is a Python package designed for processing and analyzing Sentinel-1 and Sentinel-2 satellite imagery using Google Earth Engine (GEE). It allows for the loading, processing, and combining of Sentinel-1 and Sentinel-2 data, as well as the calculation of various vegetation indices. Additionally, it supports exporting the processed data to Google Drive.

## Installation

Before using the `gee` library, you need to set up the Google Earth Engine Python API. Follow the official installation guide [here](https://developers.google.com/earth-engine/guides/python_install).

## Usage

Here's a step-by-step guide on how to use the `gee` library.

### 1. Import the Library

```python
import ee
from gee import gee

# Initialize the Earth Engine library
ee.Initialize()
ee.Initialize(project='name of project')
```


### 2. Clone form github

This code can only be used in Google Colab

```python
!git clone https://github.com/parvvaresh/google-earth-engine
%cd google-earth-engine

from get_data.gee import gee
```
### 3. Define the Area of Interest (AOI)

You need to define your area of interest (AOI) as an `ee.Geometry`. For example, to define a rectangular AOI:

```python
aoi = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax])
```

### 4. Create an Instance of the `gee` Class

```python
gee_instance = gee(aoi)
```

Optionally, you can provide a `table_clip` parameter if you want to clip the results to a specific geometry.

### 5. Run the Data Pipeline

Call the `pipeline_data` method with the required parameters to process and export the data:

```python
gee_instance.pipeline_data(
    start_date='YYYY-MM-DD',  # Start date of the data collection period
    end_date='YYYY-MM-DD',    # End date of the data collection period
    name_file='exported_data',  # Name of the exported file
    name_folder='GEE_exports'  # Name of the folder in Google Drive where the file will be saved
)
```

### Example Usage

```python
import ee
from gee import gee

# Initialize the Earth Engine library
ee.Initialize()
ee.Initialize(project='name of project')


!git clone https://github.com/parvvaresh/google-earth-engine
%cd google-earth-engine

from get_data.gee import gee

# Define your AOI (example coordinates)
aoi = ee.Geometry.Rectangle([-10, 35, 10, 45])

# Create an instance of the gee class
gee_instance = gee(aoi)

# Run the data pipeline
gee_instance.pipeline_data(
    start_date='2023-01-01',
    end_date='2023-01-31',
    name_file='sentinel_data',
    name_folder='GEE_exports'
)
```

## Methods

### `_load_Sentinel1(self, start_date: str, end_date: str) -> None`

Loads the Sentinel-1 ImageCollection within the specified date range and AOI.

### `_process_Sentinel1(self) -> None`

Processes the loaded Sentinel-1 data, including filtering and creating mosaics based on ascending and descending orbit passes.

### `_load_Sentinel2(self, start_date: str, end_date: str, cloudy_pixel: int) -> None`

Loads the Sentinel-2 ImageCollection within the specified date range, AOI, and cloud cover percentage.

### `_process_Sentinel2(self, interval: int, start_date: str, end_date: str) -> None`

Processes the loaded Sentinel-2 data, creating composites at specified intervals and calculating NDVI, EVI, and SAVI indices.

### `_combine_sentinel1_sentinel2(self) -> None`

Combines the processed Sentinel-1 and Sentinel-2 data into a single dataset and clips it if a `table_clip` is provided.

### `_export_data(self, name_file: str, name_folder: str) -> None`

Exports the processed and combined data to Google Drive as a CSV file.

### `pipeline_data(self, start_date: str, end_date: str, name_file: str, name_folder: str) -> None`

Runs the entire data pipeline, from loading and processing Sentinel-1 and Sentinel-2 data to exporting the results.

## Notes

- Ensure that you have sufficient permissions and quota in your Google Earth Engine account to run the processing tasks.
- The export task may take some time depending on the size of the AOI and the date range specified.

## License

This code is provided under the MIT License. Feel free to use and modify it as needed.

---

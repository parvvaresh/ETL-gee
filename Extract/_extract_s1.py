import ee


def extract_Sentinel1(aoi: ee.Geometry, start_date: str, end_date: str) -> ee.ImageCollection:
    """
    Extract Sentinel-1 radar data within a specified area and time range.

    This function retrieves Sentinel-1 Ground Range Detected (GRD) data from the 
    'COPERNICUS/S1_GRD' collection. The images are filtered based on the specified 
    area of interest (AOI) and date range. The function selects polarization bands 
    suitable for analysis: Vertical-Vertical (VV) and Vertical-Horizontal (VH) polarizations.

    Parameters:
    - aoi (ee.Geometry): Area of interest in Earth Engine Geometry format.
    - start_date (str): Start date for data extraction in 'YYYY-MM-DD' format.
    - end_date (str): End date for data extraction in 'YYYY-MM-DD' format.

    Returns:
    - ee.ImageCollection: A collection of Sentinel-1 radar images with selected polarization bands.

    Raises:
    - ValueError: If no images are available for the specified parameters.

    Notes:
    - Sentinel-1 provides radar data, which is unaffected by cloud cover, making it useful 
      for all-weather monitoring.
    - The selected bands:
      - VV (Vertical transmit and Vertical receive): Useful for surface water and urban mapping.
      - VH (Vertical transmit and Horizontal receive): Sensitive to vegetation structure.
    """
    sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
                .filterDate(start_date, end_date) \
                .filterBounds(aoi) \
                .select(['VV', 'VH'])
    
    if sentinel1.size().getInfo() == 0:
        raise ValueError("Sentinel-1 collection is empty. Check your date range or AOI.")
    
    return sentinel1


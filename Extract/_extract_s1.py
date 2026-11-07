import ee

# Polarisation bands kept from Sentinel-1.
S1_BANDS = ['VV', 'VH']


def extract_Sentinel1(aoi: ee.Geometry, start_date: str, end_date: str) -> ee.ImageCollection:
    """
    Extract Sentinel-1 GRD radar data (VV and VH, in dB) within a specified area and time range.

    Only Interferometric Wide (IW) swath scenes that actually contain both VV and VH
    are kept; otherwise selecting 'VH' fails on single-polarisation scenes.

    Parameters:
    - aoi (ee.Geometry): Area of interest.
    - start_date (str): Start date, 'YYYY-MM-DD' (inclusive).
    - end_date (str): End date, 'YYYY-MM-DD' (exclusive).

    Returns:
    - ee.ImageCollection: Sentinel-1 images with the bands in S1_BANDS.

    Raises:
    - ValueError: If no images match the parameters.
    """
    sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi) \
        .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
        .select(S1_BANDS)

    if sentinel1.size().getInfo() == 0:
        raise ValueError("Sentinel-1 collection is empty. Check your date range or AOI.")

    return sentinel1

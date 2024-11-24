import ee


def extract_Sentinel1(aoi : ee.Geometry, start_date : str, end_date : str) -> ee.ImageCollection:
    """
      Extract Sentinel-1 radar data.
    """
    sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
                .filterDate(start_date, end_date) \
                .filterBounds(aoi) \
                .select(['VV', 'VH'])
    
    if sentinel1.size().getInfo() == 0:
        raise ValueError("Sentinel-1 collection is empty. Check your date range or AOI.")
    
    return sentinel1

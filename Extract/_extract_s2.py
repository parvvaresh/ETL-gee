import ee


import ee

def s2_clear_sky(image: ee.Image) -> ee.Image:
    """
    Masks clear sky pixels in a Sentinel-2 image using the SCL band.

    Parameters:
    - image (ee.Image): Sentinel-2 image containing the 'SCL' band.

    Returns:
    - ee.Image: Sentinel-2 image masked for clear sky pixels, scaled to reflectance values.
    """
    scl = image.select('SCL')    
    clear_sky_pixels = scl.eq(4).Or(scl.eq(5)).Or(scl.eq(6)).Or(scl.eq(11))    
    return image.updateMask(clear_sky_pixels).divide(10000).copyProperties(image, ["system:time_start"])


def extract_Sentinel2(aoi: ee.Geometry, start_date: str, end_date: str) -> ee.ImageCollection:
    """
    Extract Sentinel-2 surface reflectance data within a specified area and time range.

    This function retrieves Sentinel-2 data from the Harmonized Sentinel-2 Surface Reflectance collection 
    ('COPERNICUS/S2_SR_HARMONIZED'). It filters the data based on the specified area of interest (AOI), 
    date range, and a cloud coverage threshold. The function applies a clear sky mask using the SCL (Scene 
    Classification Layer) band to retain only high-quality pixels and selects key spectral bands for analysis.

    Parameters:
    - aoi (ee.Geometry): Area of interest in Earth Engine Geometry format.
    - start_date (str): Start date for data extraction in 'YYYY-MM-DD' format.
    - end_date (str): End date for data extraction in 'YYYY-MM-DD' format.

    Returns:
    - ee.ImageCollection: A collection of Sentinel-2 images with clear sky pixels and selected spectral bands.

    Raises:
    - ValueError: If no images are available for the specified parameters.

    Notes:
    - The selected bands include: B1 (Coastal aerosol), B2 (Blue), B3 (Green), B4 (Red), 
      B5–B7 (Vegetation Red Edge), B8 (NIR), B8A (Narrow NIR), B9 (Water vapor), B11 (SWIR1), 
      and B12 (SWIR2).
    - Cloudy pixels are filtered using the CLOUDY_PIXEL_PERCENTAGE metadata.
    """
    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                .filterDate(start_date, end_date) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 100)) \
                .filterBounds(aoi) \
                .map(s2_clear_sky) \
                .select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12'])
    
    if sentinel2.size().getInfo() == 0:
        raise ValueError("Sentinel-2 collection is empty. Check your date range or AOI.")
    
    return sentinel2

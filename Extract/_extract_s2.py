import ee

# Reflectance bands kept from Sentinel-2 (SCL is only used for masking).
S2_BANDS = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']

# SCL classes treated as clear sky: 4 = vegetation, 5 = bare soil, 6 = water, 11 = snow/ice.
CLEAR_SKY_CLASSES = [4, 5, 6, 11]


def s2_clear_sky(image: ee.Image) -> ee.Image:
    """
    Mask non clear-sky pixels of a Sentinel-2 image using its SCL band and
    scale the reflectance bands to [0, 1].

    Parameters:
    - image (ee.Image): Sentinel-2 SR image containing the 'SCL' band.

    Returns:
    - ee.Image: Reflectance bands (S2_BANDS), masked to clear-sky pixels and divided by 10000.
    """
    scl = image.select('SCL')
    clear_sky = scl.remap(CLEAR_SKY_CLASSES, [1] * len(CLEAR_SKY_CLASSES), 0)
    reflectance = image.select(S2_BANDS).updateMask(clear_sky).divide(10000)
    return ee.Image(reflectance.copyProperties(image, ['system:time_start']))


def extract_Sentinel2(aoi: ee.Geometry, start_date: str, end_date: str, cloudy_pixel: int = 100) -> ee.ImageCollection:
    """
    Extract Sentinel-2 surface reflectance data within a specified area and time range.

    Uses 'COPERNICUS/S2_SR_HARMONIZED', filtered by AOI, date range and the
    CLOUDY_PIXEL_PERCENTAGE metadata, then masked to clear-sky pixels with the SCL band.

    Parameters:
    - aoi (ee.Geometry): Area of interest.
    - start_date (str): Start date, 'YYYY-MM-DD' (inclusive).
    - end_date (str): End date, 'YYYY-MM-DD' (exclusive).
    - cloudy_pixel (int): Keep only scenes whose CLOUDY_PIXEL_PERCENTAGE is below this value (0-100).

    Returns:
    - ee.ImageCollection: Clear-sky Sentinel-2 images with the bands in S2_BANDS.

    Raises:
    - ValueError: If no images match the parameters.
    """
    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloudy_pixel)) \
        .map(s2_clear_sky)

    if sentinel2.size().getInfo() == 0:
        raise ValueError("Sentinel-2 collection is empty. Check your date range, AOI or cloudy_pixel threshold.")

    return sentinel2

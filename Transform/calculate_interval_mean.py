import ee

from Extract._extract_s1 import S1_BANDS
from Extract._extract_s2 import S2_BANDS

MODIS_BANDS = ['Emis_32', 'Emis_31', 'LST_Day_1km', 'LST_Night_1km']


def _empty_image(bands: list) -> ee.Image:
    """A fully masked float image with the given band names (used when an interval has no data)."""
    return ee.Image.constant([0] * len(bands)).rename(bands).toFloat().updateMask(0)


def _reduce_or_empty(collection: ee.ImageCollection, bands: list, reducer: str = 'mean') -> ee.Image:
    """
    Reduce a collection to one image, or return a masked placeholder with the same bands
    if the collection is empty. This keeps the band structure identical for every interval,
    so later band math (NDVI, ...) and concatenation never fail on empty intervals.
    """
    reduced = collection.mean() if reducer == 'mean' else collection.median()
    return ee.Image(ee.Algorithms.If(collection.size().gt(0),
                                     reduced.toFloat(),
                                     _empty_image(bands)))


def _scale_modis(image: ee.Image) -> ee.Image:
    """Convert MOD11A1 integers to physical units: emissivity (unitless) and LST (Kelvin)."""
    emissivity = image.select(['Emis_32', 'Emis_31']).multiply(0.002).add(0.49)
    lst = image.select(['LST_Day_1km', 'LST_Night_1km']).multiply(0.02)
    return ee.Image(emissivity.addBands(lst).copyProperties(image, ['system:time_start']))


def add_indices(image: ee.Image) -> ee.Image:
    """
    Add spectral indices (NDVI, EVI, SAVI, BSI) as bands. Expects reflectance in [0, 1].
    """
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2'),
        }).rename('EVI')

    savi = image.expression(
        '((NIR - RED) / (NIR + RED + 0.5)) * 1.5', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
        }).rename('SAVI')

    bsi = image.expression(
        '((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))', {
            'SWIR': image.select('B11'),
            'RED': image.select('B4'),
            'NIR': image.select('B8'),
            'BLUE': image.select('B2'),
        }).rename('BSI')

    return image.addBands([ndvi, evi, savi, bsi])


def calculate_interval_mean(start: ee.Date, interval: int, collectionS2: ee.ImageCollection,
                            collectionS1: ee.ImageCollection, aoi: ee.Geometry) -> ee.Image:
    """
    Build one feature image for the interval [start, start + interval days).

    Bands (in order):
    - Sentinel-2 mean reflectance: S2_BANDS
    - Sentinel-1 mean backscatter (dB): VV, VH
    - Spectral indices: NDVI, EVI, SAVI, BSI
    - Terrain (GMTED2010): mea, min, max, slope
    - MODIS MOD11A1 median: Emis_32, Emis_31 (emissivity), LST_Day_1km, LST_Night_1km (Kelvin)

    Intervals with no Sentinel-2 / Sentinel-1 / MODIS images get masked bands instead of failing.

    Parameters:
    - start (ee.Date): Start date of the interval.
    - interval (int): Interval length in days.
    - collectionS2 (ee.ImageCollection): Output of the Extract phase (Sentinel-2).
    - collectionS1 (ee.ImageCollection): Output of the Extract phase (Sentinel-1).
    - aoi (ee.Geometry): Area of interest.

    Returns:
    - ee.Image: Float image clipped to the AOI.
    """
    end = start.advance(interval, 'day')

    s2 = _reduce_or_empty(collectionS2.filterDate(start, end).select(S2_BANDS), S2_BANDS)
    s1 = _reduce_or_empty(collectionS1.filterDate(start, end).select(S1_BANDS), S1_BANDS)

    merged = add_indices(s2.addBands(s1))

    # Terrain from GMTED2010 (static, identical for every interval).
    gmted = ee.Image('USGS/GMTED2010_FULL').select(['mea', 'min', 'max'])
    slope = ee.Terrain.slope(gmted.select('mea')).rename('slope')
    merged = merged.addBands(gmted.toFloat()).addBands(slope.toFloat())

    # MODIS LST / emissivity, converted from stored integers to physical units.
    modis_collection = ee.ImageCollection('MODIS/061/MOD11A1') \
        .filterDate(start, end) \
        .filterBounds(aoi) \
        .select(MODIS_BANDS) \
        .map(_scale_modis)
    modis = _reduce_or_empty(modis_collection, MODIS_BANDS, reducer='median')
    merged = merged.addBands(modis)

    return merged.toFloat().clip(aoi)

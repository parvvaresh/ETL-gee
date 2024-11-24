import ee

def calculate_interval_mean(start: ee.Date, interval: int, collectionS2: ee.ImageCollection, collectionS1: ee.ImageCollection, aoi: ee.Geometry) -> ee.Image:
    """
    Calculate the mean image for a given time interval from Sentinel-2 and Sentinel-1 collections.

    This function computes the temporal mean of Sentinel-2 and Sentinel-1 images for a specified
    time interval. It also enhances the merged dataset by adding spectral indices, terrain 
    information, and MODIS Land Surface Temperature (LST) data.

    Parameters:
    - start (ee.Date): The start date for the interval.
    - interval (int): The interval duration in days.
    - collectionS2 (ee.ImageCollection): Sentinel-2 image collection.
    - collectionS1 (ee.ImageCollection): Sentinel-1 image collection.
    - aoi (ee.Geometry): Area of interest in Earth Engine Geometry format.

    Returns:
    - ee.Image: An image with averaged bands from Sentinel-2 and Sentinel-1, spectral indices,
      terrain data, and MODIS LST bands clipped to the AOI.
    """
    # Compute the end date for the interval
    end = start.advance(interval, 'day')

    # Compute the mean image for Sentinel-2 within the interval
    filteredS2 = collectionS2.filterDate(start, end).mean().set('system:time_start', start.millis())

    # Compute the mean image for Sentinel-1 within the interval
    filteredS1 = collectionS1.filterDate(start, end).mean().set('system:time_start', start.millis())

    # Merge Sentinel-2 and Sentinel-1 bands
    mergedImage = filteredS2.addBands(filteredS1)

    # Function to add spectral indices (NDVI, EVI, SAVI, BSI)
    def add_indices(image: ee.Image) -> ee.Image:
        """
        Add spectral indices (NDVI, EVI, SAVI, BSI) as bands to the image.

        Parameters:
        - image (ee.Image): The input image.

        Returns:
        - ee.Image: The image with added spectral indices.
        """
        # Calculate NDVI
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

        # Calculate EVI
        evi = image.expression(
            '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
                'NIR': image.select('B8'),
                'RED': image.select('B4'),
                'BLUE': image.select('B2')
            }).rename('EVI')

        # Calculate SAVI
        savi = image.expression(
            '((NIR - RED) / (NIR + RED + 0.5)) * 1.5', {
                'NIR': image.select('B8'),
                'RED': image.select('B4')
            }).rename('SAVI')

        # Calculate BSI
        bsi = image.expression(
            '((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))', {
                'SWIR': image.select('B11'),
                'RED': image.select('B4'),
                'NIR': image.select('B8'),
                'BLUE': image.select('B2')
            }).rename('BSI')

        # Add indices as bands
        return image.addBands([ndvi, evi, savi, bsi])

    # Add spectral indices to the merged image
    mergedImage = add_indices(mergedImage)

    # Add elevation bands (mean, min, max) from GMTED2010 dataset
    gmted = ee.Image('USGS/GMTED2010_FULL').select(['mea', 'min', 'max']).clip(aoi)
    mergedImage = mergedImage.addBands(gmted)

    # Add slope derived from GMTED2010 mean elevation
    slope = ee.Terrain.slope(gmted.select('mea')).rename('slope').clip(aoi)
    mergedImage = mergedImage.addBands(slope)

    # Add MODIS Land Surface Temperature (LST) and emissivity bands
    modis = ee.ImageCollection('MODIS/061/MOD11A1') \
                .filterDate(start, end) \
                .filterBounds(aoi) \
                .median() \
                .select(['Emis_32', 'Emis_31', 'LST_Day_1km', 'LST_Night_1km'])
    mergedImage = mergedImage.addBands(modis)

    # Clip the final image to the AOI
    return mergedImage.clip(aoi)

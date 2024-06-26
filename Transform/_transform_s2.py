import ee

def transform_sentinel2(aoi: ee.Geometry,
                        sentinel2,
                        interval: int,
                        start_date: str,
                        end_date: str):
    increment = 'day'
    start = ee.Date(start_date)
    end = ee.Date(end_date)
    dates = ee.List.sequence(start.millis(), end.millis(), ee.Number(interval).multiply(1000 * 60 * 60 * 24))

    def make_sentinel2_composite(date):
        date = ee.Date(date)
        composite = sentinel2.filterDate(date, date.advance(interval, increment)).mean()
        return composite.clip(aoi).set('system:time_start', date.millis())

    SENTINEL2_10DAY = ee.ImageCollection.fromImages(dates.map(make_sentinel2_composite))
    filtered_collection = SENTINEL2_10DAY.filter(ee.Filter.listContains('system:band_names', 'B2'))

    def calculate_indices_and_clip(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        evi = image.expression('2.5 * ((NIR - Red) / (NIR + 6 * Red - 7.5 * Blue + 1))', {
                    'NIR': image.select('B8'),
                    'Red': image.select('B4'),
                    'Blue': image.select('B2')
                }).rename('EVI')
        savi = image.expression('((NIR - Red) / (NIR + Red + L)) * (1 + L)', {
                    'NIR': image.select('B8'),
                    'Red': image.select('B4'),
                    'L': 0.5
                }).rename('SAVI')
        # Concatenate original bands B1 to B12 with indices
        original_bands = image.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12'])
        indices_image = original_bands.addBands([ndvi, evi, savi])
        return indices_image.clip(aoi).copyProperties(image, image.propertyNames())

    indices_image = filtered_collection.map(calculate_indices_and_clip).toBands()
    return indices_image



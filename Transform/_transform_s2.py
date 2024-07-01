import ee

def transform_sentinel2(aoi : ee.Geometry,
                        extract_Sentinel2,
                        interval : int,
                        start_date : str,
                        end_date : str,
                        cloudy_pixel : int) -> ee.Image:


    start_date = ee.Date(start_date)
    end_date = ee.Date(end_date)

    def calculate_interval_mean(start, interval):

        end = start.advance(interval, 'day')
        filtered = extract_Sentinel2(aoi, start_date, end_date, cloudy_pixel)


        if filtered.size().getInfo() > 0:
            mean_image = filtered.mean().set('system:time_start', start.millis())
            return mean_image
        else:
            return None

    interval_means = []
    num_intervals = end_date.difference(start_date, 'day').divide(interval).int().getInfo()
    for i in range(num_intervals):
        start = start_date.advance(i * interval, 'day')
        interval_mean = calculate_interval_mean(start, interval)
        if interval_mean is not None:
            interval_means.append(interval_mean)

    interval_means_collection = ee.ImageCollection(interval_means)



    def calculate_indices_and_clip(image : ee.ImageCollection):
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
      return image.addBands([ndvi, evi, savi])



    def addGMTEDBands(image : ee.ImageCollection):
      gmted = ee.Image('USGS/GMTED2010_FULL') \
                .select(['mea', 'min', 'max']) \
                .clip(aoi)
      return image.addBands(gmted)

    def addModisBands(image : ee.ImageCollection):

      lst = ee.ImageCollection('MODIS/061/MOD11A1') \
                .filterDate(start_date, end_date) \
                .select(['LST_Day_1km', 'LST_Night_1km']) \
                .median() \
                .clip(aoi)
      return image.addBands(lst)

    def addSlope(image : ee.ImageCollection):
      gmted = ee.Image('USGS/GMTED2010_FULL') \
                .clip(aoi) \
                .select('mea')
      slope = ee.Terrain.slope(gmted)
      return image.addBands(slope)


    image_collection = interval_means_collection.map(calculate_indices_and_clip).map(addGMTEDBands).map(addModisBands).map(addSlope)
    return image_collection.toBands()
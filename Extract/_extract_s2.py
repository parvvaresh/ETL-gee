import ee

def extract_Sentinel2(aoi: ee.Geometry,
                    start_date: str,
                    end_date: str,
                    cloudy_pixel: int) -> None:

  sentinel2 = ee.ImageCollection('COPERNICUS/S2') \
            .filter(ee.Filter.lessThanOrEquals('CLOUDY_PIXEL_PERCENTAGE', cloudy_pixel)) \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date)

  if sentinel2.size().getInfo() == 0:
    raise ValueError("Sentinel-2 collection is empty. Check your date range or AOI.")

  return sentinel2
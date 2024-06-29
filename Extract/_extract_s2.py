import ee
import time


def mask_s2_clouds(image):
  """M
    asks clouds in a Sentinel-2 image using the QA band.
  """

  qa = image.select('QA60')

  cloud_bit_mask = 1 << 10
  cirrus_bit_mask = 1 << 11

  mask = (
        qa.bitwiseAnd(cloud_bit_mask).eq(0)
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    )
  return image.updateMask(mask).divide(10000)




def extract_Sentinel2(aoi: ee.Geometry,
                      start_date: str,
                      end_date: str,
                      cloudy_pixel: int) -> ee.ImageCollection:
  sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                .filter(ee.Filter.lessThanOrEquals('CLOUDY_PIXEL_PERCENTAGE', cloudy_pixel)) \
                .filterBounds(aoi) \
                .filterDate(start_date, end_date) \
                .map(mask_s2_clouds)

  if sentinel2.size().getInfo() == 0:
    raise ValueError("Sentinel-2 collection is empty. Check your date range or AOI.")

  return sentinel2
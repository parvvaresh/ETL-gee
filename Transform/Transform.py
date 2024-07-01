from ._transform_s1 import transform_sentinel1
from ._transform_s2 import transform_sentinel2
from .combine_transform_s1_s2 import combine_sentinel1_sentinel2
import ee


def Transform(aoi : ee.Geometry,
              sentinel1,
              extract_Sentinel2,
              interval: int,
              start_date: str,
              end_date: str,
              cloudy_pixel : int):


  stack_sentinel1 = transform_sentinel1(sentinel1)
  indices_image = transform_sentinel2(aoi, extract_Sentinel2, interval, start_date, end_date, cloudy_pixel)
  reduced_image = combine_sentinel1_sentinel2(aoi, indices_image , stack_sentinel1)

  return reduced_image

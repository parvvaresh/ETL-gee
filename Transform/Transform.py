from _transform_s1 import transform_sentinel1
from _transform_s2 import transform_sentinel2
from combine_transform_s1_s2 import combine_sentinel1_sentinel2
import ee


def Transform(aoi : ee.Geometry,
              table_clip,
              sentinel1,
              sentinel2,
              interval: int,
              start_date: str,
              end_date: str):


  stack_sentinel1 = transform_sentinel1(sentinel1)
  indices_image = transform_sentinel2(aoi, sentinel2, interval, start_date, end_date)
  reduced_image = combine_sentinel1_sentinel2(aoi, table_clip, indices_image , stack_sentinel1)

  return reduced_image

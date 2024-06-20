from _extract_s1 import extract_Sentinel1
from _extract_s2 import extract_Sentinel2
import ee


def extract(aoi: ee.Geometry,
         start_date: str,
         end_date: str,
         cloudy_pixel : int) -> dict:

  sentinel1 = extract_Sentinel1(
  aoi ,
  start_date,
  end_date)

  sentinel2 = extract_Sentinel1(
  aoi ,
  start_date,
  end_date,
  cloudy_pixel)


  return {
    "sentinel1" : sentinel1,
    "sentinel2" : sentinel2
  }
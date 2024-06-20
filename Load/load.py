from _load_s1 import _load_Sentinel1
from _load_s2 import _load_Sentinel2
import ee


def Load(aoi: ee.Geometry,
         start_date: str,
         end_date: str,
         cloudy_pixel : int) -> dict:

  sentinel1 = _load_Sentinel1(
  aoi ,
  start_date,
  end_date)

  sentinel2 = _load_Sentinel1(
  aoi ,
  start_date,
  end_date,
  cloudy_pixel)


  return {
    "sentinel1" : sentinel1,
    "sentinel2" : sentinel2
  }
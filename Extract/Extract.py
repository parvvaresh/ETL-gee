from ._extract_s1 import extract_Sentinel1
import ee


def Extract(aoi: ee.Geometry,
            start_date: str,
            end_date: str) -> list:


   sentinel1 = extract_Sentinel1(aoi, start_date, end_date)
   return sentinel1
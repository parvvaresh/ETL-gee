import ee

from Extract._extract_s2 import extract_Sentinel2
from Extract.Extract import Extract

from Transform.Transform import Transform
from Load.Load import Load

def gee(aoi : ee.Geometry,
        start_date: str,
        end_date: str,
        cloudy_pixel : int,
        interval: int,
        name_file: str,
        name_folder: str):


    sentinel1  = Extract(aoi,
         start_date,
         end_date,
         cloudy_pixel)

    print("Extracted Sentinel-1 and Sentinel-2 data.")


    reduced_image = Transform(aoi,
            sentinel1,
            extract_Sentinel2,
            interval,
            start_date,
            end_date,
            cloudy_pixel)
    print("Transformed Sentinel-1 and Sentinel-2 data.")



    Load(reduced_image,
      name_file,
      name_folder)

    print("Data saved to path.")

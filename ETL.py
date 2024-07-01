
from Extract._extract_s2 import Extract
from Extract.Extract import Extract

from Transform.Transform import Transform
from Load.Load import Load

import ee

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

  print("Extract s1 and s2")


  reduced_image = Transform(aoi,
            table_clip,
            sentinel1,
            sentinel2,
            interval,
            start_date,
            end_date)
  print("transforme s1 and s2")



  Load(reduced_image,
      name_file,
      name_folder)

  print("load data on path")


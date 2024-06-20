
from Extract.Extract import Extract
from Transform.Transform import Transform
from Load.Load import Load

import ee

def gee(aoi : ee.Geometry,
        table_clip : ee.Geometry,
        cloudy_pixel : int,
        interval: int,
        start_date: str,
        end_date: str,
        name_file: str,
        name_folder: str):


  sentinel1 , sentinel2 = Extract(aoi,
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


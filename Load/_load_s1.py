import ee

def _load_Sentinel1(aoi: ee.Geometry,
                    start_date: str,
                    end_date: str) -> None:


  sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
                    .filterDate(start_date, end_date) \
                    .filterBounds(aoi)

  if sentinel1.size().getInfo() == 0:
    raise ValueError("Sentinel-1 collection is empty. Check your date range or AOI.")


  return sentinel1
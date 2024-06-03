import ee
import time

class gee:


  def __init__(self,
                 aoi: ee.Geometry,
                 table_clip: ee.Geometry = None) -> None:

    self.aoi = aoi
    self.table_clip = table_clip

  def _load_Sentinel1(self, start_date: str, end_date: str) -> None:

    self.sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterDate(start_date, end_date) \
            .filterBounds(self.aoi)

    if self.sentinel1.size().getInfo() == 0:
      raise ValueError("Sentinel-1 collection is empty. Check your date range or AOI.")

  def _process_Sentinel1(self):
    vvIw = self.sentinel1.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')).select(['VV']) \
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
    vvIwAsc = vvIw.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
    vvIwDesc = vvIw.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))

    vhIw = self.sentinel1.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')).select(['VH']) \
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
    vhIwAsc = vhIw.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
    vhIwDesc = vhIw.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))

    def mosaic_by_date(imcol):
      def mosaic_for_date(date):
        date = ee.Date(date)
        mosaic = imcol.filterDate(date, date.advance(2, "day")).mosaic()
        return mosaic.set({
                    "system:time_start": date.millis(),
                    "system:id": date.format("YYYY-MM-dd")
                })

      dates = imcol.aggregate_array('system:time_start').distinct()
      return ee.ImageCollection(dates.map(mosaic_for_date))

    self.stack_sentinel1 = mosaic_by_date(vvIwAsc).toBands() \
            .addBands(mosaic_by_date(vhIwAsc).toBands()) \
            .addBands(mosaic_by_date(vvIwDesc).toBands()) \
            .addBands(mosaic_by_date(vhIwDesc).toBands())

  def _load_Sentinel2(self, start_date: str, end_date: str, cloudy_pixel: int) -> None:
    self.colsentinel2 = ee.ImageCollection('COPERNICUS/S2') \
            .filter(ee.Filter.lessThanOrEquals('CLOUDY_PIXEL_PERCENTAGE', cloudy_pixel)) \
            .filterBounds(self.aoi) \
            .filterDate(start_date, end_date)

    if self.colsentinel2.size().getInfo() == 0:
      raise ValueError("Sentinel-2 collection is empty. Check your date range or AOI.")

  def _process_Sentinel2(self, interval: int, start_date: str, end_date: str):
    increment = 'day'
    start = ee.Date(start_date)
    end = ee.Date(end_date)
    dates = ee.List.sequence(start.millis(), end.millis(), ee.Number(interval).multiply(1000 * 60 * 60 * 24))

    def make_sentinel2_composite(date):
      date = ee.Date(date)
      composite = self.colsentinel2.filterDate(date, date.advance(interval, increment)).mean()
      return composite.clip(self.aoi).set('system:time_start', date.millis())

    SENTINEL2_10DAY = ee.ImageCollection.fromImages(dates.map(make_sentinel2_composite))
    filtered_collection = SENTINEL2_10DAY.filter(ee.Filter.listContains('system:band_names', 'B2'))

    def calculate_indices_and_clip(image):

      ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
      evi = image.expression('2.5 * ((NIR - Red) / (NIR + 6 * Red - 7.5 * Blue + 1))', {
                'NIR': image.select('B8'),
                'Red': image.select('B4'),
                'Blue': image.select('B2')
            }).rename('EVI')
      savi = image.expression('((NIR - Red) / (NIR + Red + L)) * (1 + L)', {
                'NIR': image.select('B8'),
                'Red': image.select('B4'),
                'L': 0.5
            }).rename('SAVI')
      indices_image = ee.Image.cat([ndvi, evi, savi])
      return indices_image.clip(self.aoi).copyProperties(image, image.propertyNames())

    self.indices_image = filtered_collection.map(calculate_indices_and_clip).toBands()

  def _combine_sentinel1_sentinel2(self):
    self.stack_sentinel1_SENTINEL2_INDEXES = self.stack_sentinel1.addBands(self.indices_image)

    if self.table_clip is not None:
      self.stack_sentinel1_SENTINEL2_INDEXES = self.stack_sentinel1_SENTINEL2_INDEXES.clip(self.table_clip)

    self.reduced_image = self.stack_sentinel1_SENTINEL2_INDEXES.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=self.aoi,
            scale=10,
            bestEffort=True,
            maxPixels=1e8
        )

  def _export_data(self, name_file: str, name_folder: str):
    if not self.reduced_image.getInfo():
      raise ValueError("Reduced image dictionary is empty. Nothing to export.")

    feature = ee.Feature(None, self.reduced_image)

    task = ee.batch.Export.table.toDrive(
            collection=ee.FeatureCollection([feature]),  # Convert feature to a feature collection
            description='sentinel_export',  # Description of the export task
            folder=name_folder,  # Folder in Google Drive to export to
            fileNamePrefix=str(name_file),  # Prefix for the exported file(s)
            fileFormat='CSV'  # Specify the file format as CSV
        )

    task.start()

    while task.active():
      status = task.status()
      print("Export task status:", status)
      time.sleep(10)

    status = task.status()
    print("Export task status:", status)

  def pipeline_data(self, start_date: str, end_date: str, name_file: str, name_folder: str) -> None:
    self._load_Sentinel1(start_date, end_date)
    print("Loaded Sentinel-1")
    self._load_Sentinel2(start_date, end_date, 100)
    print("Loaded Sentinel-2")
    self._process_Sentinel1()
    print("Processed Sentinel-1")
    self._process_Sentinel2(5, start_date, end_date)
    print("Processed Sentinel-2")
    self._combine_sentinel1_sentinel2()
    print("Combined Sentinel-1 and Sentinel-2 data")
    self._export_data(name_file, name_folder)
    print(f"{name_file} --> export data")
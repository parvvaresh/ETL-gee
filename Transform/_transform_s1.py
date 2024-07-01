import ee

def transform_sentinel1(sentinel1: ee.ImageCollection) -> ee.Image:
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

  vvIw = sentinel1.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')).filter(ee.Filter.eq('instrumentMode', 'IW'))
  vvIwAsc = vvIw.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
  vvIwDesc = vvIw.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  vhIw = sentinel1.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')).filter(ee.Filter.eq('instrumentMode', 'IW'))
  vhIwAsc = vhIw.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
  vhIwDesc = vhIw.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))

  stack_sentinel1 = mosaic_by_date(vvIwAsc).toBands() \
                    .addBands(mosaic_by_date(vhIwAsc).toBands()) \
                    .addBands(mosaic_by_date(vvIwDesc).toBands()) \
                    .addBands(mosaic_by_date(vhIwDesc).toBands())




  return stack_sentinel1
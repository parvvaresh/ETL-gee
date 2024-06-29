import ee

def combine_sentinel1_sentinel2(aoi,
                                table_clip,
                                indices_image ,
                                stack_sentinel1):
  stack_sentinel1_SENTINEL2_INDEXES = stack_sentinel1.addBands(indices_image)



  reduced_image = stack_sentinel1_SENTINEL2_INDEXES.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=aoi,
            scale=10,
            bestEffort=True,
            maxPixels=1e8
        )
  return reduced_image
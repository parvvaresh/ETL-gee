import ee
import time

def save_csv(reduced_image,
         name_file: str,
         name_folder: str):

  if not reduced_image.getInfo():
    raise ValueError("Reduced image dictionary is empty. Nothing to export.")

  feature = ee.Feature(None, reduced_image)

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

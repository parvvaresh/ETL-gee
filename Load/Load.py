import time

import ee


def load(reduced_image: ee.Image, aoi: ee.Geometry, name_file: str, name_folder: str,
         scale: int = 10, crs: str = 'EPSG:4326', wait: bool = True) -> ee.batch.Task:
    """
    Load phase: export the transformed image to Google Drive as a GeoTIFF.

    Parameters:
    - reduced_image (ee.Image): Output of the Transform phase.
    - aoi (ee.Geometry): Export region.
    - name_file (str): Task description and output file name prefix in Google Drive.
    - name_folder (str): Google Drive folder (created if it does not exist).
    - scale (int): Output pixel size in metres (default 10, the Sentinel-2 resolution).
    - crs (str): Output coordinate reference system (default 'EPSG:4326').
    - wait (bool): If True, block until the export task finishes and raise if it fails.

    Returns:
    - ee.batch.Task: The started export task.

    Raises:
    - ValueError: If the image has no bands.
    - RuntimeError: If wait=True and the export task does not complete successfully.
    """
    if reduced_image.bandNames().size().getInfo() == 0:
        raise ValueError("The image has no bands. Nothing to export.")

    task = ee.batch.Export.image.toDrive(
        image=reduced_image,
        description=name_file,
        fileNamePrefix=name_file,
        folder=name_folder,
        region=aoi,
        scale=scale,
        crs=crs,
        maxPixels=1e13,
    )
    task.start()
    print(f"Export task '{name_file}' started (id: {task.id}).")

    if not wait:
        return task

    while task.active():
        print("Export task state:", task.status().get('state'))
        time.sleep(10)

    status = task.status()
    if status.get('state') != 'COMPLETED':
        raise RuntimeError(f"Export task failed: {status.get('error_message', status)}")

    print(f"Export completed: Google Drive/{name_folder}/{name_file}.tif")
    return task

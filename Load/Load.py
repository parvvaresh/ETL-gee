import ee
import time

def load(reduced_image: ee.Image, aoi: ee.Geometry, name_file: str, name_folder: str) -> None:
    """
    Export the processed image to Google Drive.

    This function exports a given Earth Engine image (reduced_image) to the user's Google Drive.
    The exported image is clipped to the specified area of interest (AOI) and saved with the 
    specified file name and folder.

    Parameters:
    - reduced_image (ee.Image): 
        The processed image to be exported.
    - aoi (ee.Geometry): 
        The area of interest in Earth Engine Geometry format. The exported image will be clipped to this AOI.
    - name_file (str): 
        The name of the output file in Google Drive.
    - name_folder (str): 
        The folder name in Google Drive where the file will be saved.

    Returns:
    - None: 
        This function does not return any value. The exported image is saved to Google Drive.

    Raises:
    - ValueError: 
        If the input image (reduced_image) is empty or invalid.
    - Exception: 
        If an error occurs during the export process.

    Notes:
    - The export task uses a spatial resolution (scale) of 10 meters.
    - The coordinate reference system (CRS) used is EPSG:4326 (WGS84).
    - The maximum number of pixels allowed for export is set to 1e13.
    """
    # Check if the input image is valid
    if not reduced_image.getInfo():
        raise ValueError("Reduced image dictionary is empty. Nothing to export.")

    # Initialize the export task to Google Drive
    task = ee.batch.Export.image.toDrive(
        image=reduced_image,
        description=name_file,
        folder=name_folder,
        region=aoi,
        scale=10,  # Spatial resolution in meters
        crs='EPSG:4326',  # Coordinate Reference System
        maxPixels=1e13  # Maximum number of pixels allowed for export
    )

    # Start the export task
    task.start()

    # Monitor the task status
    while task.active():
        print("Export task status:", task.status())
        time.sleep(10)  # Wait 10 seconds before checking again

    # Print final task status
    print("Export task completed:", task.status())

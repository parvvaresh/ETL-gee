import ee

from ._extract_s1 import extract_Sentinel1
from ._extract_s2 import  extract_Sentinel2






def Extract(aoi : ee.Geometry, start_date : str, end_date : str) -> dict:
    """
    Main function for the Extract phase.
    
    Extracts Sentinel-2 and Sentinel-1 data for the given area of interest (AOI)
    and date range, and returns the collections.
    
    Parameters:
    - aoi: ee.Geometry
        Area of interest in Earth Engine Geometry format.
    - start_date: str
        Start date for data extraction in 'YYYY-MM-DD' format.
    - end_date: str
        End date for data extraction in 'YYYY-MM-DD' format.
    
    Returns:
    - dict containing Sentinel-2 and Sentinel-1 collections.
    """
    try:
        print("Extracting Sentinel-2 data...")
        sentinel2_collection = extract_Sentinel2(aoi, start_date, end_date)
        print(f"Extracted {sentinel2_collection.size().getInfo()} Sentinel-2 images.")

        print("Extracting Sentinel-1 data...")
        sentinel1_collection = extract_Sentinel1(aoi, start_date, end_date)
        print(f"Extracted {sentinel1_collection.size().getInfo()} Sentinel-1 images.")

        return {
            "Sentinel2": sentinel2_collection,
            "Sentinel1": sentinel1_collection
        }
    except Exception as e:
        print(f"Error during data extraction: {str(e)}")
        return None

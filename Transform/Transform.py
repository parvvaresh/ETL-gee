from datetime import date, timedelta

import ee

from .calculate_interval_mean import calculate_interval_mean


def transform(aoi: ee.Geometry, start_date: str, end_date: str, interval_days: int,
              collectionS2: ee.ImageCollection, collectionS1: ee.ImageCollection) -> ee.Image:
    """
    Transform phase: aggregate Sentinel-2 and Sentinel-1 into fixed time intervals and
    stack all intervals into a single multi-band image.

    The period [start_date, end_date) is split into floor(days / interval_days) intervals of
    interval_days each; a trailing partial interval is dropped. Every band of every interval
    is prefixed with the interval start date, e.g. '20230101_NDVI', '20230111_VV'.

    Parameters:
    - aoi (ee.Geometry): Area of interest.
    - start_date (str): Start date, 'YYYY-MM-DD'.
    - end_date (str): End date, 'YYYY-MM-DD' (exclusive).
    - interval_days (int): Length of each interval in days.
    - collectionS2 (ee.ImageCollection): Sentinel-2 collection from the Extract phase.
    - collectionS1 (ee.ImageCollection): Sentinel-1 collection from the Extract phase.

    Returns:
    - ee.Image: Float image with (number of intervals x bands per interval) bands.

    Raises:
    - ValueError: If interval_days is not positive or the period is shorter than one interval.
    """
    if interval_days <= 0:
        raise ValueError("interval_days must be a positive integer.")

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    num_intervals = (end - start).days // interval_days

    if num_intervals < 1:
        raise ValueError(
            f"The period {start_date} -> {end_date} is shorter than one interval of {interval_days} days.")

    print(f"Building {num_intervals} interval(s) of {interval_days} day(s)...")

    interval_images = []
    for i in range(num_intervals):
        interval_start = start + timedelta(days=i * interval_days)
        prefix = interval_start.strftime('%Y%m%d')

        image = calculate_interval_mean(ee.Date(interval_start.isoformat()), interval_days,
                                        collectionS2, collectionS1, aoi)

        new_names = image.bandNames().map(lambda name: ee.String(prefix + '_').cat(name))
        interval_images.append(image.rename(new_names))

    return ee.Image.cat(interval_images).toFloat()

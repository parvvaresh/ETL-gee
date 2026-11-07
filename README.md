# ETL-gee

An Extract → Transform → Load pipeline on Google Earth Engine (GEE). It builds a time-series
feature stack from **Sentinel-2**, **Sentinel-1**, terrain (GMTED2010) and **MODIS LST** for an
area of interest and exports it to Google Drive as one multi-band GeoTIFF.

```
Extract ──────────────────────► Transform ─────────────────────────► Load
Sentinel-2 (clear-sky mask)     one image per `interval` days:        Export.image.toDrive
Sentinel-1 (IW, VV + VH)        S2 mean, S1 mean, indices,            → <folder>/<name>.tif
                                terrain, MODIS → stacked into 1 image
```

## Project structure

```
ETL.py                            # gee(): runs Extract -> Transform -> Load
Extract/
  Extract.py                      # extract(): returns {"Sentinel2": ..., "Sentinel1": ...}
  _extract_s2.py                  # Sentinel-2 SR Harmonized + SCL clear-sky mask
  _extract_s1.py                  # Sentinel-1 GRD (IW, VV/VH)
Transform/
  Transform.py                    # transform(): splits the period into intervals and stacks them
  calculate_interval_mean.py      # features for a single interval
Load/
  Load.py                         # load(): exports to Google Drive and waits for the task
```

## Installation

```bash
git clone https://github.com/parvvaresh/ETL-gee
cd ETL-gee
pip install -r requirements.txt
```

You need a Google Cloud project with the Earth Engine API enabled. See the
[official guide](https://developers.google.com/earth-engine/guides/python_install).

### Google Colab

```python
!git clone https://github.com/parvvaresh/ETL-gee
%cd ETL-gee
```

## Usage

Run the code from the repository root, so that `Extract`, `Transform` and `Load` can be imported.

```python
import ee

ee.Authenticate()                       # only needed once per environment
ee.Initialize(project='your-gcp-project-id')

from ETL import gee

aoi = ee.Geometry.Rectangle([51.30, 35.60, 51.45, 35.75])   # [xmin, ymin, xmax, ymax]

gee(
    aoi=aoi,
    start_date='2023-01-01',   # inclusive
    end_date='2023-01-31',     # exclusive
    cloudy_pixel=20,           # keep Sentinel-2 scenes with CLOUDY_PIXEL_PERCENTAGE < 20
    interval=10,               # aggregate every 10 days -> 3 intervals
    name_file='sentinel_data',
    name_folder='GEE_exports',
)
```

The result is written to `Google Drive/GEE_exports/sentinel_data.tif`.

### Parameters of `gee()`

| Parameter      | Type          | Description |
|----------------|---------------|-------------|
| `aoi`          | `ee.Geometry` | Area of interest; also the export region. |
| `start_date`   | `str`         | `YYYY-MM-DD`, inclusive. |
| `end_date`     | `str`         | `YYYY-MM-DD`, exclusive. |
| `cloudy_pixel` | `int`         | Maximum `CLOUDY_PIXEL_PERCENTAGE` (0–100) for Sentinel-2 scenes. |
| `interval`     | `int`         | Interval length in days. The period is split into `floor(days / interval)` intervals; a trailing partial interval is dropped. |
| `name_file`    | `str`         | Export task name and output file name. |
| `name_folder`  | `str`         | Google Drive folder. |
| `scale`        | `int`         | Export pixel size in metres (default `10`). |
| `wait`         | `bool`        | If `True` (default), block until the export finishes and raise if it fails. If `False`, return the started task immediately. |

`gee()` returns the `ee.batch.Task` of the export.

### Running the stages separately

```python
from Extract.Extract import extract
from Transform.Transform import transform
from Load.Load import load

collections = extract(aoi, '2023-01-01', '2023-01-31', cloudy_pixel=20)
image = transform(aoi, '2023-01-01', '2023-01-31', 10,
                  collections['Sentinel2'], collections['Sentinel1'])
print(image.bandNames().getInfo())     # check the output before exporting
task = load(image, aoi, 'sentinel_data', 'GEE_exports', wait=False)
```

## Output bands

Each interval adds these 26 bands. Every band name starts with the interval's start date,
e.g. `20230101_NDVI`, `20230111_VV`.

| Group | Bands | Source / notes |
|-------|-------|----------------|
| Sentinel-2 reflectance (mean, 0–1) | `B1 B2 B3 B4 B5 B6 B7 B8 B8A B9 B11 B12` | `COPERNICUS/S2_SR_HARMONIZED`; only SCL classes 4, 5, 6, 11 (vegetation, bare soil, water, snow) are kept |
| Sentinel-1 backscatter (mean, dB) | `VV VH` | `COPERNICUS/S1_GRD`; IW mode, only scenes that contain both VV and VH |
| Spectral indices | `NDVI EVI SAVI BSI` | Computed from the Sentinel-2 mean |
| Terrain | `mea min max slope` | `USGS/GMTED2010_FULL` elevation (m) and slope (degrees) |
| MODIS (median) | `Emis_32 Emis_31 LST_Day_1km LST_Night_1km` | `MODIS/061/MOD11A1`; emissivity is unitless, LST is in Kelvin |

If a sensor has no images in an interval, that interval's bands are masked (no data); the
pipeline does not fail.

All bands are exported as `float32`.

## Notes

- Extraction raises `ValueError` if the whole period has no Sentinel-2 or no Sentinel-1 images
  for the AOI (for Sentinel-2, try a higher `cloudy_pixel`).
- Exports at 10 m over large areas or long periods produce big files and can take a long time.
  Increase `scale` or shrink the AOI if the task is too slow or hits quota limits.
- Coarser sources (GMTED ~250 m, MODIS 1 km) are resampled to the export `scale`.

## License

MIT

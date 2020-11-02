# This python script will convert your single channel geoscience raster into an
# appropriately scaled tiff for importing into Blender as the displacement map.
# The same process is outlined in QGIS on github repository.

# From here, you simply need to load this in blender as the displacement map.
# You will also need to load an image texture for the colourmap.


from pathlib import Path

import numpy as np
import rasterio as rio
from rasterio.profiles import DefaultGTiffProfile

d_path = "C:/Luke/Python/blender/2018SA001_PACECopper_GCAS_Region8b_DEM_laser.ers"
dst_crs = "EPSG:28353"  # GDA94 MGA53

with rio.open(d_path) as d_src:
    array = np.array(d_src.read(1))
    mask = array == d_src.nodata
    array[mask] = 0

    scaled_array = 1 + (
        65533 * (array - array.min()) / (array.max() - array.min())
    ).astype(
        np.uint16
    )  # Scale between 1 and 65534.
    scaled_array[mask] = 0  # We set the nodatavalue to 0 (no height)

    if not scaled_array.min() >= 0 and scaled_array.max() < 65535:
        raise ValueError("Scaled array is still out of range for Uint16")

    height, width = scaled_array.shape
    profile = DefaultGTiffProfile(count=1)  # single band only
    profile.update(dtype=rio.uint16, nodata=0, height=height, width=width)

    with rio.open("test.tif", "w", **profile) as dst:
        dst.write(scaled_array, 1)

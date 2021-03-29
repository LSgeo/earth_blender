def gdal_convert_raster(raster_path):
    """Convert input geo raster and output files ready for blender rendering.
    This means we output two tifs:
     - A UINT16 file for the height map
     - A RGB colourmap of the same extent
    TODO:
     - gdalWarp to reproject
     - use cutline argument in Warp to crop to cutline.
    """
    from pathlib import Path

    import colorcet as cc
    from osgeo import gdal

    import numpy as np
    from PIL import Image

    gdal.UseExceptions()

    out_path = Path(raster_path).parent
    hillshade_file_path = out_path / "hillshade.tif"
    colourmap_file_path = out_path / "colourmap.tif"

    raster = gdal.Open(str(raster_path))
    band = raster.GetRasterBand(1)
    if band.GetMinimum() is None or band.GetMaximum() is None:
        band.ComputeStatistics(0)

    ## Create hillshade file
    translate_options = gdal.TranslateOptions(
        outputType=gdal.gdalconst.GDT_UInt16,
        scaleParams=[[band.GetMinimum(), band.GetMaximum(), 1, 65535]],
    )  # We leave 0 out so it should be used as a NaN indicator.
    a = gdal.Translate(str(hillshade_file_path), raster, options=translate_options)

    ## Create colourmap file
    array = band.ReadAsArray()
    nan_val = band.GetNoDataValue()
    mask = array == nan_val
    array[mask] = np.nan
    array = (array - np.nanmin(array)) / (np.nanmax(array) - np.nanmin(array))
    im_array = np.uint8(cc.cm.CET_L1(array, bytes=True))[:, :, :3]  # remove alpha
    # im_array[mask] = [0, 0, 0]
    image = Image.fromarray(im_array, mode="RGB")
    image.save(str(colourmap_file_path))

    print(
        f"Converted:\n{str(raster_path)}\n"
        f"into hillshade and colourmap, located in:\n{colourmap_file_path.parent}\n"
    )


gdal_convert_raster(
    raster_path=r"O:\Grids_Rendering_NGEA\03_Grids\70359_tmi_rtp_2vd.ers"
)


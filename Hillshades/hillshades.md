# Guide to creating rendered hillshades for geoscientific data

This guide will walk through the process of visualising geoscience data as a 3D surface with natural illumination. You can visualise any geophysical raster, although it works best with smooth or continuous data such as gravity, magnetics, DEMs, etc. 
You can visualise a single data layer, coloured using a colourmap, or integrate different datasets using one for the 3D effect and one for the colour data. The process is very similar.


0. [Install blender](https://www.blender.org/download/)
1. Download your data of choice in a typical format, such as .tif or .ers
1. Open the provided hillshades.blend file in Blender  
    a. Familiarise yourself with the [node layout of hillshades.blend](https://github.com/LSgeo/earth_blender/blob/hillshades/Data/Repo_Resources/hillshades_nodes.png)
3. Load the data later used for the surface colouring in the *colourmap_file* node (upper orange box)  
4. Load the data layer used for the 3D displacement in the *displacement_file* node (lower orange box)  
     a. If using different data for the hillshade and colourmap, you need to match the extents manually in a GIS program.  
     b. The hillshade needs to be using raw data values, normalised as an unsigned 16 bit integer (1 channel, 0-65535)  
          | In QGIS: *Raster>Conversion>Translate (Convert Format)*, and under Advanced>Additional command-line parameters, insert `-scale <your_data_min>, <your_data_max>, 0, 65535`)     
     c. The surface colour file needs to be sRGB (3 channel, 0-255)  
          | In QGIS: *Export>Save as>Rendered Image*
5. Adjust the *scale* parameter in the *Displacement* node (purple box) until the heightmap is suitably scaled for your data. 
6. Set camera and render settings, and process the render using the Render drop down menu (or press F12)


## Notes:
* Consider adjusting the sun angle with the Light object in Blender. Angle the "sun" so that the black line light path is perpendicular to the dominant strike, by adjusting the Light objects *Location* and *Rotation* parameters (Orange square)

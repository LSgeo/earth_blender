# Guide to creating rendered hillshades for geoscientific data

This guide will walk through the process of visualising geoscience data as a 3D surface with natural illumination. You can visualise any geophysical raster, although it works best with smooth or continuous data such as gravity, magnetics, DEMs, etc. 
You can visualise a single data layer coloured using a colourmap, or integrate different datasets using one for the 3D effect and one for the colour data. The process is very similar.

## GIS Step
1. Download your geoscience data of choice and import into your favorite GIS package
2. Normalise the data for the 3D displacement between 0 and 65535, and save as a UINT16 tif
     > In QGIS: *Raster>Conversion>Translate (Convert Format)*, and under *Advanced>Additional command-line parameters*, insert `-scale <your_data_min>, <your_data_max>, 0, 65535`, then select *Output Data type*: *UInt16*)
 
    a. If you are using the same data for the surface colouring:  
        i. Apply a colour map [Use Perceptually Uniform Colour Maps](https://peterkovesi.com/projects/colourmaps/index.html)
        
    b. If you are using a seperate dataset for the surface colouring:  
        i. Apply a colour map  
        ii. ensure the two layers have the same extent when exporting
        
4. Export your displacement map as a raw data tiff
      > In QGIS: *Export>Save as>Raw data*
5. Export your colour map as an rendered image tiff
      > In QGIS: *Export>Save as>Rendered Image*


## Blender Step
0. [Install blender](https://www.blender.org/download/)

1. Open the provided hillshades.blend file in Blender  
    a. Familiarise yourself with the node view for Blender.  
    ![node layout of hillshades.blend](https://github.com/LSgeo/earth_blender/blob/hillshades/Data/Repo_Resources/hillshades_nodes.png)
3. Load the data layer used for the surface colouring in the *colourmap_file* node (upper orange box)  
4. Load the data layer used for the 3D displacement in the *displacement_file* node (lower orange box)  
     a. Change the *Color Space* of the displacement map to *Raw*  
     b. The hillshade needs to be using raw data values, normalised as an unsigned 16 bit integer (1 channel, 0-65535)    
     c. The surface colour file needs to be sRGB (3 channel, 0-255)
5. Adjust the *Scale* parameter in the *Displacement* node (purple box) until the heightmap is suitably scaled for your data. 
6. Adjust remaining settings for the green texture box to adjust the appearance of the rendered surface.
7. Adjust scene *Render Properties* (camera icon in right hand menu) to set the *Render Engine* to *Cycles* and *Feature Set* to *Experimental*. Optionally set Device to GPU Compute.
8. Process the render using the Render drop down menu (or press F12)


## Notes:
* Consider adjusting the sun angle with the Light object in Blender. Angle the "sun" so that the black line light path is perpendicular to the dominant strike, by adjusting the Light objects *Location* and *Rotation* parameters (Orange square)

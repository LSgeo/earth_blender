 ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# <pep8 compliant>

bl_info = {
    "name": "Raster Hillshade Import",
    "author": "Luke, Tasman, David, Lu",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import GeoRasters for Hillshade",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}


import bpy
from bpy import context
import rasterio
import os
import math
from mathutils import Vector, Matrix
import numpy as np

from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )


class raster_hill_import(bpy.types.Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_scene.raster_hillshade"
    bl_label = "Import Raster for Hillshade"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".obj"

    filter_glob: StringProperty(
        default= "*.tif",
        options={'HIDDEN'},
    )

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    edges_setting: BoolProperty(
        name="Lines",
        description="Import lines and faces with 2 verts as edge",
        default=True,
    )
    smooth_groups_setting: BoolProperty(
        name="Smooth Groups",
        description="Surround smooth groups by sharp edges",
        default=True,
    )

    split_objects_setting: BoolProperty(
        name="Object",
        description="Import OBJ Objects into Blender Objects",
        default=True,
    )
    split_groups_setting: BoolProperty(
        name="Group",
        description="Import OBJ Groups into Blender Objects",
        default=True,
    )

    groups_as_vgroups_setting: BoolProperty(
        name="Poly Groups",
        description="Import OBJ groups as vertex groups",
        default=False,
    )

    image_search_setting: BoolProperty(
        name="Image Search",
        description="Search subdirs for any associated images "
                    "(Warning, may be slow)",
        default=False
    )

    split_mode_setting: EnumProperty(
        name="Split",
        items=(('ON', "Split", "Split geometry, omits unused verts"),
               ('OFF', "Keep Vert Order", "Keep vertex order from file"),),
    )

    clamp_size_setting: FloatProperty(
        name="Clamp Size",
        description="Clamp bounds under this value (zero to disable)",
        min=0.0, max=1000.0,
        soft_min=0.0, soft_max=1000.0,
        default=0.0,
    )

    axis_forward_setting: EnumProperty(
        name="Forward",
        items=(('X', "X Forward", ""),
               ('Y', "Y Forward", ""),
               ('Z', "Z Forward", ""),
               ('-X', "-X Forward", ""),
               ('-Y', "-Y Forward", ""),
               ('-Z', "-Z Forward", ""),
               ),
        default='-Z',
    )

    axis_up_setting: EnumProperty(
        name="Up",
        items=(('X', "X Up", ""),
               ('Y', "Y Up", ""),
               ('Z', "Z Up", ""),
               ('-X', "-X Up", ""),
               ('-Y', "-Y Up", ""),
               ('-Z', "-Z Up", ""),
               ),
        default='Y',
    )

    scale_setting: FloatProperty(
        name="Size",
        description="Scale objects",
        min=0.0, max=1000.0,
        soft_min=0.0, soft_max=1000.0,
        default=1,
    )

    
    def create_custom_mesh(self,file_name):
        raster = rasterio.open(file_name)
        objname = raster.name.split(sep='/')[-1] # set object name to file name
        r_bounds = list(raster.bounds) # get tif bounds

        # Define arrays for holding data    
        myvertex = []
        myfaces = []

        # Create vertices from geotiff bounds
        myvertex.extend([(r_bounds[0], r_bounds[1], 0.0)])
        myvertex.extend([(r_bounds[2], r_bounds[1], 0.0)])
        myvertex.extend([(r_bounds[0], r_bounds[3], 0.0)])
        myvertex.extend([(r_bounds[2], r_bounds[3], 0.0)])

        # Create all Faces
        myface = [(0, 1, 3, 2)]
        myfaces.extend(myface)

        mymesh = bpy.data.meshes.new(objname)
        myobject = bpy.data.objects.new(objname, mymesh)
        mymesh.from_pydata(myvertex, [], myfaces)
        mymesh.update(calc_edges=True)

        ## load image as texture
        
        
        # define a new material
        mat = bpy.data.materials.new(name=objname) # name it based on the image used to make it
        mat.use_nodes = True
        
        # get all the material nodes
        mat_nodes = mat.node_tree.nodes
        
        # make some nodes
        texPbsdf = mat_nodes["Principled BSDF"]
        texImage = mat_nodes.new('ShaderNodeTexImage')
        texMappi = mat_nodes.new('ShaderNodeMapping')
        texCoord = mat_nodes.new('ShaderNodeTexCoord')
            
        # link the nodes
        mat.node_tree.links.new(texPbsdf.inputs['Base Color'], texImage.outputs['Color'])
        mat.node_tree.links.new(texImage.inputs['Vector'], texMappi.outputs['Vector'])
        mat.node_tree.links.new(texMappi.inputs['Vector'], texCoord.outputs['Object'])
        
        # populate our nodes fields as necessary using math and other things
        texImage.image = bpy.data.images.load(file_name)
        
        # we want to transform the texture in a way that makes sense for our plane
        # thus we need two sets of dimensions
        # image resolution
        iw = raster.width
        ih = raster.height
        
        # geo extent
        rw = r_bounds[2] - r_bounds[0]
        rh = r_bounds[3] - r_bounds[1]
        
        w_scale = iw/rw
        h_scale = ih/rh

        texMappi.vector_type = "POINT"
        
        # define bottom left point relative to center of geometry in blender units
        w_loc = -iw/2
        h_loc = -ih/2
        
        texMappi.inputs[1].default_value = (w_loc,h_loc,0) # location
        texMappi.inputs[3].default_value = ((w_scale/iw),(h_scale/ih),0) # scale

        # assign to our object
        myobject.data.materials.append(mat)
        
        return(myobject,raster)

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "smooth_groups_setting")
        row.prop(self, "edges_setting")

        box = layout.box()
        row = box.row()
        row.prop(self, "split_mode_setting", expand=True)

        row = box.row()
        if self.split_mode_setting == 'ON':
            row.label(text="Split by:")
            row.prop(self, "split_objects_setting")
            row.prop(self, "split_groups_setting")
        else:
            row.prop(self, "groups_as_vgroups_setting")

        row = layout.split()
        row.prop(self, "clamp_size_setting")
        layout.prop(self, "axis_forward_setting")
        layout.prop(self, "axis_up_setting")

        layout.prop(self, "image_search_setting")

        row = layout.split()
        row.prop(self, "scale_setting")
        row.prop(self, "center_origin")

    def execute(self, context):
        obs = context.selected_objects
        bpy.ops.object.delete()
        C = bpy.context
        # get the folder
        folder = (os.path.dirname(self.filepath))
        
        r_objs = []
        r_rios = []
        
        
        # perform imports for all files
        for j, i in enumerate(self.files):
            
            # generate full path to file
            path_to_file = (os.path.join(folder, i.name))

            _, file_ext = os.path.splitext(path_to_file)
                    
            # load tifs
            if file_ext==".tif": 
                myobj,raster = self.create_custom_mesh(str(path_to_file))
                scene = context.scene
                scene.collection.objects.link(myobj)
                # append to list for other processing
                r_objs.append(myobj)
                r_rios.append(raster)
                                       
        ## other processing   
        item='MESH'
        bpy.ops.object.select_all(action='DESELECT')             
        bpy.ops.object.select_by_type(type=item)
        obs = context.selected_objects
        for ob in obs:
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY',center='BOUNDS')
            ob.scale.x = 0.0002
            ob.scale.y = 0.0002
            ob.location.x=0
            ob.location.y=0
            ob.location.z=0
            
        # clear unneccesary objects
        for o in bpy.context.scene.objects: #Remove all lights and cameras - we make new ones
            if o.type in ['CAMERA','LIGHT','EMPTY']:
                o.select_set(True)
            else:
                o.select_set(False)
        
        bpy.ops.object.delete()


        #Add new sun and ortho camera at origin
        bpy.ops.object.light_add(type="SUN", location=(0.0, 0.0, 10.0))
        C.object.data.energy = 5  

        bpy.ops.object.camera_add(location=(0.0, 0.0, 20.0))
        C.object.data.type="ORTHO"
        
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(raster_hill_import.bl_idname, text="Hillshade Raster Import (.tif)")


def register():
    bpy.utils.register_class(raster_hill_import)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(raster_hill_import)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
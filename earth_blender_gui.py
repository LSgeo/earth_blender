# -*- coding:utf-8 -*-

#  ***** GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#  ***** GPL LICENSE BLOCK *****

import bpy
import os, sys, tempfile
from datetime import datetime
import bpy.utils.previews as iconsLib
import bpy
from bpy import context
import rasterio
import os
import math
from mathutils import Vector, Matrix
import numpy as np
from bpy.types import Panel

from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )

bl_info = {
    'name': 'Earth Blender',
    'description': 'Tools for the Visualisation of Geological Data',
    'author': 'Tasman,Luke,David,Lu',
    'license': 'GPL',
    'deps': '',
    'version': (0, 1),
    'blender': (2, 80, 0),
    'location': 'View3D > Tools > Earth Blender',
    'warning': '',
    'repo_url': 'https://github.com/LSgeo/earth_blender',
    'link': '',
    'support': 'COMMUNITY',
    'category': '3D View'
    }



# put functional code here
class import_geo_objects(bpy.types.Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_scene.import_geo_objects"
    bl_label = "Import Geo_Scene"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".obj"

    filter_glob: StringProperty(
        default= "*.obj",
        options={'HIDDEN'},
    )

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)


    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "smooth_groups_setting")
        row.prop(self, "edges_setting")

        box = layout.box()
        row = box.row()
        row.prop(self, "split_mode_setting", expand=True)

    def execute(self, context):
        obs = context.selected_objects
        bpy.ops.object.delete()
        C = bpy.context
        # get the folder
        folder = (os.path.dirname(self.filepath))
        
        
        # perform imports for all files
        for j, i in enumerate(self.files):
            
            # generate full path to file
            path_to_file = (os.path.join(folder, i.name))

            _, file_ext = os.path.splitext(path_to_file)
            
            # loading the objs
            if file_ext==".obj":     
                bpy.ops.import_scene.obj(filepath=path_to_file)        
                                       
        ## other processing   
        item='MESH'              
        bpy.ops.object.select_by_type(type=item)
        obs = context.selected_objects
        
        scaling = 0.0002
        for ob in obs:
            orig_loc, orig_rot, orig_scale = ob.matrix_world.decompose()
            orig_loc_mat   = Matrix.Translation(orig_loc)
            orig_rot_mat   = orig_rot.to_matrix().to_4x4()
            orig_scale_mat = (Matrix.Scale(scaling,4,(1,0,0)) @ Matrix.Scale(scaling,4,(0,1,0)) @ Matrix.Scale(scaling,4,(0,0,1)))
            
            ob.matrix_world = orig_loc_mat @ orig_rot_mat @ orig_scale_mat
            ob.data.transform(ob.matrix_world)
            ob.matrix_world = Matrix()
            
        # origin setting
        obj_objects = bpy.context.scene.objects # all objects
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type=item)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY',center='BOUNDS')
        
        # move to 0,0 - this is old magic
        obs = context.selected_objects
        o_calc = sum((obj.matrix_world.translation for obj in obs),Vector()) / len(obs)         
        
        bpy.ops.object.empty_add(location=o_calc)
        
        mt = context.object
        mwi = mt.matrix_world.inverted()

        for ob in obs:
            ob.parent = mt
            # alter ob.matrix_local
            ob.matrix_local = mwi @ ob.matrix_world

        mt.location = (0, 0, 0)
        bpy.data.objects.remove(mt)
        
        
        #bpy.ops.transform.resize(value=(0.002,0.002,0.002))
        #bpy.ops.object.transform_apply(scale=True)

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


class import_hil_ras(bpy.types.Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_scene.import_hil_ras"
    bl_label = "Import Raster for Hillshade"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".tif"

    filter_glob: StringProperty(
        default= "*.tif",
        options={'HIDDEN'},
    )

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)

    
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
        raster = [x for x in obs if x.name in [r.name for r in r_objs]]
        for ob in raster:
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
    
    
bpy.utils.register_class(import_geo_objects)
bpy.utils.register_class(import_hil_ras)
# GUI START

icons_dict = {}

class earth_blender_menu(bpy.types.Menu):
    bl_label = "Earth Blender"
    # Set the menu operators and draw functions
    def draw(self, context):
        layout = self.layout
        layout.operator('import_scene.import_hil_ras', icon='RNDCURVE')
        layout.separator()
        layout.operator('import_scene.import_geo_objects', icon='CAMERA_STEREO')

def add_gis_menu(self, context):
    if context.mode == 'OBJECT':
        self.layout.menu('earth_blender_menu')

def register():
    #icons
    global icons_dict
    icons_dict = iconsLib.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")


    bpy.utils.register_class(earth_blender_menu)
    
    #menus
    bpy.types.VIEW3D_MT_editor_menus.append(earth_blender_menu)

    #shortcuts
    if not bpy.app.background: #no ui when running as background
        wm = bpy.context.window_manager
        kc =  wm.keyconfigs.active
        if '3D View' in kc.keymaps:
            km = kc.keymaps['3D View']


def unregister():

    #icons
    global icons_dict
    icons_dict = iconsLib.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")


    bpy.utils.unregister_class(earth_blender_menu)
    
    #menus
    bpy.types.VIEW3D_MT_editor_menus.remove(earth_blender_menu)

    #shortcuts
    if not bpy.app.background: #no ui when running as background
        wm = bpy.context.window_manager
        kc =  wm.keyconfigs.active
        if '3D View' in kc.keymaps:
            km = kc.keymaps['3D View']
        
if __name__ == "__main__":
    register()
# ##### BEGIN GPL LICENSE BLOCK #####
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
    "name": "Import GeoScene",
    "author": "Tasman, David, Luke, Lu",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import and scale multiple OBJ, and GeoRasters",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}


import bpy
import rasterio
import os
import math

from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )






class ImportGEO_Scene(bpy.types.Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_scene.geo_scene"
    bl_label = "Import Geo_Scene"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".obj"

    filter_glob: StringProperty(
        default= "*.tif;*.obj",
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

    center_origin: BoolProperty(
        name="Center Origin",
        default=True
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
        
        texMappi.vector_type = "POINT"
        texMappi.inputs[1].default_value = (10,10,10) # location
        texMappi.inputs[3].default_value = (10,10,10) # scale

        # assign to our object
        myobject.data.materials.append(mat)
        return(myobject)

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

        # get the folder
        folder = (os.path.dirname(self.filepath))

        # iterate through the selected files
        for j, i in enumerate(self.files):
            
            # generate full path to file
            path_to_file = (os.path.join(folder, i.name))

            _, file_ext = os.path.splitext(path_to_file)
            
            #tif_obj = [
            
            
            if file_ext==".tif": 
                myobj = self.create_custom_mesh(str(path_to_file))
                #tif_obj.append(obj)
                myobj.location.x = 0
                myobj.location.y = 0
                myobj.location.z = 0
                scene = context.scene
                scene.collection.objects.link(myobj)

            if file_ext==".obj":     
                # call obj operator and assign ui values
                bpy.ops.import_scene.obj(filepath=path_to_file,
                                         axis_forward=self.axis_forward_setting,
                                         axis_up=self.axis_up_setting,
                                         use_edges=self.edges_setting,
                                         use_smooth_groups=self.smooth_groups_setting,
                                         use_split_objects=self.split_objects_setting,
                                         use_split_groups=self.split_groups_setting,
                                         use_groups_as_vgroups=self.groups_as_vgroups_setting,
                                         use_image_search=self.image_search_setting,
                                         split_mode=self.split_mode_setting,
                                         global_clight_size=self.clamp_size_setting)

                if self.center_origin:
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                
                bpy.ops.transform.resize(value=(self.scale_setting, self.scale_setting, self.scale_setting), constraint_axis=(False, False, False))
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportGEO_Scene.bl_idname, text="Import GeoScene (.obj,.tif)")


def register():
    bpy.utils.register_class(ImportGEO_Scene)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportGEO_Scene)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
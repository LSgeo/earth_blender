bl_info = {
    "name": "big dum dum",
    "blender": (2, 80, 0),
}

# module imports
import bpy

class tif2plane(bpy.types.Operator):
    '''I wanna take some things and do some things'''
    bl_idname = "object.tif2plane"
    bl_label = "Tif Plane"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self,context):
        objname = 'fart'
        myvertex =[]
        myfaces  =[]
            
        points = [[(-1.0, -1.0, 0.0)],[(-1.0, 1.0, 0.0)],
                    [(1.0, -1.0, 0.0)],[(1.0, 1.0, 0.0)]]
            
        # iteratively cycle through point definition
        for i in range(len(points)):
            point = points[i]
            myvertex.extend(point)
                
        # face for plane
        myface = [(0, 1, 3, 2)]
        myfaces.extend(myface)
        
        
        mymesh = bpy.data.meshes.new(objname)
        myobject = bpy.data.objects.new(objname, mymesh)    
        # Generate mesh data
        mymesh.from_pydata(myvertex, [], myfaces)
        # Calculate the edges
        mymesh.update(calc_edges=True)
        
        myobject.location.x = 0
        myobject.location.y = 0
        myobject.location.z = 0
        
        scene = context.scene
        scene.collection.objects.link(myobject)
        
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(tif2plane.bl_idname)
    
def register():
    bpy.utils.register_class(tif2plane)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # hndle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(tif2plane)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
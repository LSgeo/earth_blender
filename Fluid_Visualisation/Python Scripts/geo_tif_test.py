def create_custom_mesh(objname, file_name):

    # Define arrays for holding data    
    myvertex = []
    myfaces = []

    # Create all Vertices

    # vertex 0
    mypoint = [(-1.0, -1.0, 0.0)]con
    myvertex.extend(mypoint)

    # vertex 1
    mypoint = [(1.0, -1.0, 0.0)]
    myvertex.extend(mypoint)

    # vertex 2
    mypoint = [(-1.0, 1.0, 0.0)]
    myvertex.extend(mypoint)

    # vertex 3
    mypoint = [(1.0, 1.0, 0.0)]
    myvertex.extend(mypoint)

    # -------------------------------------
    # Create all Faces
    # -------------------------------------
    myface = [(0, 1, 3, 2)]
    myfaces.extend(myface)


    mymesh = bpy.data.meshes.new(objname)

    myobject = bpy.data.objects.new(objname, mymesh)

    bpy.context.scene.objects.link(myobject)

    # Generate mesh data
    mymesh.from_pydata(myvertex, [], myfaces)
    # Calculate the edges
    mymesh.update(calc_edges=True)

    # Set Location
    myobject.location.x = px
    myobject.location.y = py
    myobject.location.z = pz

    return(myobject)

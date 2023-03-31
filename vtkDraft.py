import vtk

# Create a reader for the PLY file
reader = vtk.vtkPLYReader()
reader.SetFileName("SZ_002-NW.ply")
reader.Update()

# Create a mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Create an actor and set its mapper
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Set the color of the actor to white
actor.GetProperty().SetColor(1.0, 1.0, 1.0)

# Create a renderer and add the actor to it
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

# Set up a basic light
light = vtk.vtkLight()
light.SetFocalPoint(renderer.GetActiveCamera().GetFocalPoint())
light.SetPosition(renderer.GetActiveCamera().GetPosition())
renderer.AddLight(light)

# Create a render window and set its size
render_window = vtk.vtkRenderWindow()
render_window.SetSize(800, 600)
renderer.SetBackground(1.0, 1.0, 1.0)

# Add the renderer to the render window
render_window.AddRenderer(renderer)

# Create an interactor and set it up with the render window
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()


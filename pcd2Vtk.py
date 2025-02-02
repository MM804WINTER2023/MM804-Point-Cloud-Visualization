import vtk
import open3d as o3d
import numpy as np
import numpy as np
import open3d as o3d
from vtkmodules.vtkIOImage import vtkPNGWriter
import os
import random
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowToImageFilter
)


def vtkPCDLoader(path, model_Num, itemName):
    clases=['PLY##', 'CL##', 'PV##', 'PLW##', 'PLXW##', 'PLSB##', 'LDN##', 'SVB', 'VLG', 'BOX', 'VLT', 'ACH', 'MT', 'LPS', 'POLHT', 'MHE', 'MHT', 'JB', 'ANC', 'POLHY', 'GPO', 'PWT', 'MHS', 'CBT', 'MHCB', 'STDP', 'FH', 'VHCL', 'COT', 'VLW', 'MHD', 'SBS', 'SZ', 'SGW', 'IRS', 'SI', 'SSS', 'SNP', 'SP', 'TR', 'PLXW2##', 'PLA##', 'PLBK##', 'HV', 'TLS', 'PWL', 'TREC', 'TRED', 'KSK', 'POLEL', 'MRS', 'PRS', 'PGZ', 'BUSH', 'ANC']
    d=[] # List that used to contain the path of the pcd object 
    clouds_object = [] # List that used to contain the pcd object 
    # Create two empty lists for source objects
    sourceObjects = list()
    sourceObjects2 = list()
    # Traverse through the directory tree rooted at `path`
    for root, dirs, filenames in os.walk(path):
        for clouds in filenames:
            d.append(root+'/'+clouds)
            clouds_object.append(clouds)
    new_path = ""   
    for samples in d:
        item = itemName

        for clasesss in [item]: #["FH","LPS", 'SI','SSS', 'SNP', 'BUSH', 'PWL', 'POLHT', 'BOX']:
            if clasesss in samples:
                index = samples.find("MHE")
                if index != -1:
                    # Slice the string from the "MHE" index to the end of the path
                    new_path = samples[index:]
                else:
                    # "MHE" is not in the path, so keep the original path
                    new_path = samples
                # Read the point cloud data from the file using Open3D 
                # and convert it to a numpy array
                pcd = o3d.io.read_point_cloud(samples)
                p = np.asarray(pcd.points)
                # Create a new vtkPoints object and add each point in `p` to it
                points = vtk.vtkPoints()
                vertices = vtk.vtkCellArray()
                for i in range(len(p)):
                    point_id = points.InsertNextPoint(p[i])
                    vertices.InsertNextCell(1)
                    vertices.InsertCellPoint(point_id)  
                # Create a new vtkPolyData object, set the points and vertices, 
                # and add it to `sourceObjects` 
                sourceObjects.append(vtk.vtkPolyData())
                sourceObjects[-1].SetPoints(points)
                sourceObjects[-1].SetVerts(vertices)
                sourceObjects2.append(clasesss)
                break
            break # Break out of the loop if the class is not found in the file path

    # The Total windows number in app is 3 so as the renderers 
    windowNum = 3
    colors = vtk.vtkNamedColors()

    # Set the background color.
    colors.SetColor('BkgColor', [255, 255, 255, 255])
    # this code sets it to white with RGBA values [255, 255, 255, 255] (fully opaque)
    renderers = list()
    mappers = list()
    actors = list()
    textmappers = list()
    textactors = list()

    # Create one text property for all.
    textProperty = vtk.vtkTextProperty()
    textProperty.SetFontSize(8)
    textProperty.SetJustificationToCentered()
    textProperty.SetColor(colors.GetColor3d('LightGoldenrodYellow'))

    backProperty = vtk.vtkProperty()
    backProperty.SetColor(colors.GetColor3d('Tomato'))
    targetObjects = sourceObjects[model_Num]
    targetObjects2 = sourceObjects2[model_Num]

    # Create a source, renderer, mapper, and actor
    # for each object.
    for i in range(0, windowNum):
        mappers.append(vtk.vtkPolyDataMapper())
        mappers[i].SetInputData(targetObjects)

        actors.append(vtk.vtkActor())
        actors[i].SetMapper(mappers[i])
        actors[i].GetProperty().SetOpacity(0.8)
        actors[i].GetProperty().SetColor(colors.GetColor3d('DarkGrey'))
        actors[i].SetBackfaceProperty(backProperty)
        actors[i].GetProperty().SetPointSize(1.0)      

        textmappers.append(vtk.vtkTextMapper())
        textmappers[i].SetInput(targetObjects2)
        textmappers[i].SetTextProperty(textProperty)

        textactors.append(vtk.vtkActor2D())
        textactors[i].SetMapper(textmappers[i])
        textactors[i].SetPosition(120, 16)

        renderers.append(vtk.vtkRenderer())
    
    gridDimensions = 2



    # We need a renderer even if there is no actor.
    for i in range(len(sourceObjects), gridDimensions ** 2):
        renderers.append(vtk.vtkRenderer())
        


    for index in range(0, windowNum):
        renderers[index].AddActor(actors[index])
        renderers[index].AddActor(textactors[index])
        # Set the background color of the renderer to white and reset the camera
        renderers[index].SetBackground(colors.GetColor3d('White'))
        renderers[index].ResetCamera()

        # Set camera position and orientation for each renderer
        if index == 0:
            renderers[index].GetActiveCamera().Azimuth(60)# Vertical
            renderers[index].GetActiveCamera().Elevation(100) # Vertical
            renderers[index].GetActiveCamera().Zoom(1.2)# Vertical
            position = renderers[index].GetActiveCamera().GetPosition()
            print("Camera position:", position)
        elif index == 1:
            renderers[index].GetActiveCamera().Azimuth(180) # FLAT
            renderers[index].GetActiveCamera().Elevation(100) # FLAT
            renderers[index].GetActiveCamera().Zoom(1.2)
        elif index == 2:
            renderers[index].GetActiveCamera().Azimuth(-180) # 60 angle view
            renderers[index].GetActiveCamera().Elevation(-00)
            renderers[index].GetActiveCamera().Zoom(1.2)
        renderers[index].ResetCameraClippingRange()


    return renderers, new_path


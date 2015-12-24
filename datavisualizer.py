import bpy
import bpy.ops as B
import mathutils
from mathutils import Vector
import math
from math import radians
from math import degrees
from decimal import *
from Definitions import *
import csv
import os

"""Global Data"""
dataGlobal = {}
textOptionsGlobal = {}

"""These are controls"""
FramesPerSecond = 30
defaultScale = ((4,4,4))
defaultLocation = ((-1.5,0,0))
invertPitch = False


""" function that reads all data from csv file"""
#Usage:
#importFile: contains file path to the data file
#dataToInclude: list of what data is in the files
#timeStep: minimum time step between each row of data
def readIntoLists(importFile, dataToInclude, timeStep):
    data = {x: [] for x in dataToInclude}
    oldTime = float(-2*timeStep)
    with open(importFile, 'r') as dataFile:
        iterator = csv.reader(dataFile, delimiter=',', quotechar='|')
        next(iterator)
        for row in iterator:
            if float(row[rowIndex['Time']]) - oldTime > timeStep:
                for dataType in dataToInclude:
                    data[dataType].append(float(row[rowIndex[dataType]]))
                oldTime = float(row[rowIndex['Time']])

    return data


""" Import model """
#modelFile: name of the model to import
def importModel(modelFile):
    bpy.ops.import_scene.obj(filepath = modelFile)
    o = bpy.data.objects['Object']
    bpy.context.scene.objects.active = o
    bpy.context.scene.objects.active.name = 'RotationDisplay'
    o.scale = defaultScale
    o.location = defaultLocation
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.ops.object.transform_apply( rotation = True )

"""Creates a list of values that contain keyframe numbers for each time"""
#Note it is entirely possible for these to overlap
#Times: list of time values
#timeStep: the minimum amount of time between keyframes
def createKeyframeList(Times, timeStep, timeScale):
    startingTime = Times[0]
    frameslist = []
    for time in Times:
        framenumber = FramesPerSecond/timeScale *(time-startingTime)/1000
        frameslist.append(int(framenumber))
    return frameslist


"""Fixes any problems with data"""
#data: all of the data values
#dataToConvert: Types of data to convert from degrees to radians
def dataFix(data, dataToConvert):
    for dataType in dataToConvert:
        dataValues = data[dataType]
        dataValuesNew = []
        for value in dataValues:
            dataValuesNew.append(math.radians(value))
        data[dataType] = dataValuesNew
    
    if invertPitch:
        dataValuesNew = []
        for value in data['Pitch']:
            dataValuesNew.append(-value)
        data['Pitch'] = dataValuesNew
        

"""Key frame all of the RPY data in the visualizer model"""
#data: data set that contains Roll Pitch Yaw values
def keyFrameRollPitchYaw(data):
    bpy.ops.object.select_all(action='DESELECT')    
    ob = bpy.data.objects.get("RotationDisplay")
    
    for i in range(len(data['KeyFrame'])):
        ob.rotation_euler = [data['Roll'][i], data['Pitch'][i], data['Yaw'][i]]
        ob.keyframe_insert(data_path = "rotation_euler", frame = data['KeyFrame'][i])
        
    for curve in ob.animation_data.action.fcurves:
        for kf in curve.keyframe_points:
            kf.interpolation = 'BEZIER'

"""Sets the end of the scene based on keyframe values"""
#data: data set that contains keyframes
def setEndOfAnimation(data):
    lastFrame = data['KeyFrame'][len(data['KeyFrame'])-1]
    bpy.context.scene.frame_end = lastFrame


"""Sets up the handler for the text"""
#Defines the needed global values and adds the handler
def setupText(data, config):
    global dataGlobal
    global textOptionsGlobal
    
    dataGlobal = data

    if config.get('Text', 'Upper Right') != 'None':
        textOptionsGlobal['URText'] = textOpt[config.get('Text', 'Upper Right')]
    if config.get('Text', 'Upper Left') != 'None':
        textOptionsGlobal['ULText'] = textOpt[config.get('Text', 'Upper Left')]
    if config.get('Text', 'Lower Right') != 'None':
        textOptionsGlobal['LRText'] = textOpt[config.get('Text', 'Lower Right')]
    if config.get('Text', 'Lower Left') != 'None':
        textOptionsGlobal['LLText'] = textOpt[config.get('Text', 'Lower Left')]
    
    bpy.app.handlers.frame_change_pre.append(doText)

"""A handler for the text. Changes the text based on current frame"""
#Requires following globals
#dataGlobal: data for all text
#textOptionsGlobal: what to display where
def doText(scene):
    global dataGlobal
    global textOptionsGlobal
    frame =  scene.frame_current
    index = min(range(len(dataGlobal['KeyFrame'])), key=lambda i: abs(dataGlobal['KeyFrame'][i]-frame))

    for i, func in textOptionsGlobal.items():
        bpy.ops.object.select_all(action='DESELECT')    
        ob = bpy.data.objects.get(i)
        ob.data.body = func(dataGlobal, index)


"""Handle rendering image or video"""
def handleRender(Config, root):
    bpy.data.scenes['Scene'].render.resolution_x = int(Config.get('Render', 'Resolution X'))
    bpy.data.scenes['Scene'].render.resolution_y = int(Config.get('Render', 'Resolution Y'))
    bpy.data.scenes['Scene'].render.fps = FramesPerSecond
    if Config.get('Render', 'Type') == 'Image':
        bpy.data.scenes['Scene'].render.filepath = os.path.join(root, 'images', 'render.png')
        bpy.ops.render.render( write_still=True )
    elif Config.get('Render', 'Type') == 'Video':
        bpy.data.scenes['Scene'].render.filepath = os.path.join(root, 'videos', 'render.avi')
        bpy.data.scenes['Scene'].render.image_settings.file_format = 'AVI_JPEG'
        bpy.ops.render.opengl( animation = True, write_still = True)

def exitBlender():
    bpy.ops.wm.quit_blender()
def keyFrameGPSMap(Frames):    
    global Lats
    global Longs
    global scalemap
    global Alts
    bpy.ops.object.select_all(action='DESELECT')    
    ob = bpy.data.objects.get("GPSMAP")
    centerOfMap = [ob.location[0], ob.location[2]]
    mapWidth = ob.dimensions[0]
    mapHeight = ob.dimensions[2]
    mapGPSWidth = LowerRightGPSMAP[1] - UpperLeftGPSMAP[1]
    mapGPSHeight = UpperLeftGPSMAP[0] - LowerRightGPSMAP[0]
    
    scalemap = mapWidth/distancecrossmap
    coords = []    
    edges = []
    
    bpy.ops.object.select_all(action='DESELECT')    
    ob = bpy.data.objects.get("GPSMAPGLIDER")
    for i in range(len(Frames)):
        offsetLat = Lats[i] - CenterGPSMAP[0]
        offsetLong = Longs[i] - CenterGPSMAP[1]
        worldCoords = [centerOfMap[0] + offsetLong*mapWidth/mapGPSWidth, ob.location[1],  centerOfMap[1] + offsetLat*mapHeight/mapGPSHeight]
        ob.location = worldCoords
        HeightCoords = [worldCoords[0], Alts[i]*scalemap/100, worldCoords[2]]
        
        coords.append(HeightCoords)
        ob.rotation_euler = [3.1415/2,Yaws[i],0]
        ob.keyframe_insert(data_path = "location", frame = Frames[i])
        ob.keyframe_insert(data_path = "rotation_euler", frame = Frames[i])
    for coord in range(len(coords)-1):
        edges.append([coord,coord+1])
    faces = []
    me = bpy.data.meshes.new("PathMesh")   # create a new mesh  
 
    ob = bpy.data.objects.new("Path", me)          # create an object with that mesh
    ob.location = bpy.context.scene.cursor_location   # position object at 3d-cursor
    bpy.context.scene.objects.link(ob)                # Link object to scene
     
    # Fill the mesh with verts, edges, faces 
    me.from_pydata(coords,edges,faces)   # edges or faces should be [], or you ask for problems
    me.update(calc_edges=True)    # Update mesh with new data  


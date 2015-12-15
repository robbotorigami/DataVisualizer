import bpy
import bpy.ops as B
import mathutils
from mathutils import Vector
import math
from math import radians
from decimal import *
import csv

"""These are controls"""
#File to read from
FramesPerSecond = 30
#These are the upper left and lower right lat longs of the gps map
LowerRightGPSMAP = [38.160025,-104.801775]
UpperLeftGPSMAP = [38.168844,-104.816625]
CenterGPSMAP = [(LowerRightGPSMAP[0]+UpperLeftGPSMAP[0])/2,(LowerRightGPSMAP[1]+UpperLeftGPSMAP[1])/2]
distancecrossmap = 1298
scalemap = 0

#Row definitions


""" function that reads all data from csv file"""
#Usage:
#importFile: contains file path to the data file
#dataToInclude: list of what data is in the files 
def readIntoLists(importFile, dataToInclude):
    Times = []
    Rolls = []
    Pitches = []
    Yaws = []
    Alts = []
    
    with open(importFile, 'r') as dataFile:
        iterator = csv.reader(dataFile, delimiter=',', quotechar='|')
        for row in iterator:
            if 'Time' in dataToInclude:
                Times.append(float(row[0]))
            if 'Euler' in dataToInclude:
                Rolls.append(float(row[1]))
                Pitches.append(float(row[2]))
                Yaws.append(float(row[3]))
            if 'Altitude' in dataToInclude:
                Alts.append(float(row[4]))

    if 'Time

def createKeyframeList():
    startingTime = Times[0]
    frameslist = []
    for time in Times:
        framenumber = (time-startingTime)*FramesPerSecond/1000
        frameslist.append(int(framenumber))
    return frameslist

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
    
        
    
def keyFrameRollPitchYaw(Frames):
    global Rolls
    global Pitches
    global Yaws    
    bpy.ops.object.select_all(action='DESELECT')    
    ob = bpy.data.objects.get("BIGGLIDER")
    
    for i in range(len(Frames)):
        ob.rotation_euler = [Pitches[i], Rolls[i], Yaws[i]]
        ob.keyframe_insert(data_path = "rotation_euler", frame = Frames[i])
    ob.rotation_euler = [0,0,0]
    ob.keyframe_insert(data_path = "rotation_euler", frame = 0)

def doText(scene):
    global States
    global Times
    global Rolls
    global Pitches
    global Yaws
    global FixTimes
    global Lats
    global Longs
    global VelocityMag
    global VelocityDir
    global Sats
    global Alts
    global keyFrames
    frame =  scene.frame_current
    if keyFrames.count(frame) != 0:
        i = keyFrames.index(frame)
        bpy.ops.object.select_all(action='DESELECT')    
        ob = bpy.data.objects.get("RPYText")
        ob.data.body = "Roll:" + str(Rolls[i]) + " Pitch:" + str(Pitches[i]) + " Yaw:" + str(Yaws[i])
        
        bpy.ops.object.select_all(action='DESELECT')    
        ob = bpy.data.objects.get("LATLONGText")
        ob.data.body = "Lat:" + str(Lats[i]) + " Long:" + str(Longs[i])
        
        bpy.ops.object.select_all(action='DESELECT')    
        ob = bpy.data.objects.get("StatusText")
        ob.data.body = StatusMessages[States[i]]
        
        bpy.ops.object.select_all(action='DESELECT')    
        ob = bpy.data.objects.get("ALTText")
        ob.data.body = str(Alts[i]/100) + "m / " + str(round(Alts[i]/30.48,2)) +"ft"
        
    
    
readIntoGlobalVars()
keyFrames = createKeyframeList()
keyFrameGPSMap(keyFrames)    
keyFrameRollPitchYaw(keyFrames)


def my_handler(scene):
    frame = scene.frame_current
 
    if frame > len(char_list):
        current_string = char_list[-1]
 
    current_string = char_list[frame]
    bpy.data.objects['Text'].data.body = current_string
 
for i in bpy.app.handlers.frame_change_pre:
    bpy.app.handlers.frame_change_pre.pop() 
bpy.app.handlers.frame_change_pre.append(doText)      
print(len(bpy.app.handlers.frame_change_pre))

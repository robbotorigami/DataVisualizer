import sys
import os
root = os.path.dirname(__file__)
sys.path.append(root)

import datavisualizer as dv
import configparser

#Setup Config File

Config = configparser.ConfigParser()
Config.read(os.path.join(root,'Settings.ini'))

#Read Model
model = Config.get('Settings', 'Model')
modelFile = os.path.join(root, 'models', model)
dv.importModel(modelFile)

#Read data
datacsv = Config.get('Settings', 'Data')
timeStep = float(Config.get('Settings', 'TimeStep'))
dataFile = os.path.join(root, 'data', datacsv)
dataToRead = ['Time', 'Roll', 'Pitch', 'Yaw', 'Altitude']
data = dv.readIntoLists(dataFile, dataToRead, timeStep)

#Convert data that should be in radians from degrees
dv.dataFix(data, ['Roll','Pitch','Yaw'])

#Create the list of keyframes for all the timestamps
dv.FramesPerSecond = int(Config.get('Settings', 'FPS'))
timeScale = float(Config.get('Settings', 'Speed Factor'))
framesList = dv.createKeyframeList(data['Time'], timeStep, timeScale)

#Keyframe the rotation data on the model
data['KeyFrame'] = framesList
dv.keyFrameRollPitchYaw(data)

#Set the end of the animation
dv.setEndOfAnimation(data)

#Setup the text
dv.setupText(data, Config)

#Render the desired output
dv.handleRender(Config, root)

#Exit
dv.exitBlender()

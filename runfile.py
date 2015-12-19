import sys
import os
root = os.path.dirname(__file__)
print('------------------------OUTPUT------------------')
print(root)
print('------------------------------------------------')
sys.path.append(root)

import datavisualizer
import configparser

Config = configparser.ConfigParser()
Config.read(os.path.join(root,'Settings.ini'))

model = Config.get('Settings', 'Model')

file = os.path.join(root, 'models', model)

datavisualizer.importModel(file)

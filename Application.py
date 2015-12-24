import os
import tkinter
from tkinter.messagebox import *
from Definitions import *
import configparser

class simpleapp_tk(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.root = os.path.dirname(__file__)

        frame1 = tkinter.Frame(self)
        frame1.grid(column = 0,row=0, sticky = 'NEW')

       
        self.setupLabel(frame1, 0,0,"Choose Data File:")
        self.file = tkinter.StringVar()
        self.fileList = tkinter.OptionMenu(frame1, self.file,"")
        self.fileList.grid(column = 0, row=1)
        
        self.populateDataSelection()

        button = tkinter.Button(frame1, text=u"Refresh Files", command = self.populateDataSelection)
        button.grid(column=1, row=1, sticky = 'E')

        self.setupLabel(frame1, 0,2,"Choose Model File:")
        self.model = tkinter.StringVar()
        self.modelList = tkinter.OptionMenu(frame1, self.model, "")
        self.modelList.grid(column = 0, row = 3)

        self.populateModelSelection()

        button2 = tkinter.Button(frame1, text=u"Refresh Models", command = self.populateModelSelection)
        button2.grid(column = 1, row=3, sticky = 'E')

        frame2 = tkinter.Frame(self)
        frame2.grid(column = 2,row =0, padx =5, sticky = 'N')

        dataOptions = [key for key in textOpt]
        dataOptions.append("None")
        
        self.ULData = tkinter.StringVar(self)
        self.ULData.set("None")
        self.URData = tkinter.StringVar(self)
        self.URData.set("None")
        self.LLData = tkinter.StringVar(self)
        self.LLData.set("None")
        self.LRData = tkinter.StringVar(self)
        self.LRData.set("None")

        self.setupLabel(frame2, 0,0,"Select Text Options:")
        
        ULMenu = tkinter.OptionMenu(frame2, self.ULData, *dataOptions)
        ULMenu.grid(column = 1, row=1, sticky ='W')

        URMenu = tkinter.OptionMenu(frame2, self.URData, *dataOptions)
        URMenu.grid(column = 1, row=2, sticky ='W')

        LLMenu = tkinter.OptionMenu(frame2, self.LLData, *dataOptions)
        LLMenu.grid(column = 1, row=3, sticky ='W')

        LRMenu = tkinter.OptionMenu(frame2, self.LRData, *dataOptions)
        LRMenu.grid(column = 1, row=4, sticky ='W')

        self.setupLabel(frame2,0,1,"Upper Left Display:")
        self.setupLabel(frame2,0,2,"Upper Right Display:")
        self.setupLabel(frame2,0,3,"Lower Left Display:")
        self.setupLabel(frame2,0,4,"Lower Right Display:")

        frame3 = tkinter.Frame(self)
        frame3.grid(column = 1, row = 0, padx = 5, sticky = 'N')

        self.setupLabel(frame3, 0, 0, "Data import options")
        self.setupLabel(frame3, 0, 1, "Minimum Time Step:")
        self.setupLabel(frame3, 0, 2, "Speed Multiplier:")
        self.timeStep = tkinter.StringVar()
        self.timeStepEntry = tkinter.Entry(frame3, textvariable=self.timeStep)
        self.timeStepEntry.grid(column = 1, row = 1, sticky ='EW')
        self.timeStep.set("10")
        self.timeScale = tkinter.StringVar()
        self.timeScaleEntry = tkinter.Entry(frame3, textvariable=self.timeScale)
        self.timeScaleEntry.grid(column = 1, row = 2, sticky ='EW')
        self.timeScaleEntry.bind("<Return>", self.checktimeScale)
        self.timeScale.set("1.00")

        frame4 = tkinter.Frame(self)
        frame4.grid(column = 0, row = 1, sticky = 'NW')

        self.setupLabel(frame4, 0,0, "Render Settings")
        self.renderType = tkinter.StringVar()
        renderOptions = tkinter.OptionMenu(frame4, self.renderType,"Image", "Video")
        renderOptions.grid(column =1, row = 1)
        
        self.renderType.set("Video")
        self.setupLabel(frame4, 0,1, "Render Type:", 'E')
        self.setupLabel(frame4, 0,2, "Frame Rate:", 'E')
        self.setupLabel(frame4, 0,3, "Resolution:", 'E')

        resFrame = tkinter.Frame(frame4)
        resFrame.grid(column = 1, row = 3, sticky = 'EW')

        self.resolutionx = tkinter.StringVar()
        self.resolutiony = tkinter.StringVar()

        resxEntry = tkinter.Entry(resFrame, textvariable=self.resolutionx, width = 4)
        resxEntry.grid(column = 0, row =0, sticky = 'W')
        resxEntry.bind("<Return>", self.checkResolution)
        self.setupLabel(resFrame, 1,0, " x ")
        resyEntry = tkinter.Entry(resFrame, textvariable=self.resolutiony, width = 4)
        resyEntry.grid(column = 2, row =0, sticky = 'W')
        resyEntry.bind("<Return>", self.checkResolution)

        self.resolutionx.set("854")
        self.resolutiony.set("480")

        self.frameRate = tkinter.StringVar()
        frameRateEntry = tkinter.Entry(frame4, textvariable=self.frameRate, width = 4)
        frameRateEntry.grid(column = 1, row = 2, sticky = 'EW')
        frameRateEntry.bind("<Return>", self.checkFPS)
        self.frameRate.set("30")

        renderFrame = tkinter.Frame(self)
        renderFrame.grid(column = 1, row = 1, columnspan = 2)
        
        finishButton = tkinter.Button(renderFrame, text = "Run Render", command = self.RunRender)
        finishButton.grid(column = 0, row = 0)
        
        
    def checktimeScale(self, event):
        if float(self.timeScale.get()) <= 0:
            showerror('Ok', "Time Scale must be greater than 0")
            self.timeScale.set("1.00")
            return False
        return True

    def checkFPS(self, event):
        fps = int(self.frameRate.get())
        if fps < 1 or fps > 60:
            showerror('Ok', "Frame Rate must be between 1`and 60")
            fps = 30
            return False
        self.frameRate.set(fps)
        return True
        
    def checkResolution(self, event):
        resx = int(self.resolutionx.get())
        resy = int(self.resolutiony.get())
        if resx < 170 or resx > 2000 or resy < 100 or resy > 1200:
            showerror('Ok', "Resolution must be between 170x100 and 2000x1200")
            resx = 854
            resy = 480
            return False
        self.resolutionx.set(str(resx))
        self.resolutiony.set(str(resy))
        return True

    def populateDataSelection(self):
        menu = self.fileList['menu']
        menu.delete(0, "end")
        files = self.find_csv_filenames(os.path.join(self.root,"data"))
        print(files)
        for file in files:
            menu.add_command(label=file, command=lambda file=file: self.file.set(file))
        self.file.set(files[0])
        
    def populateModelSelection(self):
        menu = self.modelList['menu']
        menu.delete(0, "end")
        files = self.find_obj_filenames(os.path.join(self.root,"models"))
        print(files)
        for file in files:
            menu.add_command(label=file, command=lambda file=file: self.model.set(file))
        self.model.set(files[0])
    
    def find_csv_filenames( self, path_to_dir, suffix=".csv" ):
        filenames = os.listdir(path_to_dir)
        return [ filename for filename in filenames if filename.endswith( suffix ) ]

    def find_obj_filenames( self, path_to_dir, suffix=".obj" ):
        filenames = os.listdir(path_to_dir)
        return [ filename for filename in filenames if filename.endswith( suffix ) ]

    def setupLabel(self, master, c, r, text, s ='EW'):
        labelText = tkinter.StringVar()
        labelText.set(text)
        label = tkinter.Label(master, textvariable=labelText)
        label.grid(column = c, row=r, sticky = s)

    def RunRender(self):
        Config = configparser.ConfigParser()
        Config.read(os.path.join(self.root,'Settings.ini'))

        if self.checktimeScale(None):
            if self.checkFPS(None):
                if self.checkResolution(None):
                    Config['Settings']['Model'] = self.model.get()
                    Config['Settings']['Data'] = self.file.get()
                    Config['Settings']['TimeStep'] = self.timeStep.get()
                    Config['Settings']['FPS'] = self.frameRate.get()
                    Config['Settings']['Speed Factor'] = self.timeScale.get()

                    Config['Text']['Lower Right'] = self.LRData.get()
                    Config['Text']['Lower Left'] = self.LLData.get()
                    Config['Text']['Upper Right'] = self.URData.get()
                    Config['Text']['Upper Left'] = self.ULData.get()

                    Config['Render']['Type'] = self.renderType.get()
                    Config['Render']['Resolution X'] = self.resolutionx.get()
                    Config['Render']['Resolution Y'] = self.resolutiony.get()
                    with open('Settings.ini', 'w') as configfile:
                        Config.write(configfile)
                    
                    os.system("Blender\\blender.exe Original.blend --python runfile.py > blenderlog.txt")
                    os.system("timeout /t -1")


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Data Visualization')
    app.mainloop()



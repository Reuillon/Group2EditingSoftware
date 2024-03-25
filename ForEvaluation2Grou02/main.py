import tkinterdnd2
import shutil
from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import Image,ImageTk
from dataclasses import dataclass
import mouse
import os
import sys

isRender = 0
isPlaying = 1

currentProject = "empty!\\"

window = tkinterdnd2.Tk()
window.state('withdrawn')
window.geometry('0x0')

projSelect = Tk()

nameC = Tk()
nameC.geometry('0x0')
nameC.state('withdrawn')



screen_height = window.winfo_screenheight()
screen_width  = window.winfo_screenwidth()

vIcon = ImageTk.PhotoImage(Image.open("icons/video.png"))
fIcon = ImageTk.PhotoImage(Image.open("icons/file.png"))
aIcon = ImageTk.PhotoImage(Image.open("icons/audio.png"))
rIcon = ImageTk.PhotoImage(Image.open("icons/render.png"))
tIcon = ImageTk.PhotoImage(Image.open("icons/timeline.png"))
pIcon = ImageTk.PhotoImage(Image.open("icons/play.png"))
sIcon = ImageTk.PhotoImage(Image.open("icons/fast.png"))
bIcon = ImageTk.PhotoImage(Image.open("icons/rev.png"))

selectedElement = -1

canvas = Canvas(window, width=screen_width, height=screen_height, highlightthickness=0)

selected = -4

tabIni = 0

mode = 0

toggle = 1
toggleEx = 1
toggleSh = 1

centerPos = 0

def donothing():
   print()

projFiles = 0

####

textFont = 20;

scale = 60

#CLASS FOR COLOR SCHEME
@dataclass
class colorScheme:
    background: str
    light: str
    dark: str
    highlighted: str
    
#Class for button locations
@dataclass
class button():
    pX = 0
    pY = 0
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.pX = (x1 + x2) / 2
        self.pY = (y1 + y2) / 2
@dataclass
class element():
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

elementStack = []


x = 1
y = 1

#colors
color = colorScheme
color.background = '#1B1F38';
color.light = '#273044';
color.dark = '#0E1628'
color.highlighted = '#5A667F';
color.screen = '#000000';

elementsInTimeline = 0

#Buttons
####
####
####

fSys = button(0, (screen_width/6) / 4, (2*screen_height/3) + screen_height/30, (2*screen_height/3))

vid = button((screen_width/6) / 4,2*(screen_width/6)  / 4,  (2*screen_height/3) + screen_height/30, (2*screen_height/3))

audio = button(2 * (screen_width/6) / 4,3*(screen_width/6)  / 4,(2*screen_height/3) + screen_height/30, (2*screen_height/3))

exp = button(3 * (screen_width/6) / 4, (screen_width/6),(2*screen_height/3) + screen_height/30, (2*screen_height/3))

####
####
####

playerPercentage = 0

def highlight(x1,x2,y1,y2):
    
    if(x > x1 and x < x2) and (y > y1 and y < y2):
        canvas.create_rectangle(x1, y1, x2, y2, fill=color.highlighted)

def listProjects():
    if not os.path.exists("projects"):
        os.makedirs("projects")
    dir_list = os.listdir("projects")
    return dir_list

def printInput(): 
    global currentProject
    inp = title.get(1.0, "end-1c") 
    if inp == '':
        inp = 'project'
    currentProject = str(inp)
    create()


def fileClick(x1,x2,y1,y2):
    global elementStack
    global selected
    if(x > x1 and x < x2) and (y > y1 and y < y2):
        if (mode == 1 or mode == 2):
            tot = len(elementStack)
            elementStack.append(element((0 + (screen_width / 100)) + 250 * tot  , (250)))    
            return False
        return True
    else:
        return False
        
        
title = Text(nameC, height = 1, width = 60)

def newProject():
    global tabIni
    if (tabIni <1):
        tabIni = 1
        
        nameC.state('normal')
        nameC.overrideredirect(True)

        nameC.geometry('500x120')
        nameC.geometry('%dx%d+%d+%d' % (500, 100, (screen_width/2) - 250, (screen_height/2) +250))
        nameC.configure(background=color.light)
    
        label = Label(nameC, text = "Project Name:", bg = color.light, fg = '#ffffff')
        label.config(font = ("Helvetica", textFont))
        creatBtn = Button(nameC, text = 'Create', bd = '5', command = printInput) 
        creatBtn.pack() 
        label.pack()
        title.pack()
        creatBtn.place(x=250 - 20, y=60)



def drawTimeLineElements():
    global toggle
    global selectedElement
    global elementStack
    tY = ((2*screen_height/3) + screen_height/30) + screen_height / 50
    bY = (screen_height) - (screen_height / 20)
    centerPos = (tY + bY) /2
    
    
    if (toggle == -1):
        elementStack[selectedElement].x1 = x - (elementStack[selectedElement].x2)/2
   
    for i in range(len(elementStack)):
        
        canvas.create_rectangle(elementStack[i].x1, centerPos , elementStack[i].x1 + elementStack[i].x2, centerPos + screen_height/30 , fill='green')
    

def sideFile():
    bX1 = screen_width - (screen_width / 100)
    bX2 = screen_width - (screen_width/6 - (screen_width / 100))
    bY1 = 0 + screen_height / 50
    bY2 = (2*screen_height/3) - (screen_height / 50)
        
    canvas.create_rectangle(bX1, bY1, bX2 , bY2, fill="#666688",  )
    
def parse(parsed):
    newString=""
    for i in range(len(parsed)):
        newString = newString + parsed[i]
        if i % 4 == 0 and i != 0:
            newString = newString + '\n' 
    return (newString)
    
def displayFiles(orientation):
    global currentProject
    global projFiles
    global selected
    projFiles = os.listdir("projects/" + str(currentProject) + "/files")
    
    
    if orientation == 0:
        canvas.create_rectangle((scale * selected) + scale - 50, ((2*screen_height/3) + screen_height/30) + scale - 60, (scale * selected) + scale + 10, ((2*screen_height/3) + screen_height/30) + scale + 50, fill=color.highlighted)
        for i in range(len(projFiles)):
            newValue = parse(str(projFiles[i]))
            highlight((scale * i) + scale - 50,(scale * i) + scale + 10, ((2*screen_height/3) + screen_height/30) + scale - 60, ((2*screen_height/3) + screen_height/30) + scale + 50)
            if projFiles[i].__contains__('.') == False: 
                canvas.create_image((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale - 25,image=fIcon)
                canvas.create_text((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale + 20, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
            elif projFiles[i].__contains__('.mp4'):
                canvas.create_image((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale - 25,image=vIcon)
                canvas.create_text((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale + 20, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
            elif projFiles[i].__contains__('.mp3'):
                canvas.create_image((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale - 25,image=aIcon)    
                canvas.create_text((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale + 20, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
            elif projFiles[i].__contains__('.tm'):
                canvas.create_image((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale - 25,image=tIcon)
                canvas.create_text((scale * i) + scale - 20, ((2*screen_height/3) + screen_height/30) + scale + 20, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
    else:
        for i in range(len(projFiles)):
            newValue = parse(str(projFiles[i]))
            highlight(screen_width - 110,screen_width - 50, (60 + (60* i)) * 2 , ((120 ) + (60* i)) * 2)
            if projFiles[i].__contains__('.') == False:  
                canvas.create_image(screen_width - 80,  (((screen_height/30)  + (screen_height/60) + scale * i)) *2 + textFont,image=fIcon)
                canvas.create_text(screen_width - 80, (((screen_height/30)  + (screen_height/60) + scale * i)) *2 + textFont + 45, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
            elif projFiles[i].__contains__('.mp4'):
                canvas.create_image(screen_width - 80,  (((screen_height/30)  + (screen_height/60) + scale * i)) *2 + textFont,image=vIcon)
                canvas.create_text(screen_width - 80, (((screen_height/30)  + (screen_height/60) + scale * i)) *2 + textFont + 45, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
            elif projFiles[i].__contains__('.mp3'):
                canvas.create_image(screen_width - 80,  (((screen_height/30) + (screen_height/60) + scale * i)) *2 + textFont,image=aIcon)   
                canvas.create_text(screen_width - 80, (((screen_height/30)  + (screen_height/60) + scale * i)) *2 + textFont + 45, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
            elif projFiles[i].__contains__('.tm'):
                canvas.create_image(screen_width - 80,  (((screen_height/30)  + (screen_height/60) + scale * i)) *2 + textFont,image=tIcon)
                canvas.create_text(screen_width - 80, (((screen_height/30)  + (screen_height/60) + scale * i)) *2 + textFont + 45, text=newValue, font=('Helvetica ' + str(12) + ' bold'), fill =  'white')
    
def create():
    global currentProject
    if not os.path.exists("projects/" + str(currentProject)):
        os.makedirs("projects/" + str(currentProject))
    if not os.path.exists("projects/" + str(currentProject) + "/files"):
        os.makedirs("projects/" + str(currentProject) + "/files")
    
    f = open("projects/" + str(currentProject) + "/" + currentProject + ".proj", "w")
    f.write("SAMPLE TEXT")
    f.close()
    
    initialize()
    projSelect.destroy()

def reset():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

def loadProject():
    global currentProject
    global elementStack
    
    f = open("projects/" + str(currentProject) + "/" + currentProject + ".proj", "w")
    f.write("3")
    f.write("680")
    f.write("240")
    f.write("24")
    f.write("h.264")
    f.close()
    
    f = open("projects/" + str(currentProject) + "/files/" + 'timeline' + ".tm", "r")
    data = f.readlines()
    
    for i in range(5,len(data),2): 
        elementStack.append(element(float(data[i]) , float(data[i+1]) ))
    
        
    initialize()
    projSelect.destroy()

def saveTimeline():
    f = open("projects/" + str(currentProject) + "/files/" + 'timeline' + ".tm", "w")
    f.write("3\n")
    f.write("680\n")
    f.write("240\n")
    f.write("24\n")
    f.write("h.264\n")
    for i in range(len(elementStack)):
        f.write(str(elementStack[i].x1) + "\n")
        f.write(str(elementStack[i].x2) + "\n")
    f.close()

def drawIcons():
    canvas.create_image(fSys.pX,fSys.pY,image=fIcon)
    canvas.create_image(vid.pX,vid.pY,image=vIcon)
    canvas.create_image(audio.pX,audio.pY,image=aIcon)
    canvas.create_image(exp.pX,exp.pY,image=rIcon)    

def displayContents():

    if projFiles[selected].__contains__('.') == False:
        return
    if mode != 0:
        return
    bX1 = 0 + screen_width / 100
    bX2 = screen_width/6 - (screen_width / 100)
    bY1 = 0 + screen_height / 50
    bY2 = (2*screen_height/3) - (screen_height / 50)
        
    canvas.create_rectangle(bX1, bY1, bX2 , bY2, fill="#4B5577", outline='#000000' ,width=1.5)
    
    fileRead = open("projects/" + str(currentProject) + "/files/" + projFiles[selected] , "r")
    var = fileRead.readlines()
    fileRead.close()
    canvas.create_text((bX1 + bX2) / 2, (bY1 + screen_height / 25), fill="white", text= 'Clip Information', font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 2), fill="white", text= 'Length: ' + var[0].strip() + ':00', font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 3), fill="white", text= 'Resolution:', font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 4.5), fill="white", text= 'X: ' + var[1] + "Y: " + var[2] , font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 6), fill="white", text= 'Framerate: ' + var[3] , font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 7), fill="white", text= 'Encoding: ' + var[4] , font=('Helvetica ' + str(textFont)))


def timelineInfo():
    
    bX1 = 0 + screen_width / 100
    bX2 = screen_width/6 - (screen_width / 100)
    bY1 = 0 + screen_height / 50
    bY2 = (2*screen_height/3) - (screen_height / 50)
    canvas.create_rectangle(bX1, bY1, bX2 , bY2, fill="#4B5577", outline='#000000' ,width=1.5)
   
        
    canvas.create_text((bX1 + bX2) / 2, (bY1 + screen_height / 25), fill="white", text= 'Timeline', font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 2), fill="white", text= 'Length: ' + "3" + ':00', font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 3), fill="white", text= 'Resolution:', font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 4.5), fill="white", text= 'X: ' + "640" + "Y: " + "480" , font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 6), fill="white", text= 'Framerate: ' + "30" , font=('Helvetica ' + str(textFont)))
    canvas.create_text((bX1 + bX2) / 2, (bY1 + (screen_height / 25) * 7), fill="white", text= 'Encoding: ' + 'h.264', font=('Helvetica ' + str(textFont)))

def setstring(path):
    global currentProject
    currentProject = path
    loadProject()

def createTimeline():
    print("created timeline!")
    f = open("projects/" + str(currentProject) + "/files/" + 'timeline' + ".tm", "w")
    f.write("3\n")
    f.write("680\n")
    f.write("240\n")
    f.write("24\n")
    f.write("h.264\n")
    f.close()

pPosition = screen_width /6 + (screen_width) / 200

def playerPos():
    global pPosition
    global playerPercentage
    if pPosition < screen_width /6 + (screen_width) / 200:
        pPosition = screen_width /6 + (screen_width) / 200
    elif pPosition > 5 * screen_width /6 - (screen_width) / 200:
        pPosition = 5 * screen_width /6 - (screen_width) / 200      

    total = (5 * screen_width /6 - (screen_width) / 200) - (screen_width /6 + (screen_width) / 200)
    total = (total * playerPercentage) + (screen_width /6 + (screen_width) / 200)
            
    pointer = canvas.create_rectangle(total - (screen_width) / 500, (2*screen_height/3) - (screen_height/30 *1.5) + (screen_height) / 300 , total + (screen_width) / 500, (2*screen_height/3)  - screen_height/30 - (screen_height) / 300, fill='#FFFFFF')   
    

def player():
    
    #clip screen
    screen = canvas.create_rectangle(screen_width /6, 0, 5 * screen_width /6, (2*screen_height/3) - screen_height/30, fill=color.screen)   
    
        
    player = canvas.create_rectangle(screen_width /6, (2*screen_height/3) - screen_height/30, 5 * screen_width /6, (2*screen_height/3), fill='#777777')   
    scrubberBorder = canvas.create_rectangle(screen_width /6, (2*screen_height/3) - (screen_height/30 *1.5), 5 * screen_width /6, (2*screen_height/3)  - screen_height/30, fill='#444444')   
    scrubber = canvas.create_rectangle(screen_width /6 + (screen_width) / 200, ((2*screen_height/3) - (screen_height/30)) - (screen_height/ 100) * 0.7  , 5 * screen_width /6 - (screen_width) / 200, ((2*screen_height/3)  - (screen_height/30) * 1.1  ) - (screen_height/ 100) * 0.7, fill='#000000')   
    
    highlight(((screen_width /6 + (5 * screen_width /6)) / 2 ) - 60, ((screen_width /6 + (5 * screen_width /6)) / 2 ) + 10, ((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) - 20,((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) + 20)    
    canvas.create_image(((screen_width /6 + (5 * screen_width /6)) / 2 ) - 20, (((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2 ,image=pIcon)
    highlight(((screen_width /6 + (5 * screen_width /6)) / 2 ) + 10, ((screen_width /6 + (5 * screen_width /6)) / 2 ) + 70, ((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) - 20,((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) + 20)    
    highlight(((screen_width /6 + (5 * screen_width /6)) / 2 ) - 110, ((screen_width /6 + (5 * screen_width /6)) / 2 ) - 50, ((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) - 20,((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) + 20)    
    
    canvas.create_image(((screen_width /6 + (5 * screen_width /6)) / 2 ) - 80, (((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2 ,image=bIcon)
   
    canvas.create_image(((screen_width /6 + (5 * screen_width /6)) / 2 ) + 40, (((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2 ,image=sIcon)
    
    playerPos()

def drawMain():
    player()
    #TITLE BAR
    canvas.create_rectangle(screen_width, (2*screen_height/3) + screen_height/30, screen_width/6, (2*screen_height/3), fill=color.dark)
   

def startApplication():
    projSelect.title("Select Project") 
    projSelect.geometry('%dx%d+%d+%d' % (500, 500, (screen_width/2) - 250, (screen_height/2) - 250))
    projSelect.overrideredirect(True)
    projSelect.configure(background=color.light)
    

    dir = listProjects()
    proj = [0] * len(dir)
    projCanvas = Canvas(projSelect, width=500, height=500, highlightthickness=1)
    projCanvas.configure(bg=color.light)
    projCanvas.create_rectangle(0, 0, 500, 50, fill=color.dark)
    textP = Label(projCanvas, text="Open Project:", fg = "white" ,bg=color.dark, font=("Helvetica", textFont))
    textP.place(x=(500/2) - ((len("Open Project:")) * textFont) + 20  ,y=5)

    projCanvas.pack()
    
    
    
    for x in range(len(dir)):

        action_with_arg = partial(setstring, dir[x])
        proj[x] = Button(projSelect, text = str(dir[x]), bd = '5', command = action_with_arg)
        proj[x].pack(side = 'top') 
        proj[x].place(x=10, y=(10 + (50 * (x + 1))))
   
    
    btn = Button(projSelect, text = 'New Project', bd = '5', command = newProject) 
    btn.pack(side = 'top') 
    btn.place(x=340, y=450)
    btn2 = Button(projSelect, text = 'Quit', bd = '5', command = projSelect.quit) 
    btn2.pack(side = 'top') 
    btn2.place(x=440, y=450)
    
m = Menu(window, tearoff = 0) 

def initialize():
    global canvas
    nameC.destroy()
    window.title("Video Editor: " + str(currentProject))
    
    #Get the current screen width and height
    resolution = str(screen_width) +  "x" + str(screen_height)
    window.state('zoomed')


    window.geometry(resolution)
    window.configure(background=color.background)
    
    canvas = Canvas(window, width=screen_width, height=screen_height)
    canvas.configure(bg=color.light)
    window.resizable(width=False, height=False)
    

    canvas.create_rectangle(fSys.x1, fSys.y1, fSys.x2, fSys.y2, fill=color.highlighted, outline='#000000' ,width=1.5)
    canvas.create_rectangle(vid.x1, vid.y1, vid.x2, vid.y2, fill=color.dark, outline='#000000' ,width=1.5)
    canvas.create_rectangle(audio.x1, audio.y1, audio.x2, audio.y2, fill=color.dark, outline='#000000' ,width=1.5)
    canvas.create_rectangle(exp.x1, exp.y1, exp.x2, exp.y2, fill=color.dark, outline='#000000' ,width=1.5)    
    
    m.add_command(label ="New Timeline", command = createTimeline) 
    
   
  
    drawMain()

    canvas.pack()

def drawTimeline():
    global playerPercentage
    
    lX = 0 + (screen_width / 100) 
    rX = screen_width - (screen_width / 100)
    tY = ((2*screen_height/3) + screen_height/30) + screen_height / 50
    bY = (screen_height) - (screen_height / 20)
    
    if mode == 1:
        canvas.create_rectangle(0, bY, screen_width, tY, fill='#BFCDFF' ,width=1.5) 
    elif mode == 2:
        canvas.create_rectangle(0, bY, screen_width, tY, fill='#FFD7D1' ,width=1.5)    
    for i in range(int(screen_width/10)):
        
        
        if i % 5 == 0:       
            canvas.create_rectangle(0 + (i * 10), tY, 0 + 2 + (i * 10), tY * 1.04, fill='#000000' )
        else:
            canvas.create_rectangle(0 + (i * 10), tY, 0 + 2 + (i * 10), tY * 1.02, fill='#000000' )
    
    drawTimeLineElements()
    
    total = rX - lX
    total = (total * playerPercentage)
    
    canvas.create_rectangle(lX + total  , tY , lX + 5 + total , bY, fill='#FF5D00')  
    canvas.create_rectangle(lX - 5 + total , tY - 10 , lX + 10 + total, tY + 10, fill='#FF5D00') 
    
    
def renderOutput():
    print("created timeline!")
    f = open("projects/" + str(currentProject) + "/files/" + 'output.' + "mp4", "w")
    f.write("3\n")
    f.write("680\n")
    f.write("240\n")
    f.write("24\n")
    f.write("h.264\n")
    f.close()
    messagebox.showinfo("Output", "Render Successful!") 


def update():
    global text
    global currentProject
    global selected
    time = 0
    
    
    
    if int((playerPercentage * 180) % 60) < 10:
        time = str(int(playerPercentage * 180 / 60)) + ":0" +  str(int((playerPercentage * 180) % 60))
    else:   
        time = str(int(playerPercentage * 180 / 60)) + ":" +  str(int((playerPercentage * 180) % 60))
    
    

    menubar = Menu(window)    
    if mode ==0:
        #menubar
        menubar = Menu(window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=reset)
        filemenu.add_command(label="Open", command=reset)
        filemenu.add_command(label="Save", command=saveTimeline)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=window.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        window.config(menu = menubar)
    else:
        menubar.destroy()
    if (currentProject == "empty!\\"):
        return    
        
    canvas.delete("all")
    
    drawMain() 
    
    
    if selected >= 0 and mode == 0:
        canvas.create_text(((screen_width /6 + (5 * screen_width /6)) / 2 ) - 20 - len(str(projFiles[selected])), (((audio.y2 + audio.y1)/2)), text=str(projFiles[selected]), fill="white", font=('Helvetica ' + str(textFont)))
        displayContents()
        
    if mode == 0:
        displayFiles(0)
        #draw buttons
        canvas.create_rectangle(fSys.x1, fSys.y1, fSys.x2, fSys.y2, fill=color.highlighted, outline='#000000' ,width=1.5)
        canvas.create_rectangle(vid.x1, vid.y1, vid.x2, vid.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(audio.x1, audio.y1, audio.x2, audio.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(exp.x1, exp.y1, exp.x2, exp.y2, fill=color.dark, outline='#000000' ,width=1.5)
            
    elif mode == 1:
        sideFile()
        displayFiles(1)
        drawTimeline()
        timelineInfo()
        canvas.create_rectangle(fSys.x1, fSys.y1, fSys.x2, fSys.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(vid.x1, vid.y1, vid.x2, vid.y2, fill=color.highlighted, outline='#000000' ,width=1.5)
        canvas.create_rectangle(audio.x1, audio.y1, audio.x2, audio.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(exp.x1, exp.y1, exp.x2, exp.y2, fill=color.dark, outline='#000000' ,width=1.5)    
    elif mode == 2:
        sideFile()
        displayFiles(1)
        drawTimeline()
        timelineInfo()
        canvas.create_rectangle(fSys.x1, fSys.y1, fSys.x2, fSys.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(vid.x1, vid.y1, vid.x2, vid.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(audio.x1, audio.y1, audio.x2, audio.y2, fill=color.highlighted, outline='#000000' ,width=1.5)
        canvas.create_rectangle(exp.x1, exp.y1, exp.x2, exp.y2, fill=color.dark, outline='#000000' ,width=1.5)    
    elif mode == 3:
        canvas.create_rectangle(fSys.x1, fSys.y1, fSys.x2, fSys.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(vid.x1, vid.y1, vid.x2, vid.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(audio.x1, audio.y1, audio.x2, audio.y2, fill=color.dark, outline='#000000' ,width=1.5)
        canvas.create_rectangle(exp.x1, exp.y1, exp.x2, exp.y2, fill=color.highlighted, outline='#000000' ,width=1.5)   
       
    
    if mode == 3:
        selected = -4
    
    
    highlight(fSys.x1, fSys.x2, fSys.y2, fSys.y1)
    highlight(vid.x1, vid.x2, vid.y2, vid.y1)
    highlight(audio.x1, audio.x2, audio.y2, audio.y1)
    highlight(exp.x1, exp.x2, exp.y2, exp.y1)
    
    
    #render Icone
    drawIcons()
    
    canvas.create_text(4*screen_width/5, fSys.y2 - screen_width/100, text=time, fill="white", font=('Helvetica ' + str(textFont)))
   
    if isPlaying == -1:
        canvas.create_text(screen_width/2, screen_height/2, text='Playing...', fill="white", font=('Helvetica ' + '30'))
    
   
    canvas.pack()    
    canvas.update_idletasks()




    
def elementInteract():
    global toggle
    global toggleEx
    global elementStack
    global selectedElement
    global centerPos
    
    for i in range(len(elementStack)):
        if x > (((elementStack[i].x2) + (elementStack[i].x1) + (elementStack[i].x1) )/2) - screen_width / 50 and x < (((elementStack[i].x2) + (elementStack[i].x1) + (elementStack[i].x1) )/2) + screen_width / 50 and y >  screen_height/30 *25 and y <  screen_height/30 *26: 
            toggle = toggle * -1
            selectedElement = i
        
        
    


def motion(event):
    global x
    global y
    x, y = event.x, event.y 
    update()

def drop(event):
    path = event.data
    fName = path.split('/')
    fName = fName[-1]
    shutil.copyfile(path, "projects/" + str(currentProject) + "/files/" + fName)

def checkClick():
    global x
    global y
    global mode
    global projFiles
    global selected
    global pPosition
    global playerPercentage
    global toggle
    global isRender
    global isPlaying
    
    if (x > (screen_width /6 + (5 * screen_width /6)) / 2 ) - 60 and x < ((screen_width /6 + (5 * screen_width /6)) / 2 ) + 10 and y > ((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) - 20 and y < ((((2*screen_height/3) - screen_height/30) + (2*screen_height/3)) / 2) + 20:
        isPlaying = isPlaying * -1
    
    #mode buttons
    if ((y > (2*screen_height/3) and y <  (2*screen_height/3) + screen_height/30) and (x < (screen_width/6) / 4)) and mode != 0:
        mode = 0
    if ((y > (2*screen_height/3) and y <  (2*screen_height/3) + screen_height/30) and (x > (screen_width/6) / 4 and x < 2 *(screen_width/6) / 4)) and mode != 1:
        mode = 1
    if ((y > (2*screen_height/3) and y <  (2*screen_height/3) + screen_height/30) and (x > 2 * (screen_width/6) / 4 and x < 3 * (screen_width/6) / 4)) and mode != 2:
        mode = 2
    if ((y > (2*screen_height/3) and y <  (2*screen_height/3) + screen_height/30) and (x > 3 * (screen_width/6) / 4 and x < (screen_width/6))) and mode != 3:
        mode = 3
    if not projFiles:
        return
    if (mode == 0):    
        for i in range(len(projFiles)):
            if fileClick((scale * i) + scale - 50,(scale * i) + scale + 10, ((2*screen_height/3) + screen_height/30) + scale - 60, ((2*screen_height/3) + screen_height/30) + scale + 10):
                selected = i
    elif (mode == 1 or mode == 2):    
        for i in range(len(projFiles)):
            if fileClick(28.5 * screen_width/30, 29.5 * screen_width/30, (i * 120) + 125,85 + (i * 120) + 125):
                print("CLICK")
                selected = i
    if mode == 3 and isRender ==0:
        isRender = 1
        renderOutput()
    if mode != 3:
        isRender = 0
    
    
    if (x > screen_width /6 + (screen_width) / 200 and x < 5 * screen_width /6 - (screen_width) / 200) and (y >  (2*screen_height/3) - (screen_height/30 *1.5)  and  y < (2*screen_height/3)  - screen_height/30):
        percentage = ((5 * screen_width /6) - ((screen_width) / 200)) - (screen_width /6 + (screen_width) / 200)
        playerPercentage = (x - ((screen_width /6) + (screen_width / 200)))/percentage
        pPosition = x
    if mode == 1 or mode == 2:    
        if (x > 0 + (screen_width / 100) and x < screen_width - (screen_width / 100)) and (y > (((2*screen_height/3) + screen_height/30) + screen_height / 50) - screen_height / 50 and y <  (((2*screen_height/3) + screen_height/30) + screen_height / 50)+ screen_height / 20) :
            percentage = (screen_width - (screen_width / 100)) - (0 + (screen_width / 100))
            playerPercentage = (x - (0 + (screen_width / 100)))/percentage
        elementInteract()
    

    
    
def main():
    startApplication()
    mouse.on_click(lambda:checkClick())
    mouse.on_right_click(lambda:m.tk_popup(x, y))
    window.bind("<Motion>", motion)
    window.drop_target_register(tkinterdnd2.DND_FILES)
    window.dnd_bind("<<Drop>>", drop)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()
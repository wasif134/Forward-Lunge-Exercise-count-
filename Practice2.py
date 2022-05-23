#Modules for GUI
from tkinter import *
from tkinter import filedialog
from turtle import left, right
from PIL import Image, ImageTk

# Modules for Mediapipe
import cv2
import numpy as np
import time
import pose as pm


# Video accessing
def camselect(cam=1, file1=NONE):
    global cap
    if cam:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(file1)
camselect()
detector = pm.PoseDetector()
count=0
dir=0
pTime=0
def test2():
    global count
    global dir
    global pTime
    success, img = cap.read()

    #Sizing the screen
    img = cv2.resize(img, (990, 640))  # width, height
    
    img=detector.findPose(img)
    lmList=detector.findPosition(img,False)
    
    if len(lmList)!=0:
        angle=detector.findAngle(img,23,25,27)
        angle2=detector.findAngle(img,24,26,28)
        per=np.interp(angle,(77,172),(100,0))
        bar=np.interp(angle,(77,172),(100,550))
        if per==100:
            if dir==1:
                    count+=0.5
                    dir=0
        if per==0:
            if dir==0:
                    count+=0.5
                    dir=1
        cv2.rectangle(img,(875,100),(900,550),(0,255,0),3)
        cv2.rectangle(img,(875,int(bar)),(900,550),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(per)}%',(875,75),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),4)
        cv2.rectangle(img,(0,450),(150,550),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(int(count)),(45,520),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)
    #Displaying FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return rgb


################################### Tkinter Code ##########################################
def openfile():
    file1 = filedialog.askopenfilename()
    cam = 0
    camselect(cam, file1)

# code for opening first video
def openV1():  
    file1 = 'PoseVideos/1.mp4'
    cam = 0
    camselect(cam, file1)
def openV2():  
    file1 = 'PoseVideos/2.mp4'
    cam = 0
    camselect(cam, file1)
def camvideo():
    cam = 1
    camselect(cam)
def close():
    window.destroy()
# Window Creation
window = Tk()
window.configure(bg='blue')
window.title("Forward Lunge")
width = window.winfo_screenwidth()+10
height = window.winfo_screenheight()+10
window.geometry("%dx%d" % (width, height))
window.minsize(width, height)
window.maxsize(width, height)
################ Design ################
mainlabel = Label(window, text="Forward Lunge Count", font=(
    "Arial", 20, "bold", "italic"), bg="white", fg='black',relief=RAISED,bd=10,padx=20)
mainlabel.place(x=330,y=0)
f1 = Frame(window, bg='blue',relief=SUNKEN,bd=10)
f1.pack(side=RIGHT, fill='y', anchor='nw')
explore = Button(f1, text="Browse File", bg='white', fg='black', font=(
    "Calibri", 14, "bold"), command=openfile,relief=GROOVE,bd=5).pack(padx=50)
livecam = Button(f1, text="Open Web Cam", bg='white', fg='black', font=(
    "Calibri", 14, "bold"), command=camvideo,relief=GROOVE,bd=5).pack()
v1 = Button(f1, text="Test Video 1", bg='white', fg='black', font=(
    "Calibri", 14, "bold"), command=openV1,relief=GROOVE,bd=5).pack()
v2 = Button(f1, text="Test Video 2", bg='white', fg='black', font=(
    "Calibri", 14, "bold"), command=openV2,relief=GROOVE,bd=5).pack()
Exit_Application = Button(f1, text="Exit", bg='white', fg='black', font=(
    "Calibri", 14, "bold"), command=close,relief=GROOVE,bd=5).pack(pady=200)
############### Video Player #######################
label1 = Label(window, width=960, height=640,relief=SUNKEN,bd=10)
label1.place(x=40, y=50)
def select_img():
    image = Image.fromarray(test2())
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    window.after(1, select_img)
select_img()
window.mainloop()
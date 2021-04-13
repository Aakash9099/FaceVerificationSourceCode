import tkinter as tk
import cv2
import sys
from PIL import Image, ImageTk
from tkinter import messagebox
import numpy as np
import dlib

detector = dlib.get_frontal_face_detector()
new_path ="/Users/roshanvenkat/PycharmProjects/Hallaxy/venv/cropped_images/" # add a path to folder where cropped faces are stored
def MyRec(rgb,x,y,w,h,v=20,color=(200,0,0),thikness =2):

    cv2.line(rgb, (x,y),(x+v,y), color, thikness)
    cv2.line(rgb, (x,y),(x,y+v), color, thikness)

    cv2.line(rgb, (x+w,y),(x+w-v,y), color, thikness)
    cv2.line(rgb, (x+w,y),(x+w,y+v), color, thikness)

    cv2.line(rgb, (x,y+h),(x,y+h-v), color, thikness)
    cv2.line(rgb, (x,y+h),(x+v,y+h), color, thikness)

    cv2.line(rgb, (x+w,y+h),(x+w,y+h-v), color, thikness)
    cv2.line(rgb, (x+w,y+h),(x+w-v,y+h), color, thikness)

def save (img,name, bbox, width=180,height=227):
    x, y, w, h = bbox
    imgCrop = img[y:h, x: w]
    imgCrop = cv2.resize(imgCrop, (width, height)) #we need this line to reshape the images
    cv2.imwrite(name+".jpg", imgCrop)

def faces():
    frame =cv2.imread('imageCap.png')
    gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for counter,face in enumerate(faces):
        #print(counter)
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        cv2.rectangle(frame,(x1,y1),(x2,y2),(220,255,220),1)
        MyRec(frame, x1, y1, x2 - x1, y2 - y1, 10, (0,250,0), 3)
        # save(gray,new_path+str(counter),(x1-fit,y1-fit,x2+fit,y2+fit))
        save(gray,new_path+str(counter),(x1,y1,x2,y2))

cancel = False

def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
    button1 = tk.Button(mainWindow, text="Verify!", command=saveAndExit)
    button1.place(anchor=tk.CENTER, relx=0.5, rely=0.9, width=150, height=50)
    button1.focus()

def saveAndExit(event = 0):
    global prevImg

    if (len(sys.argv) < 2):
        filepath = "imageCap.png"
    else:
        filepath = sys.argv[1]

    #print ("Output file to: " + filepath)
    prevImg.save(filepath)

    PATH = "/Users/roshanvenkat/PycharmProjects/Hallaxy/venv/cropped_images/"
    faces()
    original = cv2.imread("/Users/roshanvenkat/PycharmProjects/Hallaxy/venv/cropped_images/0.jpg")
    duplicate = cv2.imread("/Users/roshanvenkat/PycharmProjects/Hallaxy/venv/cropped_images/1.jpg")
    if original.shape == duplicate.shape:
        #print("The images have same size and channels")
        difference = cv2.subtract(original, duplicate)
        #print(np.sum(difference))
        w, h, c = difference.shape
        total_pixel_value_count = w * h * c * 255
        percentage_match = (total_pixel_value_count - np.sum(difference)) / total_pixel_value_count * 100
        #print(percentage_match)
        if percentage_match > 90:
            messagebox.showinfo("Verification","Verification Successful")
            #print("Image Matched")
        else:
            messagebox.showerror("Verification","Verification UnSuccessful")
            #print("Image Not Matched")
    mainWindow.quit()

cap = cv2.VideoCapture(0)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()
mainWindow = tk.Tk(screenName="Camera Capture")
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
button = tk.Button(mainWindow, text="Capture", command=prompt_ok)
lmain.pack()
button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
button.focus()

def show_frame():
    global cancel, prevImg, button

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()

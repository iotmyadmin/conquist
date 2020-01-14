from tkinter import * 
from tkinter.filedialog import askopenfilename
import cv2
from detect import *
import sqlite3

window = Tk()
window.title("automatic detector")
window.minsize(500, 300)
window.configure(bg="#2cc3d4")
frame = Frame(window)
frame.configure(bg="#2cc3d4")
frame2=Frame(frame)
frame2.configure(bg="#2cc3d4")
frame3=Frame(frame)
frame3.configure(bg="#2cc3d4")
filename=None
image = cv2.imread("mycar.jpg")

def choose():
	filename=askopenfilename()
	#print(filename)
	global image
	image = cv2.imread(filename)
	out.delete(0.0,END)
	#text2.insert(END,filename)

def capture():
    video = cv2.VideoCapture(0) 
    a = 0
    while True:
        a = a + 1
        check, frame = video.read()
        cv2.imshow("Capturing",frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    showPic = cv2.imwrite("textImage.jpg",frame)
    #print(showPic)
    global image
    image = cv2.imread("textImage.jpg")
    video.release()
    cv2.destroyAllWindows

def myfun():
        try:
            images = detectPlateRough(image,image.shape[0],top_bottom_padding_rate=0.1)
            text = pytesseract.image_to_string(images)
            #text.replace(')','')
            #print(text)
            out.delete(0.0,END)
            owner = "Vehical Number: "+text+"\nOwner name: "+show(text)
            out.insert(END,owner)
            print(owner)
        except:
            print("An exception occurred")
        #print("next")

def show(veh):
        con=sqlite3.connect("data.db")
        #con.execute("create table owner(sno int ,veh_no char(10), name char(10) )")
        #con.execute("insert into owner values(2,'INA 8001)','vedant')")
        #con.commit
        c=""
        veh_no=veh #"mp0932"
        q0="select name from owner where veh_no='"+veh_no+"'"
        s=con.execute(q0)
        for i in s:
        	#print(i[0])
        	c=i[0]
        return c
        
head = Label(frame, text="Welcome to Project G-5" ,bg="#2cc3d4")
head.config(font=("Courier",30))
text1= Label(frame,text="Choose file to get details",bg="#2cc3d4")
text1.config(font=("Courier",18))
text2= Label(frame,text="",bg="#2cc3d4")
text2.config(font=("Courier",33))
button0=Button(frame2,text="capture",command=capture,bg="#ffffff")
button1=Button(frame2,text="select",command=choose,bg="#ffffff")
button2 = Button (frame3,font=18, text="process", command=myfun,bg="#ffffff")
text3=Label(frame2,text="\nOwner Info",bg="#2cc3d4")#.grid(row=6,column=0,sticky=W)
text3.config(font=("Courier",18))
out=Text(frame2,width=30,height=2,wrap=WORD,background="white",bg="#2cd4c0")
#out.grid(row=10,column=0,columnspan=2,sticky=W)

#button2 = Button (frame, text="Close", command=window.destroy)

head.pack()
text1.pack()
frame.pack()
frame2.pack()
text3.pack()
out.pack()
text2.pack()

button0.pack(side=RIGHT)
button1.pack(side=LEFT)
frame3.pack(side=BOTTOM)
button2.pack()
window.mainloop()

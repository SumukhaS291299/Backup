from docx2pdf import convert
from tkinter import *
from PyInstaller.utils.hooks import copy_metadata
class ToPdf:
    def click(self):
        e1.get()
        e2.get()
        convert(e1.get())
        convert(e1.get(), e2.get())
        convert(e2.get())
        l3.config(text="Prepairing")
        exit(0)
S=ToPdf()
frame=Tk()
frame.geometry('500x200')
l1=Label(frame,text="Enter word(input) file location(abs path)")
l2=Label(frame,text="Enter pdf(output) file location(abs path)")
l3=Label(frame,text="")
e1 = Entry(frame,font=20,width=50)
e2 = Entry(frame,font=20,width=50)
ok = Button(frame, text="Done", bg="purple", fg="cyan",command=S.click)
l1.pack()
e1.pack()
l2.pack()
e2.pack()
ok.pack()
ok.pack()
l3.pack()
frame.mainloop()

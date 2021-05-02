from tkinter import *
#import tkinter as tk
import time

root = Tk()
root.title('FEEDER ACTUATOR CLOCK')
root.geometry("400x200")







def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")

    my_label.config(text=hour + ":" + minute)
    my_label.after(60000, clock)

def update():
    my_label.config(text="new text")

my_label = Label(root, text="", font=("Helvetica", 48), fg="green", bg="black")
#my_label = Label(root, text="old text")    
my_label.pack(pady=20)
#my_label.after(5000, update)
clock()
root.mainloop()

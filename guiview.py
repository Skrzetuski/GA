import tkinter as tk
import tkinter.ttk as ttk
import random

from PIL import ImageTk,Image

random.seed(111)

def random_color():
    hex = ['5','6','7','8','9','a','b','c','d','e','f']
    kod = '#'
    for i in range(0,6):
        kod += random.choice(hex)
    return kod

def random_coord():
    return random.randint(10,350)

def create_box(asdf,weight,value,final=False):
    global pos_x,pos_y
    if final:
        pos_y = pos_y+50
    else:
        pos_x = random_coord()
        pos_y = random_coord()
    box = asdf.create_rectangle(pos_x,pos_y,pos_x+50,pos_y+20,fill=random_color())
    asdf.create_text(pos_x+25,pos_y+10,fill="#111",text="{}kg {}zł".format(weight,value))
    asdf.pack()
    return box

def buttonClick(pole,b,mapa,input_bin):
    pole.delete("all")
    random.seed(55)

    global pos_x,pos_y
    pos_x,pos_y = 280,100
    for x in mapa:
        create_box(pole,x[0],x[1],final=True)

    # img = ImageTk.PhotoImage(Image.open("knapsack.png"))
    # panel = tk.Label(pole, image=img)
    # panel.pack(side="bottom", fill="both", expand="yes")


    b.configure(text='Pokaz historie generacji',command=input_bin.showGraph)




def showGui(items,mapa,input_bin):
    global root
    root = tk.Tk()
    root.geometry("500x500")
    root.configure(background="#333")

    pole = tk.Canvas(root,width=400,height=400,bg='#111')

    for x in items:
        create_box(pole,items[x][0],items[x][1])

    pole.pack(pady=15)


    button = tk.Button(root,command=lambda: buttonClick(pole,button,mapa,input_bin),text="Start",width=50)
    button.pack()

    root.mainloop()
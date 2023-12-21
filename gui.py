import tkinter as tk
import calculate as calc
import numpy
from PIL import Image,ImageTk

#初期画面作成
pic=Image.open('image.jpg')
w=pic.width
h=pic.height

root=tk.Tk()
root.geometry("1920x1080")
root.title("潮流計算")

pic=pic.resize((int(w * (1080/w)), int(h * (1080/w))))
pic = ImageTk.PhotoImage(pic)

canvas=tk.Canvas(bg="gray", width=1920, height=1080)
canvas.place(x=0, y=0)
canvas.create_image(200, 50, image=pic, anchor=tk.NW)

#潮流計算の関数作成

#GUI上にP1を表示
P2_label=tk.Label(master=root,text="P2",font=20)
P2_label.place(x=10,y=20)

Q2_label=tk.Label(master=root,text="Q2",font=20)
Q2_label.place(x=10,y=50)

P3_label=tk.Label(master=root,text="P3",font=20)
P3_label.place(x=10,y=80)

Q3_label=tk.Label(master=root,text="Q3",font=20)
Q3_label.place(x=10,y=110)

P4_label=tk.Label(master=root,text="P4",font=20)
P4_label.place(x=10,y=140)

#テキストエリア作製
num_area_1=tk.Entry(master=root,width=5,font=20)
num_area_1.place(x=100,y=20)

num_area_2=tk.Entry(master=root,width=5,font=20)
num_area_2.place(x=100,y=50)

num_area_3=tk.Entry(master=root,width=5,font=20)
num_area_3.place(x=100,y=80)

num_area_4=tk.Entry(master=root,width=5,font=20)
num_area_4.place(x=100,y=110)

num_area_5=tk.Entry(master=root,width=5,font=20)
num_area_5.place(x=100,y=140)

def draw_shape(canvas,above,under,V4):
    canvas.delete("arrow","circle")
    # 矢印の描画（上）
    if (above <= 0).any():
        canvas.create_line(500, 80, 550, 80, width=above*(-33), arrow="first", arrowshape=(above*(-20),above*(-25),above*(-10)),tag="arrow")
        #数値は全て変数にする(始点x,始点ｙ,終点x,終点y,太さ)
    else:
        canvas.create_line(600, 80, 650, 80, width=above*33, arrow="last", arrowshape=(above*20,above*25,above*10),tag="arrow")

    # 矢印の描画（下）
    if under <= 0:
        canvas.create_line(500, 500, 550, 500, width=under*(-33), arrow="first", arrowshape=(under*(-20),under*(-25),under*(-10)),tag="arrow")
        #数値は全て変数にする
    else:
        canvas.create_line(600, 500, 650, 500, width=under*33, arrow="last", arrowshape=(under*20,under*25,under*10),tag="arrow")

    #円の表示
    t1=240.0
    t2=400.0

    x0=t1-10*V4
    y0=t2-10*V4
    x1=t1+10*V4+100
    y1=t2+10*V4+100

    canvas.create_oval(x0,y0,x1,y1,fill="red",tag="circle")
    #canvas.create_text(100,100,text="test")

def Caluclation():
    val_1 = float(num_area_1.get())
    val_2 = float(num_area_2.get())
    val_3 = float(num_area_3.get())
    val_4 = float(num_area_4.get())
    val_5 = float(num_area_5.get())
    V4=var.get()
    
    P2 = val_1
    Q2 = val_2
    P3 = val_3
    Q3 = val_4
    P4 = val_5

    P_branch=calc.node_calc(P2,P3,P4,Q2,Q3)
    above=P_branch[0][1] 
    under=P_branch[2][3] #後で修正
    draw_shape(canvas,above,under,V4)
    
    #実部を潮流電流とした
    

#ボタン作成
enter_btn=tk.Button(master=root,text="入力",command=Caluclation)
enter_btn.place(x=100,y=300)


#スライド作成

var=tk.DoubleVar()

(tk.Scale(
    master=root,
    from_=0.1,
    to=10,
    resolution=0.1,
    label='V4',
    font=("",15),
    tickinterval=5,
    length=200,
    width=20,
    orient=tk.HORIZONTAL,
    variable=var
    ).
    grid(
    row=1,
    column=3,
    padx=10,
    pady=170))

t1=240.0
t2=100.0

x0=t1-10
y0=t2-10
x1=t1+110
y1=t2+110

canvas.create_oval(x0,y0,x1,y1,fill="red")





root.mainloop()
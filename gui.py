import tkinter as tk
import calculate as calc
import numpy
from PIL import Image,ImageTk

#初期画面作成
pic=Image.open('image2.jpg')
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

def draw_shape(canvas,above,under,V4,V2,V3):
    canvas.delete("arrow","circle","line")
    # 矢印の描画（上）
    if (above <= 0).any():
        canvas.create_line(600, 80, 650, 80, width=above*(-33), fill="#edb918", arrow="first", arrowshape=(above*(-20),above*(-25),above*(-10)),tag="arrow")
        #数値は全て変数にする(始点x,始点ｙ,終点x,終点y,太さ)
    else:
        canvas.create_line(600, 80, 650, 80, width=above*33, fill="#edb918", arrow="last", arrowshape=(above*20,above*25,above*10),tag="arrow")

    # 矢印の描画（下）
    if under <= 0:
        canvas.create_line(600, 500, 650, 500, width=under*(-33), fill="#edb918", arrow="first", arrowshape=(under*(-20),under*(-25),under*(-10)),tag="arrow")
        #数値は全て変数にする
    else:
        canvas.create_line(600, 500, 650, 500, width=under*33, fill="#edb918", arrow="last", arrowshape=(under*20,under*25,under*10),tag="arrow")

    #円の表示
    t1=240.0
    t2=400.0

    x0=t1-10*V4
    y0=t2-10*V4
    x1=t1+10*V4+100
    y1=t2+10*V4+100

    canvas.create_oval(x0,y0,x1,y1,fill="red",tag="circle")
    #canvas.create_text(100,100,text="test")

    #電圧の表示
    canvas.create_line(900,100,900+V2*40,100,width=20,fill="#33ccff",tag="line")
    canvas.create_line(900,350,900+V3*40,350,width=20,fill="#33ccff",tag="line")
    #+100にV2*1000 V3*1000を代入

def Caluclation():
   # val_1 = float(num_area_1.get())
   # val_2 = float(num_area_2.get())
    #val_3 = float(num_area_3.get())
    #val_4 = float(num_area_4.get())
    #val_5 = float(num_area_5.get())
    V4=scale_1.get()
    
    P2 = scale_2.get()
    Q2 = scale_3.get()
    P3 = scale_4.get()
    Q3 = scale_5.get()
    P4 = scale_6.get()
    
    ans=calc.node_calc(P2,P3,P4,Q2,Q3,V4)
    P_branch=ans[0]
    above=P_branch[0][1] 
    under=P_branch[2][3]
    V=ans[1] 
    V2=V[1]
    V3=V[2]
    draw_shape(canvas,above,under,V4,V2,V3)
    
    #実部を潮流電流とした
    

#ボタン作成
enter_btn=tk.Button(master=root,text="入力",command=Caluclation) 
enter_btn.place(x=260,y=600)


#スライド作成
    
var_1=tk.DoubleVar()
var_2=tk.DoubleVar()
var_3=tk.DoubleVar()
var_4=tk.DoubleVar()
var_5=tk.DoubleVar()
var_6=tk.DoubleVar()


scale_1=tk.Scale(
    command=Caluclation,
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
    variable=var_1,
         
)
scale_1.pack(padx=10,pady=10)
scale_1.set(1)

scale_2=tk.Scale(
    command=Caluclation,
    master=root,
    from_=-1,
    to=1,
    resolution=0.1,
    label='P2',
    font=("",15),
    tickinterval=5,
    length=200,
    width=20,
    orient=tk.HORIZONTAL,
    variable=var_2,
)
scale_2.pack(padx=10,pady=10)
scale_2.set(-0.6)

scale_3=tk.Scale(
    command=Caluclation,
    master=root,
    from_=-1,
    to=1,
    resolution=0.1,
    label='Q2',
    font=("",15),
    tickinterval=5,
    length=200,
    width=20,
    orient=tk.HORIZONTAL,
    variable=var_3,
)
scale_3.pack(padx=10,pady=10)
scale_3.set(-0.3)

scale_4=tk.Scale(
    command=Caluclation,
    master=root,
    from_=-1,
    to=1,
    resolution=0.1,
    label='P3',
    font=("",15),
    tickinterval=5,
    length=200,
    width=20,
    orient=tk.HORIZONTAL,
    variable=var_4,
    
)
scale_4.pack(padx=10,pady=10)
scale_4.set(-0.6)

scale_5=tk.Scale(
    command=Caluclation,
    master=root,
    from_=-1,
    to=1,
    resolution=0.1,
    label='Q3',
    font=("",15),
    tickinterval=5,
    length=200,
    width=20,
    orient=tk.HORIZONTAL,
    variable=var_5,
    )
scale_5.pack(padx=10,pady=10)
scale_5.set(-0.3)

scale_6=tk.Scale(
    command=Caluclation,
    master=root,
    from_=-1,
    to=1,
    resolution=0.1,
    label='P4',
    font=("",15),
    tickinterval=5,
    length=200,
    width=20,
    orient=tk.HORIZONTAL,
    variable=var_6,   
    )
scale_6.pack(padx=10,pady=10)
scale_6.set(0.6)

scale_1.place(x=20,y=50)
scale_2.place(x=20,y=150)
scale_3.place(x=20,y=250)
scale_4.place(x=20,y=350)
scale_5.place(x=20,y=450)
scale_6.place(x=20,y=550)

t1=240.0
t2=100.0

x0=t1-10
y0=t2-10
x1=t1+110
y1=t2+110

canvas.create_oval(x0,y0,x1,y1,fill="red")

root.mainloop()
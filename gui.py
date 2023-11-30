import tkinter as tk
import calculate as calc
from PIL import Image,ImageTk


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

#以下山本のコード___________________________________________________________________________
I_dash=5 #後で修正
#とりあえず＞0で設定

# 矢印の描画（上）
if I_dash <= 0:
    canvas.create_line(500, 80, 550, 80, width=20, arrow="first", arrowshape=(12, 15, 6))
    #数値は全て変数にする(始点x,始点ｙ,終点x,終点y,太さ)
else:
    canvas.create_line(600, 80, 650, 80, width=20, arrow="last", arrowshape=(12, 15, 6))

# 矢印の描画（下）
if I_dash <= 0:
    canvas.create_line(500, 500, 550, 500, width=20, arrow="first", arrowshape=(12, 15, 6))
    #数値は全て変数にする
else:
    canvas.create_line(600, 500, 650, 500, width=20, arrow="last", arrowshape=(12, 15, 6))

#canvas.create_text(100,100,text="test")

#以下やぶ_______________________________________________________________________________________

def Calculation():
    val_1 = float(num_area_1.get())
    val_2 = float(num_area_2.get())
    val_3 = float(num_area_3.get())
    val_4 = float(num_area_4.get())
    val_5 = float(num_area_5.get())

    P2 = val_1
    Q2 = val_2
    P3 = val_3
    Q3 = val_4
    P4 = val_5
    
    calc.node_calc(P2,P3,P4,Q2,Q3)


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

#ボタン作成
enter_btn=tk.Button(master=root,text="入力",command=Calculation)
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

V4=var





root.mainloop()
import numpy as np
import gui
#import sympy
np.set_printoptions(precision=4,floatmode='fixed')  

r = np.zeros((4,4))
r[0][1]=0.01
r[1][2]=0.005
r[2][3]=0.01
r[1][0]=0.01
r[2][1]=0.005
r[3][2]=0.01

x = np.zeros((4,4))
x[0][1]=0.5
x[1][2]=0.25
x[2][3]=0.5
x[1][0]=0.5
x[2][1]=0.25
x[3][2]=0.5

b = np.zeros((4,4))
b[0][1]=0.4
b[1][2]=0.2
b[2][3]=0.4
b[1][0]=0.4
b[2][1]=0.2
b[3][2]=0.4

bc = np.array([0,0.1,0.1,0])

theta=np.zeros((4,1))

V=np.zeros((4,1))
V[0][0]=1
V[3][0]=gui.V4  #1 #ここを操作する 元は1




cnt=0



Y = np.zeros((4,4),dtype=np.complex128)



for jj in range(4):
    for ii in range(4): 
        summ=0
        temp=0
        if ii==jj:
            for jj2 in range(4):
                if ii!=jj2:
                    
                    cnt=complex(r[ii][jj2],x[ii][jj2]+(b[ii][jj2])/2)
                    if cnt == 0:
                        temp=0
                    else:
                        temp=1/complex(r[ii][jj2],x[ii][jj2])+1j*(b[ii][jj2])/2
                    summ = summ+temp
                    
            Y[ii][jj]=summ+bc[ii]*1j
            
        if ii!=jj:
            cnt=complex(r[ii][jj],x[ii][jj])
            if cnt == 0:
                Y[ii][jj]=0
            else:
                Y[ii][jj]=-1/cnt
      

G=np.real(Y)
B=np.imag(Y)

#print(Y)
#print(G)
#print(B)


V=np.array([1,1,1,1])
theta=np.array([0,0,0,0])
Jacobian=np.zeros((5,5))
v=np.array([0,1,0,1,0])
func_v=np.array([[0,0,0,0,0]]) #np.zeros((5,1)) 転置するため[]が二重

P2=gui.P2 #-0.6
P3=gui.P3 #-0.6
P4=gui.P4 #0.6 #操作する 元は0.6
Q2=gui.Q2 #-0.3
Q3=gui.Q3 #-0.3

p=np.array([[P2,Q2,P3,Q3,P4]]) #転置するため[]が二重

f_inf=float('inf')



dfPi_dthetaj=np.zeros((4,4))#??
dfQi_dthetaj=np.zeros((4,4))#??
dfPi_dVj=np.zeros((4,4))#??
dfQi_dVj=np.zeros((4,4))#??

while np.linalg.norm(p-func_v,np.inf)>0.001:
    fP=np.zeros(4)#??
    fQ=np.zeros(4)#??
    for ii in range(4):
        summ=0

        for jj in range(4):
            summ=summ+V[jj]*(G[ii][jj]*np.cos(theta[ii]-theta[jj])+B[ii][jj]*np.sin(theta[ii]-theta[jj]))

        fP[ii]=V[ii]*summ

    for ii in range(4):
        summ=0

        for jj in range(4):
            summ=summ+V[jj]*(G[ii][jj]*np.sin(theta[ii]-theta[jj])-B[ii][jj]*np.cos(theta[ii]-theta[jj]))

        fQ[ii]=V[ii]*summ

    for jj in range(4):
        for ii in range(4):
            if ii==jj:
               
                dfPi_dthetaj[ii][jj]=-V[ii]*V[ii]*B[ii][jj]-fQ[ii]
                dfQi_dthetaj[ii][jj]=-V[ii]*V[ii]*G[ii][jj]+fP[ii]
                dfPi_dVj[ii][jj]=V[ii]*G[ii][jj]+fP[ii]/V[ii]
                dfQi_dVj[ii][jj]=-V[ii]*B[ii][jj]+fQ[ii]/V[ii]

            #この辺怪しいかも
            
            if ii!=jj:
                dfPi_dthetaj[ii][jj]=V[ii]*V[jj]*(G[ii][jj]*np.sin(theta[ii]-theta[jj])-B[ii][jj]*np.cos(theta[ii]-theta[jj]))

                dfQi_dthetaj[ii][jj]=-V[ii] * V[jj] * (G[ii][jj] * np.cos(theta[ii] - theta[jj]) + B[ii][jj] * np.sin(theta[ii] - theta[jj]))

                dfPi_dVj[ii][jj] = V[ii]*(G[ii][jj] * np.cos(theta[ii] - theta[jj]) - B[ii][jj] * np.sin(theta[ii] - theta[jj]))

                dfQi_dVj[ii][jj] = V[ii] * (-G[ii][jj] * np.sin(theta[ii] - theta[jj]) - B[ii][jj] * np.cos(theta[ii] - theta[jj]))

    #print(dfPi_dthetaj)
    #print(dfQi_dthetaj)
    #print(dfPi_dVj)
    #print(dfQi_dVj)

    Jacobian =np.array([[dfPi_dthetaj[1][1],dfPi_dVj[1][1],dfPi_dthetaj[1][2],dfPi_dVj[1][2],0],
                        [dfQi_dthetaj[1][1],dfQi_dVj[1][1],dfQi_dthetaj[1][2],dfQi_dVj[1][2],0],
                        [dfPi_dthetaj[2][1],dfPi_dVj[2][1],dfPi_dthetaj[2][2],dfPi_dVj[2][2],dfPi_dthetaj[2][3]],
                        [dfQi_dthetaj[2][1],dfQi_dVj[2][1],dfQi_dthetaj[2][2],dfQi_dVj[2][2],dfQi_dthetaj[2][3]],
                        [0,0,dfPi_dthetaj[3][2],dfPi_dVj[3][2],dfPi_dthetaj[3][3]]]) #それぞれ-1した

    func_v=[fP[1],fQ[1],fP[2],fQ[2],fP[3]] #それぞれ-1した

    #temp=v+np.dot(np.linalg.inv(Jacobian)*((p-func_v)).T)
    #以上の計算をするためにvを転置 np.arrayの[]が二重になった
    a=((p-func_v).T)
    c=(np.linalg.pinv(Jacobian))
    temp=np.dot(c,a)
    v=v+np.transpose(temp)
    V=np.array([V[0],v[0][1],v[0][3],V[3]]) #個々の数字をいじった(それぞれ-1,vは[0]を追加)
    theta=[theta[0],v[0][0],v[0][2],v[0][4]] #個々の数字をいじった(それぞれ-1,vは[0]を追加)
    #print(p-func_v)
    #print(np.linalg.norm(p-func_v))
    cnt=cnt+1
    #print(Jacobian)
    
#print(Y)
#print(cnt)
#print(Jacobian)
#print(v)
#print(func_v)
#print(V)
#print(theta)
                
#以下より未確定のコード
#---------------------------------------------------------------------------------------------------

#p37以下のコード

#print(b)
#print(r)
#print(x)
#print(bc)


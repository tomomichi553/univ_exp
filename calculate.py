
def node_calc(P2,P3,P4,Q2,Q3,V4):
    import numpy as np

    np.set_printoptions(precision=4,floatmode='fixed')  
    #ノードのインピーダンスとアドミタンスを代入
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

    V=np.array([1,1,1,1])
    V[3]=V4 #1 

    #ノードアドミタンス行列の計算
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
    
    theta=np.array([0,0,0,0])
    Jacobian=np.zeros((5,5))
    v=np.array([0,1,0,1,0])
    func_v=np.array([[0,0,0,0,0]]) 

    p=np.array([[P2,Q2,P3,Q3,P4]]) 
    f_inf=float('inf')

    dfPi_dthetaj=np.zeros((4,4))
    dfQi_dthetaj=np.zeros((4,4))
    dfPi_dVj=np.zeros((4,4))
    dfQi_dVj=np.zeros((4,4))

    count = 0 #反復回数
    while np.linalg.norm(p-func_v,np.inf)>0.001:
        count+=1
        if count>10000:
            return 0
        fP=np.zeros(4)
        fQ=np.zeros(4)
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

                if ii!=jj:
                    dfPi_dthetaj[ii][jj]=V[ii]*V[jj]*(G[ii][jj]*np.sin(theta[ii]-theta[jj])-B[ii][jj]*np.cos(theta[ii]-theta[jj]))

                    dfQi_dthetaj[ii][jj]=-V[ii] * V[jj] * (G[ii][jj] * np.cos(theta[ii] - theta[jj]) + B[ii][jj] * np.sin(theta[ii] - theta[jj]))

                    dfPi_dVj[ii][jj] = V[ii]*(G[ii][jj] * np.cos(theta[ii] - theta[jj]) - B[ii][jj] * np.sin(theta[ii] - theta[jj]))

                    dfQi_dVj[ii][jj] = V[ii] * (-G[ii][jj] * np.sin(theta[ii] - theta[jj]) - B[ii][jj] * np.cos(theta[ii] - theta[jj]))


        Jacobian =np.array([[dfPi_dthetaj[1][1],dfPi_dVj[1][1],dfPi_dthetaj[1][2],dfPi_dVj[1][2],0],
                            [dfQi_dthetaj[1][1],dfQi_dVj[1][1],dfQi_dthetaj[1][2],dfQi_dVj[1][2],0],
                            [dfPi_dthetaj[2][1],dfPi_dVj[2][1],dfPi_dthetaj[2][2],dfPi_dVj[2][2],dfPi_dthetaj[2][3]],
                            [dfQi_dthetaj[2][1],dfQi_dVj[2][1],dfQi_dthetaj[2][2],dfQi_dVj[2][2],dfQi_dthetaj[2][3]],
                            [0,0,dfPi_dthetaj[3][2],dfPi_dVj[3][2],dfPi_dthetaj[3][3]]]) 

        func_v=[fP[1],fQ[1],fP[2],fQ[2],fP[3]] 

        a=((p-func_v).T)
        c=(np.linalg.pinv(Jacobian))
        temp=np.dot(c,a)
        v=v+np.transpose(temp)
        V=np.array([V[0],v[0][1],v[0][3],V[3]]) 
        theta=[theta[0],v[0][0],v[0][2],v[0][4]] 
        cnt=cnt+1
        
    p=np.array([[P2,Q2,P3,Q3,P4]]) 

    I_dash=np.zeros((4,4),dtype=np.complex128)
    Power=np.zeros((4,4),dtype=np.complex128)
    V_dot=np.zeros((4),dtype=np.complex128)

    for ii in range(4):
        V_dot[ii]=V[ii]*np.exp(1j*theta[ii]) 

    for ii in range(4):
        for jj in range(4):
            I_dash[ii][jj]=((-1j*(b[ii][jj])/2)*V_dot[ii])+((V_dot[ii]-V_dot[jj])/(r[ii][jj]+1j*(x[ii][jj])))  
            
    for ii in range(4):
        for jj in range(4):
            Power[ii][jj]=V_dot[ii]*np.conj(I_dash[ii][jj])

    I_real=np.real(I_dash)
    
    P_branch=np.real(Power)
    Q_branch=np.imag(Power)
    
    return P_branch,V
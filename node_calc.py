def node_calc(P2,P3,P4,Q2,Q3,V):
    import numpy as np
    import calculate as calc

    r = np.full((4,4),np.inf)
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

    #P2=-0.6
    #P3=-0.6
    #P4=0.6
    #Q2=-0.3
    #Q3=-0.3

    p=np.array([[P2,Q2,P3,Q3,P4]]) #転置するため[]が二重


    I_dash=np.zeros((4,4),dtype=np.complex128)
    Power=np.zeros((4,4),dtype=np.complex128)
    V_dot=np.zeros((4),dtype=np.complex128)

    for ii in range(4):
        V_dot[ii]=calc.V[ii]*np.exp(1j*calc.theta[ii]) #Vとthetaの前からcalc抜いた

    for ii in range(4):
        for jj in range(4):
            I_dash[ii][jj]=((-1j*(b[ii][jj])/2)*V_dot[ii])+((V_dot[ii]-V_dot[jj])/(r[ii][jj]+1j*(x[ii][jj])))  
            
    for ii in range(4):
        for jj in range(4):
            Power[ii][jj]=V_dot[ii]*np.conj(I_dash[ii][jj])
            
    print("ブランチ電流の計算")
    print(I_dash)

    print("ブランチの電力潮流計算")
    print(Power)

    P_branch=np.real(Power)
    Q_branch=np.imag(Power)
    
node_calc(-0.6,-0.6,0.6,-0.3,-0.3,1)
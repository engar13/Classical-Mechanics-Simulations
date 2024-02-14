# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 18:16:32 2023

@author: Enric Garriga
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


steps_per_sec=100000 #Quants steps fem en un segon de "temps real"
tf=20 #Quants segons dura l'animació
N=steps_per_sec*tf #Nombre total de steps que calcularem
dt=tf/N #Temps entre steps
t=np.linspace(0, tf, num=N) #t is NOT an array of arrays: t!=[ [list of t's], length of dt ]
#ATENCIO: PARAMETRES DE L'ANIMACIÓ (framerate etc.) AVALL


theta=np.zeros(N)
dTheta=np.zeros(N) #velocitat al llarg del temps
d2Theta=np.zeros(N) #acceleracio angular al llarg del temps

#Initial conditions:
Th0=np.pi
dTh0=0

theta[0]=Th0
dTheta[0]=dTh0

#Paràmetres: (w=velocitat rotació anella, a=radi anella, b=llargada pèndol)
w=2
a=1
b=4
g=9.8

#Calculem la llista de les posicions als instants t

for i in range(0, N - 1):
    #Comencem calculant l'acceleració al moment actual t:
    d2Theta[i] = ( w**2*a*np.cos(theta[i] - w * t[i]) - g*np.sin(theta[i]) ) /b #Calculem acceleració actual amb la EOM treta usant el Lagrangià
    
    dTheta[i+1] = dTheta[i] + d2Theta[i]*dt #Calculem la velocitat al seguent instant amb l'acceleració calculada abans
    theta[i+1] = theta[i] + dTheta[i]*dt #+ d2Theta[i]*(t[i+1]-t[i])**2/2#+d2Theta[i]*t[i]*dt  #Calculem la posició al seguent instant


#Posició del pèndol (si coneixem theta ja només és passar a cartesianes):
rx=a*np.cos(w*t) + b*np.sin(theta)
ry=a*np.sin(w*t) - b*np.cos(theta)

#Posició de la lligadura:
crx = a*np.cos(w*t)
cry = a*np.sin(w*t)

#------------------------------------ANIMACIO:
    
frameRate = 15 #(en ms/frame, ha de ser un int ossigui que el minim és 1ms/frame)

frames_per_sec = int(1000/frameRate)

ratio=int(steps_per_sec/frames_per_sec)



fig, ax = plt.subplots()

#ax2.plot(t,dt/dth2)
ax.set_xlim(-6, 6)  # Adjust the x-axis limits as needed
ax.set_ylim(-6, 6)   # Adjust the y-axis limits as needed

ax.set_aspect(1)
Drawing_uncolored_circle = plt.Circle( (0,0) , 1 , fill = False )
ax.add_artist( Drawing_uncolored_circle )

line, = ax.plot([], [], 'r-', lw=2, color='grey')
point1, = ax.plot([], [], 'ro', markersize=8)
point2, = ax.plot([], [], 'bo', markersize=8)

def update_points(num, line, point1, point2):
   # time = t[num]  # Adjust the time step as needed
    x = rx[ratio*num]
    y = ry[ratio*num]
    cx = crx[ratio*num]
    cy = cry[ratio*num]

    line.set_data([x,cx], [y, cy])
    point1.set_data(x,y)
    point2.set_data(cx, cy)

    return line, point1, point2

ani = animation.FuncAnimation(fig, update_points, frames=int(tf*frames_per_sec), fargs=(line, point1, point2), interval=frameRate)

plt.show()

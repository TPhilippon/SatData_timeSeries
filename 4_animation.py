# -*- coding: cp1252 -*-
import matplotlib
matplotlib.use('TkAgg') # do this before importing pylab
import matplotlib.pyplot as plt
import Image
import glob

varg=['sst11mic_8d','poc_8d', 'nsst_8d','chl_8d']
varg=varg[1]  # Choisir la variable géochimique
path = varg+'/png'

fig = plt.figure()
ax = fig.add_subplot(111)

def animate():
    filenames=sorted(glob.glob(path+'/*.png'))
    im=plt.imshow(Image.open(filenames[0]))
    for filename in filenames[1:]:
        image=Image.open(filename)
        image=image.transpose(Image.FLIP_TOP_BOTTOM)
        im.set_data(image)
        
        fig.canvas.draw() 

win = fig.canvas.manager.window
fig.canvas.manager.window.after(100, animate)
plt.show()

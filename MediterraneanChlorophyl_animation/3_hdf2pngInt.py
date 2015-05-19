#!/usr/bin/env python
# -*- coding: utf8 -*-



import os
import sys
from pyhdf.SD import SD, SDC
from mpl_toolkits.basemap import Basemap, cm
from matplotlib.colors import LogNorm
import matplotlib
import pylab
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.signal
import scipy.ndimage
import scipy.interpolate
import pdb

#---------- read data ----------#

varg=['sst11mic_8d','poc_8d', 'nsst_8d','chl_8d']
varg=varg[3]  # Choisir la variable géochimique
      
path = varg+'/hdf/'
files = os.listdir(path)
files.sort()
print len(files)

colors = [(0.33,0.33,0.33)] + [(plt.cm.jet(i)) for i in xrange(1,256)]
new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256) # Colormap


ymin=1002
ymax=1449
xmin=4086
xmax=5212

latmax=90-ymin*0.04166666
latmin=90-ymax*0.04166666
longmin=xmin*0.04166667-179.9792
longmax=xmax*0.04166667-179.9792
#------------------------------------------------------


#-------------------------------------------------------

for myfile in files:

    annee = myfile[1:5]
    j = myfile[12:15]
    j=int(j)
 
    if j >= 355 or j < 83:
        saison = u'Hiver'
    if j >= 83 and j < 176:
        saison = u'Printemps'
    if j >= 176 and j < 261:
        saison = u'Eté'
    if j >= 261 and j < 355:
        saison = u'Automne'

    File_Name = myfile
    File = SD(varg+'/hdf/'+File_Name, SDC.READ)
    l3 = File.select('l3m_data')
    l3d = l3.get()

    print annee,j,l3d.min(),l3d.max()
    FillValue = -32767.0
    l3d=l3d[1002:1449,4086:5212] # Echantilloner la mediterranee
    
    l3d[ (l3d < 0.01) & (l3d != -32767.0) ] = 0.011 #
    l3d[ l3d > 10 ] = 10.0 # 
    print annee,j #,l3d.min(),l3d.max()
    l3d[ l3d == -32767.0 ] = np.nan # 0.011 #0.00001 #
    #print annee,j,l3d.min(),l3d.max()

    #print np.isnan(np.nan)

    #------------ Interolate


    print 'interpolating....'
    data = l3d

    # a boolean array of (width, height) which False where there are missing values and True where there are valid (non-missing) values
    mask = np.isnan(l3d)
    mask=~mask
    # array of (number of points, 2) containing the x,y coordinates of the valid values only
    xx, yy = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
    xym = np.vstack( (np.ravel(xx[mask]), np.ravel(yy[mask])) ).T
    # the valid values in the first, second, third color channel,  as 1D arrays (in the same order as their coordinates in xym)
    data = np.ravel( data[mask] )
    # three separate interpolators for the separate color channels
    interp0 = scipy.interpolate.NearestNDInterpolator( xym, data )
    # interpolate the whole image, one color channel at a time    
    result0 = interp0(np.ravel(xx), np.ravel(yy)).reshape( xx.shape )
    l3d=result0

    print 'end interp'
    #---------- Plot Data Global Map ----------#

    m = Basemap(projection='cyl',llcrnrlat=latmin,urcrnrlat=latmax, llcrnrlon=longmin, \
               urcrnrlon=longmax,resolution='c')
    print 'end basemap'           
    m.imshow(np.flipud(l3d), norm=LogNorm(vmin=10, vmax=1000.0), cmap=new_map, interpolation='bilinear')
    m.drawlsmask(land_color='beige',ocean_color='None',lakes=True)
    #cb = plt.colorbar(img,"bottom", size="5%", pad='4%')

    plt.title(varg+'  '+saison+'   '+annee+'   jour : '+str(j))
    plt.savefig(varg+'/png/'+File_Name+'.png',dpi=200,bbox_inches='tight')
    
    #plt.show()
    #pause('Pausing for click')
    plt.close() 

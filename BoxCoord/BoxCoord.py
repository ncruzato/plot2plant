# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 14:08:20 2020

@author: Nathalia Cruzato
"""
import osgeo.ogr as ogr
from math import sin, cos, pi

def BoxCoord(x1,y1,boxlen,boxwid,theta):
    coordinates=[]
    radtheta = theta*pi/180
    radbeta = (pi/2)-radtheta
    
    x2 = x1+(cos(radtheta)*boxlen)
    y2 = y1+(sin(radtheta)*boxlen)

    x3 = x2-(sin(radtheta)*boxwid)
    y3 = y2+(cos(radtheta)*boxwid)

    x4 = x1-(cos(radbeta)*boxwid)
    y4 = y1+(sin(radbeta)*boxwid)

    coordinates.append(x1)
    coordinates.append(y1)
    coordinates.append(x2)
    coordinates.append(y2)
    coordinates.append(x3)
    coordinates.append(y3)
    coordinates.append(x4)
    coordinates.append(y4)
   
    return coordinates
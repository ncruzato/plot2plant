# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:12:44 2020

@author: Nathalia Cruzato
"""
import os, sys, csv, pandas
import osgeo.ogr as ogr
import osgeo.osr as osr
from math import sin, cos, pi

#set directory
os.chdir('C:/Users/OWNER/OneDrive/Project 2')

##INPUT VARIABLES##

# CSV file containing polygon barcodes (IDs)
barcodes = 'DG2F_labels.csv'

# name of the shapefile that will be created
fin='CS18-YC2-grid.shp'

#Origin coordinates (bottom letf)
## For DG2F x0 = 746301.801, y0 = 3382007.260 / For YC x0 = 746318.7099, y0 = 3381990.6059
x0 = 746318.7099
y0 = 3381990.6059

#Row width
## 2.5 ft or 0.762 m
rowwidth = 0.762

#Row lenght
## For DG2F 21 ft or 6.4008 meters (25 ft with allies), rowlen = 5
## YC 8.5 ft (12.5 ft with allies), rowlen = 2.5
rowlen = 2.5

#Space between rows
## zero
rowspace = 0

#Space between ranges
## 4ft or 1.2192 m, for DG2F rangespace = 2.62, for UC rangespace=1.31
rangespace = 1.31

#Number of plants per plot (use maximum stand count)
## G2F 47seed/plot  MEAN 35.3, MEDIAN 36, MODE 36.5, MAX 41, max stdcount = 32 in 5m 
## YC 24 seed/plot  MEAN 12.5, MEDIAN 13, MODE 14, MAX 21, max stdcount = 21 #in 2.5 m
stdcount = 21 #in 2.5 m

#Rotation
## 47 degrees
theta = 47
#Number of ranges
## DG2F has 16 ranges
## YC has 32 ranges
ranges = 32
#Number of rows
## DG2F has 64 rows
## YC has 38 rows
rows = 17

#set up the shapefile driver
driver=ogr.GetDriverByName('ESRI Shapefile')

#create data source
driver.DeleteDataSource(fin)
ds=driver.CreateDataSource(fin)

# create the spatial referece, WGS84, UTM Zone 14N, EPSG 32614
srs = osr.SpatialReference()
srs.ImportFromEPSG(32614)

#create the layer
layer = ds.CreateLayer('polygon', srs, geom_type=ogr.wkbPolygon)

#add fields
field_id=ogr.FieldDefn('id',ogr.OFTString)
field_id.SetWidth(24)
layer.CreateField(field_id)

#set theta in radians
radtheta = theta*pi/180
#set beta in radians, beta = 90-theta
radbeta = (pi/2)-radtheta

#read ID csv file
dfbarcodes = pandas.read_csv(barcodes, header=None)
txtbarcodes=dfbarcodes.to_records(index=False)
#a[0][0] = 'CS18-DG2F-001'


for rangenumber in range (0,ranges): #ranges
    for rownumber in range (0,rows): #rows
        for plantnumber in range (0,stdcount): #standcount
            #create box coordinates
            x1 = x0-(cos(radbeta)*(rowwidth+rowspace)*rownumber)+(cos(radtheta)*(rowlen+rangespace)*rangenumber)+(cos(radtheta)*(rowlen/stdcount)*plantnumber)
            y1 = y0+(sin(radbeta)*(rowwidth+rowspace)*rownumber)+(sin(radtheta)*(rowlen+rangespace)*rangenumber)+(sin(radtheta)*(rowlen/stdcount)*plantnumber)

            x2 = x1+(cos(radtheta)*rowlen/stdcount)
            y2 = y1+(sin(radtheta)*rowlen/stdcount)

            x3 = x2-(sin(radtheta)*rowwidth)
            y3 = y2+(cos(radtheta)*rowwidth)

            x4 = x1-(cos(radbeta)*rowwidth)
            y4 = y1+(sin(radbeta)*rowwidth)


            #create ring
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(x1, y1)
            ring.AddPoint(x2, y2)
            ring.AddPoint(x3, y3)
            ring.AddPoint(x4, y4)
            ring.CloseRings()

            #create polygon
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
    
            #create feature and fields
            feature=ogr.Feature(layer.GetLayerDefn())
            feature.SetGeometry(poly)
            #if rangenumber%2==0:
            #        idtxt=txtbarcodes[(rows*(rangenumber+1)-(rownumber+1))][0]
            #else:
            #        idtxt=txtbarcodes[rows*rangenumber+rownumber][0]

            #feature.SetField('id',idtxt)
                
            #add layer
            layer.CreateFeature(feature)
        
            #destroy polygon and feature
            poly.Destroy()
            feature.Destroy()

#close file
ds.Destroy()
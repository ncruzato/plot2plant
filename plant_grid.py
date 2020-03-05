# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:12:44 2020

@author: Nathalia Cruzato
"""

#Input variables
#Origin point coordinates (row bottom letf)

#Second point coordinates (row top left)

#Row width or space between rows
## 2.5 ft or 0.762 m

#Row lenght
## G2F 21 ft (25 ft with allies)
## YC 8.5 ft (12.5 ft with allies)

#Space between plants or number of plot
## G2F 47seed/plot  MEAN 35.3, MEDIAN 36, MODE 36.5, MAX 41, max 
## YC 24 seed/plot  MEAN 12.5, MEDIAN 13, MODE 14, MAX 21

#Rotation
## -43 degrees

#number of ranges

#number of rows

import os, sys
import osgeo.ogr as ogr
import osgeo.osr as osr
#set directory
os.chdir('C:/Users/OWNER/OneDrive/Project 2')
#set up the shapefile driver
driver=ogr.GetDriverByName('ESRI Shapefile')

#create data source
fin='test_generation2.shp'
if os.path.exists(fin):
    driver.DeleteDataSource(fin)
    ds=driver.CreateDataSource(fin)
    print('file created')
    if ds is None:
        print('Could not create file', fin)
        sys.exit(1)

# create the spatial referece, WGS84, UTM Zone 14N, EPSG 32614
srs = osr.SpatialReference()
srs.ImportFromEPSG(32614)

#create the layer
layer = ds.CreateLayer('polygon', srs, geom_type=ogr.wkbPolygon)

#add fields
field_id=ogr.FieldDefn('id',ogr.OFTString)
field_id.SetWidth(24)
layer.CreateField(field_id)
id=1

# Create ring
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(746301.801, 3382007.260)
ring.AddPoint(746301.291, 3382007.736)
ring.AddPoint(746304.871, 3382011.337)
ring.AddPoint(746305.229, 3382010.899)

# Create polygon
poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(ring)
    
    #creation de la feature avec ses atributs associes a la forme
feature=ogr.Feature(layer.GetLayerDefn())
feature.SetGeometry(poly)
feature.SetField('id', 1)
    
    #ajout a la couche
layer.CreateFeature(feature)
    
poly.Destroy()
feature.Destroy()
#fermeture du fichier
ds.Destroy()
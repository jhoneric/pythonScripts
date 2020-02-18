import arcpy
from arcpy import env
from arcpy.sa import *
import os
import string
import requests
import time
import argparse
import sys


t0 = time.time()


parser = argparse.ArgumentParser(description='Images - Agencia Nacional Minera')
parser.add_argument('--mosaico', type=str, help="e.g. Mosaico_201701.lyr")
parser.add_argument('--month_title', type=str, help="e.g. ENERO 2017")
parser.add_argument('--solicitud', type=str, help="Path to file with shapefile for data driven pages")

args = parser.parse_args()

mosaico = "Mosaico_:201707.lyr" if not args.mosaico else args.mosaico
solicitud = "copia_sol.shp" if not args.solicitud else args.solicitud
month_title = "ENERO 2017" if not args.month_title else args.month_title


 
oplayerPath = r"C:\Imagenes_Satelitales_ANM\GDB\proyecto_imagenes.gdb\titulos\titulos_2018_04_10"
layerPath = os.path.join("C:\\", "Imagenes_Satelitales_ANM", 'MXD\\', 'lyr\\',mosaico) 
folderPath = os .path.join ("C:\\", "Imagenes_Satelitales_ANM", "MXD") 
mxdPath = os.path.join("C:\\", "Imagenes_Satelitales_ANM", 'MXD\\', 'Formato_Mapas_Mosaico.mxd')
out_mxd = os.path.join("Z:\\", "ATLAS", 'Formato_Mapas_JH.mxd')
shplayerPath = r"C:\Imagenes_Satelitales_ANM\SOLICITUDES"

#"\\10.0.100.45\IMG_Satelitales\ATLAS"
#"W:\ATLAS"
env.workspace = shplayerPath
arcpy.env.overwriteOutput = True

# reference to document map and dataframe

md = arcpy.mapping.MapDocument(mxdPath)
df = arcpy.mapping.ListDataFrames(md,"Titulo")[0]


# reference to mosaic layer

layer = arcpy.mapping.Layer(layerPath)
layer.visible = True

# add the layer to the map at the bottom of the TOC in data frame 0

print "adding:" + mosaico
arcpy.mapping.AddLayer(df, layer,"BOTTOM")

# refrencing operational layer

oplayer = arcpy.mapping.Layer(oplayerPath)

# swap the operational layer "titulos a realizar los mapas"

for lyr in arcpy.mapping.ListLayers(md, "Titulo"):

	print "checking layer name.....is " + lyr.name
	
	print "checking layer data source.....is " + lyr.dataSource

	if lyr.supports("DATASOURCE"):

		if lyr.dataSource == oplayerPath:
				lyr.replaceDataSource(shplayerPath, "SHAPEFILE_WORKSPACE", solicitud, "")
				lyr.name = "titulo"
				
				print "checking new layer data source.....is " + lyr.dataSource
				print "layer for data driven has been updated"

				if lyr.name == "titulo":

					oplayer = lyr
		

for elm in arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT"):
    if elm.text == "PERIODO":
        elm.text = month_title

arcpy.RefreshActiveView()

#print oplayer.dataSource
if oplayer.dataSource == os.path.join (shplayerPath, solicitud + ".shp"):
	#comprobando condicion
	#print "true"
	md.saveACopy(out_mxd)
	print "new map document has been created"
	print "Remenber change the name of mxd if you wish, mxd is in folder ATLAS"

else:

	print "There was anything wrong with shapefile, check your shp" 

ddp = md.dataDrivenPages
ddp.refresh()
c = ddp.pageCount
print "Generating.. {} pdf files".format(c)

for pageNum in range(1, c + 1):
	ddp.currentPageID = pageNum
	name = ddp.pageRow.CODIGO_EXP
	print "mapping title: " + name

	#Add corner coordinates
	ext = df.extent
	elem1 = ext.XMin
	elem2 = ext.YMax
	elem3 = ext.XMax
	elem4 = ext.YMin

#	print str(elem1) + "E"
#	print str(elem2) + "N"
#	print str (elem3) + "E"
#	print str(elem4) + "N"
	

	text1 = arcpy.mapping.ListLayoutElements (md, "TEXT_ELEMENT") [0]
	text1.text = str(round(elem2)) + " m N"

	text2 = arcpy.mapping.ListLayoutElements (md, "TEXT_ELEMENT") [1]
	text2.text = str(round(elem4)) + " m N"

	text3 = arcpy.mapping.ListLayoutElements (md, "TEXT_ELEMENT") [2]
	text3.text = str(round(elem3)) + " m E"

	text4 = arcpy.mapping.ListLayoutElements (md, "TEXT_ELEMENT") [3]
	text4.text = str(round(elem1)) + " m E"


	#print "Generating page {0} of {1}".format(str(ddp.currentPageID), str(c))
	
	#if not os.path.exists(os.path.join("W:\\", "ATLAS", month_title + "_" + name + ".pdf")):

	try:
		ddp.exportToPDF(os.path.join("Z:\\", "ATLAS", month_title + "_" + name), "CURRENT", image_quality='FASTEST')
		print "Page{0} of {1} has been generated".format(str(ddp.currentPageID), str(c))

	except AttributeError:
		ddp.exportToPDF(os.path.join("Z:\\", "ATLAS", month_title + "_" + name), "CURRENT", image_quality='FASTEST')
		print "Page{0} of {1} has been generated".format(str(ddp.currentPageID), str(c))


#multiple_files = "PDF_MULTIPLE_FILES_PAGE_NAME"

print "Files has been created"
print "Setting original values for next time"
del md, layer, oplayer

t1 = time.time()
duration = t1 - t0
print("successfully executed - total elapsed time: {} seconds".format(duration))

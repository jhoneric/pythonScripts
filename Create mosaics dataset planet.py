# Set the necessary product code

import os
import sys
import argparse
import arceditor
import time

# Import arcpy module
import arcpy
from arcpy import env


parser = argparse.ArgumentParser(description='Images - Agencia Nacional Minera')
parser.add_argument('--area', type=str, help="Area number")
parser.add_argument('--year', type=str, help="e.g. 2018")
parser.add_argument('--month', type=str, help="e.g. 01_enero")
parser.add_argument('--filters', type=str, help="e.g. *_SR_clip")

args = parser.parse_args()

area = "9" if not args.area else args.area
year = "2018" if not args.year else args.year
month = "03_marzo" if not args.month else args.month
filters = "*_SR_clip.tif" if not args.filters else args.filters

t0= time.time()
# provide location of rasters
Input_Rasters_Data_Folder = os.path.join("C:\\", "Imagenes_Satelitales_ANM", "area_" + area, "Raster", year, month)
#"C:\\Imagenes_Satelitales_ANM\\area_17\\Raster\\2018\\01_enero" 

# provide a wildcraf
Input_Data_Filter = filters 

# provide location of GDB to create
gdb_location = os.path.join("C:\\", "Imagenes_Satelitales_ANM", "area_" + area, "Mosaico", year, month)

# provide name of GDB to create

gdb_name = 'gdb_' + area + '_' + month + '_' + year

coords = "PROJCS['WGS_1984_UTM_Zone_18N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-75.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 -9998100 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision"

mosaic_name = 'mosaic_area_' + area + '_' + month + '_' + year

# Local variables:
m_location = gdb_location + "\\" + gdb_name + '.gdb'


arcpy.env.workspace = Input_Rasters_Data_Folder

#arcpy.env.overwriteOutput = True
# create file GDB

if  not os.path.exists(os.path.join("C:\\", "Imagenes_Satelitales_ANM", "area_" + area, "Mosaico", year, month, gdb_name + '.gdb')):
	arcpy.CreateFileGDB_management(gdb_location,gdb_name, "CURRENT")
	print "GDB" +" del area "+ area + " y" + " fecha " + year + month + " ha sido creada"
else:
	print ("GDB ya existe, verifique")
	print (" el script no puede continuar y se cerrara")
	sys.exit()

# Process: Create Mosaic Dataset
arcpy.CreateMosaicDataset_management(m_location, mosaic_name, coords, "4", "16_BIT_UNSIGNED", "NONE", "")

print "Dataset de Mosaico ha sido creado"


# Process: Create Statistics

rasters = arcpy.ListRasters(Input_Data_Filter)


for raster in rasters:
		
	arcpy.BuildPyramidsandStatistics_management(Input_Rasters_Data_Folder, "INCLUDE_SUBDIRECTORIES", "BUILD_PYRAMIDS", "CALCULATE_STATISTICS", "NONE", "", "NONE", "1", "1", "", "-1", "NONE", "NEAREST", "DEFAULT", "75", "OVERWRITE")

	print "se han caculado estadisticas a la imagen" + (raster)



# Process: Add Rasters To Mosaic Dataset
arcpy.AddRastersToMosaicDataset_management(m_location + "\\" + mosaic_name, "Raster Dataset", Input_Rasters_Data_Folder, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500", "", Input_Data_Filter, "NO_SUBFOLDERS", "ALLOW_DUPLICATES", "BUILD_PYRAMIDS", "CALCULATE_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE", "ESTIMATE_STATISTICS")

print "Los rasters se han agregado"

m = m_location + "\\" + mosaic_name


# Process: Build Footprints
arcpy.BuildFootprints_management(m, "", "RADIOMETRY", "0", "65535", "80", "0", "NO_MAINTAIN_EDGES", "NO_SKIP_DERIVED_IMAGES", "UPDATE_BOUNDARY", "2000", "100", "NONE", "", "20", "0,05")
print "Se han generado las huellas (footprints)"


# Process:  Color balance
arcpy.ColorBalanceMosaicDataset_management(m, "DODGING", "FIRST_ORDER", "", "", "NONE", "", "")
print "Se ha aplicado mejoramiento de color"

# Process: Build Seamlines

shp_name = "m_seamlines"

arcpy.BuildSeamlines_management(m, "", "NORTH_WEST", "", "", "", "", "RADIOMETRY", "10", "BOTH", "", "PIXELS", "PIXELS")
print "Se han generado las lineas de costura (seamlines)"
# Process: Export Mosaic Dataset Geometry
arcpy.ExportMosaicDatasetGeometry_management(m, m_location + "\\" + shp_name, "", "SEAMLINE")
print "se ha exportado la capa para editar seamlines"
print "Ya puede verificar el mosaico"
t1 = time.time()
duration = t1 - t0
print("successfully executed - total elapsed time: {} seconds".format(duration))
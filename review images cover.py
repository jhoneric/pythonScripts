import arcpy
from arcpy import env
from arcpy.sa import *
import os
import requests
import time
import argparse
import shutil



####################### Execute like: ############################

#maps_review.py --area 1 --year 2018 --month 01_enero

#python maps_review.py --area 57 --year 2018 --month 02_febrero

if __name__ == "__main__":

 if arcpy.CheckExtension("Spatial") == "Available":
  arcpy.CheckOutExtension("Spatial")

 #else:
     #raise LicenseError


 t0 = time.time()

 parser = argparse.ArgumentParser(description='Images - Agencia Nacional de Minería')
 parser.add_argument('--area', type=str, help="Area number")
 parser.add_argument('--year', type=str, help="e.g. 2018")
 parser.add_argument('--month', type=str, help="e.g. 01_enero")
 
 

 args = parser.parse_args()

 area = "66" if not args.area else args.area
 year = "2018" if not args.year else args.year
 month = "01_enero" if not args.month else args.month


 ide = "Id"
 where = '"' + ide + '" = ' + str(area)
 month_str = month[3:]
 print "Working on: Polygon: " + "Area:"+ area +"  " +"Month:"+ month_str + "  " + "Year:" +year


 file_path = os.path.join("C:\\", "Imagenes_Satelitales_ANM", "area_" + area, "Raster", year, month)
 footprint = os.path.join("C:\\", "Imagenes_Satelitales_ANM", "area_" + area, "Raster", year, month, "temp")
 mxdPath = os.path.join("C:\\", "Imagenes_Satelitales_ANM", 'MXD\\', 'Formato_Revision.mxd')
 gdb = os.path.join("C:\\", "Imagenes_Satelitales_ANM",'GDB', 'proyecto_imagenes.gdb')

 env.workspace = file_path

 arcpy.env.overwriteOutput = True

 #Remove temp folder if exits
 for files in os.listdir(file_path):
    if files == "temp":
        shutil.rmtree(file_path + "\\temp")

 print ("Getting ready ...")

 md = arcpy.mapping.MapDocument(mxdPath)
 df = arcpy.mapping.ListDataFrames(md)[0]

 lyr = arcpy.mapping.ListLayers(md)[0]
 arcpy.SelectLayerByAttribute_management (lyr, 'NEW_SELECTION', where)
 df.zoomToSelectedFeatures()

 legend = arcpy.mapping.ListLayoutElements(md, "LEGEND_ELEMENT")[0]
 legend.autoAdd = False

 rasterlist = arcpy.ListRasters("*MS_SR*","tif")
 count = len(rasterlist) + 1
 print "Number of images: " + str(count)

 if not rasterlist:
  print "Polygon without images ....!!"
  exit()

 if not os.path.exists(footprint):
  os.makedirs(footprint)
 
 print ("Processing raster data ...")

 for raster in rasterlist:

   result = arcpy.MakeRasterLayer_management(raster, '_'+raster)
   layer = result.getOutput(0)
   arcpy.mapping.AddLayer(df, layer, 'AUTO_ARRANGE')
   #print raster

   outReclassify = Raster(raster) >= 0

   out_put_fp = os.path.join(file_path, footprint, raster)
   outReclassify.save(out_put_fp)
   arcpy.RasterToPolygon_conversion (out_put_fp, out_put_fp + "_SR", "SIMPLIFY", "")
   



 arcpy.Delete_management(outReclassify)

 env.workspace = footprint
 arcpy.env.overwriteOutput = True
 shplist =  arcpy.ListFeatureClasses('*.shp')
 

 print ("Processing vector data ...")
 for fc in shplist:
     #print str("processing " + fc)

     # Define field name and expression
     field = "ID_Image"
     expression = str(fc) #populates field   

     # Create a new field with a new name
     arcpy.AddField_management(fc,field,"TEXT")

     # Calculate field here
     arcpy.CalculateField_management(fc, field, '"'+expression[:-4]+'"', "PYTHON")

 #print ("Merging vector data ...")
 #Merge images footprint 
 merged = os.path.join(footprint, 'imagery_area_' + area + '_' + year + '_' + month + '_SR' + '.shp')
 arcpy.Merge_management(shplist, merged)

 #Filling area field
 arcpy.AddField_management(merged, "area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(merged, "area", area, "PYTHON_9.3", "")

 #Filling year field
 arcpy.AddField_management(merged, "year", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(merged, "year", year, "PYTHON_9.3", "")

 #Filling month field
 arcpy.AddField_management(merged, "month", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(merged, "month", '"'+month_str+'"', "PYTHON_9.3", "")

 #calculating area: Magna Colombia Bogota (Magna): 3116 or Colombia Bogota Zone (Datum Bogota): 21897
 geoSR = arcpy.SpatialReference(3116) 
 arcpy.AddGeometryAttributes_management (merged, 'AREA',"", 'SQUARE_KILOMETERS', geoSR)
 arcpy.AddField_management(merged, "magna_km2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(merged, "magna_km2", "!POLY_AREA!", "PYTHON_9.3", "")
 arcpy.DeleteField_management (merged, "POLY_AREA")


 print ("Calculating images coverage ...")
  
 dissolved = os.path.join(footprint, 'Dissolved_area_' + area + '_' + year + '_' + month + '_SR' + '.shp')
 arcpy.Dissolve_management (merged, dissolved, "GRIDCODE", "", "MULTI_PART", "DISSOLVE_LINES")

 intersect = os.path.join(footprint, 'intersect_area_' + area + '_' + year + '_' + month + '_SR' + '.shp')
 arcpy.Intersect_analysis ([lyr, dissolved], intersect, "ALL", "", "INPUT")


 intersected = os.path.join(footprint, 'intersect_pr_area_' + area + '_' + year + '_' + month + '_SR' + '.shp')
 arcpy.Project_management(intersect, intersected, geoSR)
 
 arcpy.AddGeometryAttributes_management (intersected, 'AREA',"", 'SQUARE_KILOMETERS', geoSR)
 arcpy.AddField_management(intersected, "area_diss", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(intersected, "area_diss", "!POLY_AREA!", "PYTHON_9.3", "")
 

 # Process: Add Field 
 arcpy.AddField_management(intersected, "cover", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
 # Process: Calculate Field 
 arcpy.CalculateField_management(intersected, "cover", "!area_diss! /!d_mag_km!*100.0", "PYTHON_9.3", "")

  #Filling area field
 arcpy.AddField_management(intersected, "area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(intersected, "area", area, "PYTHON_9.3", "")

 #Filling year field
 arcpy.AddField_management(intersected, "year", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(intersected, "year", year, "PYTHON_9.3", "")

 #Filling month field
 arcpy.AddField_management(intersected, "month", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(intersected, "month", '"'+month_str+'"', "PYTHON_9.3", "")

 arcpy.AddField_management(intersected, "imagery", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") 
 arcpy.CalculateField_management(intersected, "imagery", count, "PYTHON_9.3", "")



 texts = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")
 lyr = arcpy.mapping.ListLayers(md)[0]
 cursor1 = arcpy.da.SearchCursor(lyr, ["Id", "zona", "Ingeniero", "d_mag_km"], where)



 for row in cursor1:
     id_text = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[6]
     id_text.text = row[0]

     zona_text = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[7]
     zona_text.text = row[1].title()

     descarga_text = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[8]
     descarga_text.text = row[2]

     area_text = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[0]
     area_text.text = "(" + str(round(row[3],2)) + " " + "km2)"

 cursor2 = arcpy.da.SearchCursor(intersected, ["cover"], where)

 for row in cursor2:
  cover_text = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[2]
  cover_text.text = round(row[0], 2)


 anio = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[5]
 anio.text = year

 month_text = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[4]
 month_text.text = month_str

 date_str = (time.strftime("%Y/%m/%d %H:%M:%S"))


 date_text = arcpy.mapping.ListLayoutElements(md, "TEXT_ELEMENT")[3]
 date_text.text = date_str

 #Deleting cursors
 del row
 del cursor1
 del cursor2

 arcpy.SelectLayerByAttribute_management (lyr, 'CLEAR_SELECTION', where)

 print "Genereting PDF and MXD ..."
 # Genereting PDF and MXD
 arcpy.RefreshActiveView()
 out_put_pdf = 	os.path.join(file_path, 'area_' + area + '_' + year + '_' + month + '_SR' + '.pdf')
 out_put_mxd = 	os.path.join(file_path, 'area_' + area + '_' + year + '_' + month + '_SR' + '.mxd')
 out_put_jpg =  os.path.join(file_path, 'area_' + area + '_' + year + '_' + month + '_SR' + '.jpg')
 
 #md.save()
 #print 'mxd::'
 md.saveACopy(out_put_mxd)
 #shutil.copy2(mxdPath, out_put_mxd)

 #time.sleep(60)

 for remaining in range(30, 4, -1):
     sys.stdout.write("\r")
     sys.stdout.write("{:2d} seconds remaining ...".format(remaining))
     sys.stdout.flush()
     time.sleep(1)

 #sys.stdout.write("\rComplete!            \n")

 try:
    arcpy.mapping.ExportToPDF(md, out_put_pdf, image_quality = 'BETTER')
    sys.stdout.write("\rPDF Best Quality Export Complete!            \n")

 except AttributeError:
    arcpy.mapping.ExportToPDF(md, out_put_pdf, image_quality = 'NORMAL')
    sys.stdout.write("\rPDF Better Quality Export Complete!            \n")
 except AttributeError:
    arcpy.mapping.ExportToPDF(md, out_put_pdf, image_quality = 'BEST')
    sys.stdout.write("\rPDF Normal Quality Export Complete!            \n")
 except AttributeError:
    arcpy.mapping.ExportToPDF(md, out_put_pdf, image_quality = 'FASTER')
    sys.stdout.write("\rPDF Faster Quality Export Complete!            \n")
 except AttributeError:
    arcpy.mapping.ExportToPDF(md, out_put_pdf, image_quality = 'FASTEST')
    sys.stdout.write("\rPDF Fastest Quality Export Complete!            \n")
 finally:
    arcpy.mapping.ExportToJPEG(md, out_put_jpg)
    sys.stdout.write("\rJPG Map Export Complete!            \n")



 # Remove images from dataframe
 for lyr in arcpy.mapping.ListLayers(md, "*MS_SR*", df):
 	arcpy.mapping.RemoveLayer(df, lyr)

 print "Deleting temporal files ..."
 # Delete footprint shapefiles from disk 
 for shp in shplist:  
  arcpy.Delete_management(shp) 
 # Delete footprint raster from disk 
 footprint_list = arcpy.ListRasters("*MS_SR*","tif")
 for fp_list in footprint_list:  
  arcpy.Delete_management(fp_list)



 #deleting intersect shapefile
 arcpy.Delete_management(intersect)

 # Deleting unnecessary fields
 arcpy.DeleteField_management (merged, "ID") 
 arcpy.DeleteField_management (merged, "GRIDCODE") 
 arcpy.DeleteField_management (intersected, "POLY_AREA")
 arcpy.DeleteField_management (intersected, "GRIDCODE")
 arcpy.DeleteField_management (intersected, "Id") 
 arcpy.DeleteField_management (intersected, "FID_Dissol")
 arcpy.DeleteField_management (intersected, "FID_area_c")
 arcpy.DeleteField_management (intersected, "Shape_Leng")
 arcpy.DeleteField_management (intersected, "Shape_Area")

 print ("Importing to Geodatabase ...")
 
 f_imagery = os.path.join("C:\\", "Imagenes_Satelitales_ANM",'GDB', 'proyecto_imagenes.gdb','cobertura_imagenes', 'imagery_area_' + area + '_' + year + '_' + month + '_SR' )  
 f_intersect = os.path.join("C:\\", "Imagenes_Satelitales_ANM",'GDB', 'proyecto_imagenes.gdb','cobertura_imagenes', 'intersect_area_' + area + '_' + year + '_' + month + '_SR' )  

 #Checking if the merged file exists


 if arcpy.Exists(f_imagery):
 	print ("Imagery feature class exists !!! ...")
 	arcpy.Delete_management(f_imagery)
 	arcpy.FeatureClassToGeodatabase_conversion(merged, gdb + '\cobertura_imagenes')
 	print ("Overwrited !!!") 
 else:
 	arcpy.FeatureClassToGeodatabase_conversion(merged, gdb + '\cobertura_imagenes')
 	print ("Imagery feature class created !!!")

 magna = arcpy.SpatialReference(4686)

 if arcpy.Exists(f_intersect):
 	print ("Intersect feature class exists !!! ...")
 	arcpy.Delete_management(f_intersect)
 	arcpy.Project_management(intersected, f_intersect, magna)
 	#arcpy.FeatureClassToGeodatabase_conversion(intersected, gdb + '\cobertura_imagenes')
 	print ("Overwrited !!!") 
 else:
 	arcpy.Project_management(intersected, f_intersect, magna)
 	#arcpy.FeatureClassToGeodatabase_conversion(intersected, gdb + '\cobertura_imagenes')
 	print ("Intersect feature class created !!!")

 #Deleting Shapefiles
 arcpy.Delete_management(intersect)
 arcpy.Delete_management(intersected)
 arcpy.Delete_management(dissolved)
 arcpy.Delete_management(merged)

 shutil.rmtree(file_path + "\\temp")


  #Remove footprint folder if exits
 for files in os.listdir(file_path):
 	if files == "info":
 		shutil.rmtree(file_path + "\\info")



 md.save()
 del rasterlist
 del md

 t1 = time.time()
 duration = t1 - t0
 print("successfully executed - total elapsed time: {} seconds".format(duration))
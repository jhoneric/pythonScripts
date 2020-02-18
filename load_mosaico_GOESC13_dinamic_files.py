# Set the necessary product code
#Prueba mosaicos canal 13
import sys, os, arcpy
import time
from datetime import datetime

# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = u'/u01/Data/Servicios/Conexiones/172.16.50.4(Raster).sde/gdbideam.raster.GOES16_C13'
#g_ESRI_variable_1 = r"\\172.16.50.8\Data\Servicios\Conexiones\172.16.50.4(Raster).sde\gdbideam.raster.GOES16_C13"
g_ESRI_variable_3 = u'raster.GOES16_C13_View'
g_ESRI_variable_4 = u'fecha'
g_ESRI_variable_5 = u'CalculoFecha( !name! )'
g_ESRI_variable_6 = u'diferencia'
g_ESRI_variable_7 = u'CalculoDias( !fecha! )'
g_ESRI_variable_8 = u'diferencia >7 OR diferencia IS NULL'
g_ESRI_variable_9 = u'objectid objectid VISIBLE NONE;name name VISIBLE NONE;minps minps VISIBLE NONE;maxps maxps VISIBLE NONE;lowps lowps VISIBLE NONE;highps highps VISIBLE NONE;category category VISIBLE NONE;tag tag VISIBLE NONE;groupname groupname VISIBLE NONE;productname productname VISIBLE NONE;centerx centerx VISIBLE NONE;centery centery VISIBLE NONE;zorder zorder VISIBLE NONE;typeid typeid VISIBLE NONE;itemts itemts VISIBLE NONE;urihash urihash VISIBLE NONE;uri uri VISIBLE NONE;shape shape VISIBLE NONE;raster raster VISIBLE NONE;fecha fecha VISIBLE NONE;diferencia diferencia VISIBLE NONE;st_area(shape) st_area(shape) VISIBLE NONE;st_length(shape) st_length(shape) VISIBLE NONE'
g_ESRI_variable_10 = u'name'
g_ESRI_variable_11 = u'evaluateZorder("/u01/Data/Servicios/Conexiones/172.16.50.4(Raster).sde/gdbideam.raster.GOES16_C13")'

# Import arcpy module
import arcpy
# Local variables:

gdbideam_raster_GOES16_C13 = g_ESRI_variable_1
raster_GOES16_C13_View = g_ESRI_variable_3

RPATHS = "Z:\u01\Data\GOES\C13 /u01/Data/GOES/C13"

Folder1 = "/u01/Data/GOES/Temporal/GOES/C13"
#Folder1 = r"\\172.16.50.8\Data\GOES\Temporal\GOES\C13_1"
Rasters_Folder = "/u01/Data/GOES/C13"
#Rasters_Folder = r"\\172.16.50.8\Data\GOES\C13"

arcpy.env.workspace = Folder1

rasters = arcpy.ListRasters("*", "tif")

arcpy.AddMessage("listing rasters from the temporal folder GOES:{}" .format(rasters))
L = len(rasters)

#print ("The length of list is: ", len(rasters))
#arcpy.AddMessage("The number of images for adding to mosaic is:{}".format(L))

NEWLIST = []

if not rasters:
    arcpy.AddMessage("No images in temporal folder")
    sys.exit()
else:
    
    for raster in rasters:
        BASEFILE = str(raster)
        arcpy.AddMessage("raster name is:{}" .format(BASEFILE))
        FILENAME = os.path.splitext(BASEFILE)[0]
        #arcpy.AddMessage("nombre del archivo es sin extension es:{}".format (FILENAME))
        
        current_time = datetime.now()
        #year = current_time.strftime("%Y")
        #month = current_time.strftime("%m")
        #day = current_time.strftime("%d")
        
        today_string = current_time.strftime("%Y%m%d")
        #arcpy.AddMessage("today: {}".format(today_string))

        DATE = BASEFILE[4:12]
        #arcpy.AddMessage("fechas desde el raster:{}".format(DATE))
            
        if DATE == today_string:
                NEWLIST.append("{}/{}".format(Rasters_Folder,BASEFILE))
                #NEWLIST = Input_Data_Filter
    
    arcpy.AddMessage(NEWLIST)
    #arcpy.AddMessage(Input_Data_Filter)
    FILTER = "*"+today_string+"*"
    #arcpy.AddMessage(FILTER)
    
    if not NEWLIST:
        arcpy.AddMessage("Images in tmeporal folder are not from today")
        sys.exit()
    else:
        arcpy.AddMessage("The following images will be added to mosaic dataset: {}".format(NEWLIST))
        # Process: Add Rasters To Mosaic Dataset
        arcpy.AddRastersToMosaicDataset_management(gdbideam_raster_GOES16_C13, "Raster Dataset", NEWLIST, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500", "", "", "NO_SUBFOLDERS", "EXCLUDE_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE", "NO_STATISTICS", "")
        arcpy.AddMessage("Mosaic dataset updated")
        # Process: Calculate Field
        arcpy.CalculateField_management(gdbideam_raster_GOES16_C13, g_ESRI_variable_4, g_ESRI_variable_5, "PYTHON_9.3", "try: \\n def CalculoFecha(field):\\n    Fecha=field[4:]\\n    return Fecha;\\nexcept:\\n    pass;")
        # Process: Calculate Field (2)
        arcpy.CalculateField_management(gdbideam_raster_GOES16_C13, g_ESRI_variable_6, g_ESRI_variable_7, "PYTHON_9.3", "from datetime import datetime, date, timedelta\\ndef CalculoDias(Fecha):\\n      try:\\n            FechaImagen = datetime.strptime(Fecha[0:4]+Fecha[4:6]+Fecha[6:8],'%Y%m%d').date();\\n            Diferencia = datetime.now().date()-FechaImagen;\\n            return Diferencia.days;\\n      except:\\n            pass")
        # Process: Remove Rasters From Mosaic Dataset
        arcpy.RemoveRastersFromMosaicDataset_management(gdbideam_raster_GOES16_C13, g_ESRI_variable_8, "UPDATE_BOUNDARY", "MARK_OVERVIEW_ITEMS", "DELETE_OVERVIEW_IMAGES", "DELETE_ITEM_CACHE", "REMOVE_MOSAICDATASET_ITEMS", "UPDATE_CELL_SIZES")
        # Process: Make Table View
        try:
            arcpy.MakeTableView_management(gdbideam_raster_GOES16_C13, raster_GOES16_C13_View, "", "", g_ESRI_variable_9)
        except:
            pass
        # Process: Delete Identical
        try:
            arcpy.DeleteIdentical_management(raster_GOES16_C13_View, g_ESRI_variable_10, "", "0")
        except:
            pass
        # Process: Calculate Value (3)
        arcpy.CalculateValue_management(g_ESRI_variable_11, "# Variables locales\\nzOrderField = \"zorder\"\\ndateField = \"Fecha\"\\n\\n# Importar librerias\\nimport arcpy\\ntry:\\n def evaluateZorder(table):\\n     # CreaciÃ³n de cursor de actualizaciÃ³n\\n     sqlClause = (None, 'ORDER BY {0} DESC'.format(dateField))\\n     flag = 0\\n     with arcpy.da.UpdateCursor(table, [zOrderField, dateField], sql_clause = sqlClause) as cursor:\\n         for row in cursor:\\n             if flag == 0:\\n                 row[0] = -10\\n                 flag = 1\\n             else:\\n                 row[0] = 0\\n             cursor.updateRow(row)\\n     return True\\nexcept:\\n pass", "Boolean")

        # Process: Repair Mosaic Dataset Paths
        arcpy.RepairMosaicDatasetPaths_management(gdbideam_raster_GOES16_C13, RPATHS, "")

arcpy.AddMessage("Finished script")


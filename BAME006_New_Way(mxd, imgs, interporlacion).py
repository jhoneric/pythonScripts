# Esri start of added imports
import sys, os, arcpy
# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = u'querytable'
g_ESRI_variable_2 = u'in_memory/result_idw'
g_ESRI_variable_3 = u'in_memory/result_extract'
g_ESRI_variable_4 = u'in_memory/reclass_extract'
g_ESRI_variable_5 = u'in_memory/estaciones'
g_ESRI_variable_6 = u'estaciones_view'
g_ESRI_variable_7 = u'estaciones_layer'
g_ESRI_variable_8 = u'archivo_view'
g_ESRI_variable_9 = u'objectid objectid VISIBLE NONE;idestacion idestacion VISIBLE NONE;nombre nombre VISIBLE NONE;idcategoria idcategoria VISIBLE NONE;idtecnologiatm idtecnologiatm VISIBLE NONE;idtipotransmisiontm idtipotransmisiontm VISIBLE NONE;idestadoestaciontm idestadoestaciontm VISIBLE NONE;fechainstalacion fechainstalacion VISIBLE NONE;altitud altitud VISIBLE NONE;latitud latitud VISIBLE NONE;longitud longitud VISIBLE NONE;iddepartamento iddepartamento VISIBLE NONE;idmunicipio idmunicipio VISIBLE NONE;idareaoperativa idareaoperativa VISIBLE NONE;idareahidrografica idareahidrografica VISIBLE NONE;idzonahidrografica idzonahidrografica VISIBLE NONE;codigowmo codigowmo VISIBLE NONE;codigointerno codigointerno VISIBLE NONE;codigoiata codigoiata VISIBLE NONE;codigonesdsdis codigonesdsdis VISIBLE NONE;codigooaci codigooaci VISIBLE NONE;identidad identidad VISIBLE NONE;usuario usuario VISIBLE NONE;fechaultimamodificacion fechaultimamodificacion VISIBLE NONE;codigoorfeo codigoorfeo VISIBLE NONE;observacion observacion VISIBLE NONE;idcorriente idcorriente VISIBLE NONE;fechasuspension fechasuspension VISIBLE NONE;idaquarius idaquarius VISIBLE NONE;idgis idgis VISIBLE NONE;idsubzonahidrografica idsubzonahidrografica VISIBLE NONE;prop_cod prop_cod VISIBLE NONE;prop_sector prop_sector VISIBLE NONE;familia familia VISIBLE NONE;clase clase VISIBLE NONE;temp temp VISIBLE NONE;prop_nom prop_nom VISIBLE NONE;prop_tipo prop_tipo VISIBLE NONE;shape shape VISIBLE NONE;ID_ESTACION ID_ESTACION VISIBLE NONE'
g_ESRI_variable_10 = u'ID_ESTACION'
g_ESRI_variable_11 = u'!idestacion!'
g_ESRI_variable_12 = u'IDESTACION IDESTACION VISIBLE NONE;VALOR VALOR VISIBLE NONE'
g_ESRI_variable_13 = u'IDESTACION'
g_ESRI_variable_14 = u'Estaciones.longitud'
g_ESRI_variable_15 = u'Estaciones.latitud'
g_ESRI_variable_16 = u'Estaciones.altitud'
g_ESRI_variable_17 = u'VALUE'
# Esri end of added variables

# -*- #################
# ---------------------------------------------------------------------------
# BAME006.py
# ---------------------------------------------------------------------------
'''BAME006'''
# Import libs
import os
import datetime
import time
import calendar
import json
import zipfile
import arcpy


class LicenseError(Exception):
    '''Clase creada para obtener el error de licencia'''
    pass


class ParamError(Exception):
    '''Clase creada para obtener el error de imágenes no encontradas'''
    pass


class Subred(object):
    ''' Clase encargada de retornar la subred escogida '''
    def __init__(self, base):
        self.base = base
        self.subred = -1

    def run(self, argument):
        """Método despachador"""
        method_name = str(argument)
        self.subred = int(argument[3:])
        if self.subred == 0 or self.subred == 13:
            method = getattr(self, method_name, self.default)
        else:
            method = getattr(self, "AMEALL", self.default)
        return method()

    def AME00(self):
        '''Método que retorna la subred AME00'''
        variable = os.path.join(self.base, "Colombia_croquis")
        return variable

    def AMEALL(self):
        '''Método que retorna la subred de la zona productora'''
        # Process: Make Query Table
        variable = g_ESRI_variable_1
        arcpy.MakeQueryTable_management(os.path.join(self.base, "Zona_Productora"), variable, "USE_KEY_FIELDS", "", "", "No_Zona = '{}'".format(self.subred))
        return variable

    def AME13(self):
        '''Método que retorna la subred AME13'''
        variable = os.path.join(self.base, "altiplano_cundiboyacense")
        return variable

    def default(self):
        '''Método que ejecuta un error cuando no es opción valida'''
        arcpy.AddError("No es una subred válida.")

BOLETIN = "BAME006"
PATHPUBLIC = "/u01/Data/AmeYCli/AmeYCli/products"
PATHGET = "/u01/Data/AmeYCli/AmeYCli/IDH"
ENVIRO = "/u01/Data/AmeYCli/AmeYCli"
BASE = "{}/AMEYCLIM.gdb".format(ENVIRO)
BASESDE = "{}/GDBIDEAM.sde".format(ENVIRO)
COLOMBIA_CROQUIS = "{}/Colombia_croquis".format(BASESDE)
ESTACIONESSDE = "{}/Estaciones".format(BASESDE)
#PATHPUBLIC = r"\\172.16.50.8\Data\AmeYCli\AmeYCli\products"
#PATHGET = r"\\172.16.50.8\Data\AmeYCli\AmeYCli\IDH"
#ENVIRO = r"\\172.16.50.8\Data\AmeYCli\AmeYCli"
#BASE = os.path.join(ENVIRO, "AMEYCLIM.gdb")
#BASESDE = os.path.join(ENVIRO, "GDBIDEAM.sde")
#COLOMBIA_CROQUIS = os.path.join(BASESDE, "Colombia_croquis")
#ESTACIONESSDE = os.path.join(BASESDE, "Estaciones")
#LINK = "http://172.16.50.8:6080/server/rest/directories/ameycli"
LINK = "http://dhime.ideam.gov.co/server/rest/directories/ameycli"
PLANTILLA_JPG_COLOMBIA = os.path.join(ENVIRO, "resources", "template", "{}_Colombia_JPG.mxd".format(BOLETIN))
PLANTILLA_GIF_COLOMBIA = os.path.join(ENVIRO, "resources", "template", "{}_Colombia_GIF.mxd".format(BOLETIN))
PLANTILLA_JPG_ALTI = os.path.join(ENVIRO, "resources", "template", "{}_Altiplano_JPG.mxd".format(BOLETIN))
PLANTILLA_GIF_ALTI = os.path.join(ENVIRO, "resources", "template", "{}_Altiplano_GIF.mxd".format(BOLETIN))
PLANTILLA_JPG_ZONA = os.path.join(ENVIRO, "resources", "template", "{}_Zona_JPG.mxd".format(BOLETIN))
PLANTILLA_GIF_ZONA = os.path.join(ENVIRO, "resources", "template", "{}_Zona_GIF.mxd".format(BOLETIN))
SYMBOLOGY = os.path.join(ENVIRO, "resources", "symbology", "symbology_bame006.lyr")
MES = arcpy.GetParameterAsText(0)
ANIO = arcpy.GetParameterAsText(1)
SUBRED = arcpy.GetParameterAsText(2)
ARCHIVOZIP = arcpy.GetParameterAsText(3)
PATH = os.path.join(PATHPUBLIC, str(ANIO), str(MES), BOLETIN, SUBRED)
if not os.path.exists(PATH):
    os.makedirs(PATH, 0777)
PATHPARAMS = os.path.join(PATHGET, str(ANIO), str(MES))
CROKISGEO_LYR = os.path.join(ENVIRO, "resources", "symbology", "crokisgeo.lyr")
AMERICA_PAISES_LYR = os.path.join(ENVIRO, "resources", "symbology", "america_paises.lyr")
LINK = "{}/{}/{}/{}/{}".format(LINK, str(ANIO), str(MES), BOLETIN, SUBRED)
arcpy.env.scratchWorkspace = PATH
arcpy.env.workspace = BASE
arcpy.env.overwriteOutput = True
RESULT_IDW = g_ESRI_variable_2
RESULT_EXTRACT = g_ESRI_variable_3
RECLASS_EXTRACT = g_ESRI_variable_4
ESTACIONES = g_ESRI_variable_5
ESTACIONES_VIEW = g_ESRI_variable_6
ESTACIONES_LAYER = g_ESRI_variable_7
ARCHIVO_VIEW = g_ESRI_variable_8
MESES = {"01": "Enero",
         "02": "Febrero",
         "03": "Marzo",
         "04": "Abril",
         "05": "Mayo",
         "06": "Junio",
         "07": "Julio",
         "08": "Agosto",
         "09": "Semptiembre",
         "10": "Octubre",
         "11": "Noviembre",
         "12": "Diciembre"}
NOMBRE_SUBRED = {"AME01": "Norte de Cesar y La Guajira",
                 "AME02": "Atl\xe1ntico, Magdalena y Norte de Bol\xedvar",
                 "AME03": "C\xf3rdoba, Sucre, Sur de Bol\xedvar, \nUrab\xe1 y Bajo Cauca Antioque\xf1o",
                 "AME04": "Magdalena Medio",
                 "AME05": "Norte de Santander, Oriente de Arauca\ny Nororiente",
                 "AME06": "Zona cafetera",
                 "AME07": "Altiplano Cundiboyacense y\noriente de Santander",
                 "AME08": "Piedemonte y Altillanura Meta -\nCasanare - Arauca",
                 "AME09": "Alto Magdalena Huila - Tolima",
                 "AME10": "Valle geogr\xe1fico Rio Cauca",
                 "AME11": "Altiplano Nariñense - Pac\xedfico",
                 "AME12": "Piedemonte Caqueta y Putumayo",
                 "AME14": "Choco",
                 "AME15": "Planicie de Putumayo",
                 "AME16": "Orinoquia y Amazonia"}
IDHS = ["1D", "2D", "3D", "M"]
TEXTO_DECADA_JPG = {"1D": "Primera d\xe9cada (1 al 10)",
                    "2D": "Segunda d\xe9cada (11 al 20)",
                    "3D": "Tercera d\xe9cada (21 al {})".format(calendar.monthrange(int(ANIO), int(MES))[1]),
                    "M": "Mensual"}
TEXTO_DECADA_GIF = {"1D": "Primera d\xe9cada",
                    "2D": "Segunda d\xe9cada",
                    "3D": "Tercera d\xe9cada",
                    "M": "Mensual"}
PRODUCTS = []

try:
    if not os.path.exists(PATH) or not os.path.exists(PATHPARAMS):
        raise ParamError
    for IDH in IDHS:
        if not os.path.exists(os.path.join(PATHPARAMS, "{}.CSV".format(IDH))):
            raise ParamError
    # Check out the Spatial Analysis
    if arcpy.CheckOutExtension("Spatial") == "Available" or arcpy.CheckOutExtension("Spatial") == "CheckedOut":
        arcpy.CheckOutExtension("Spatial")
    else:
        raise LicenseError
    # Process: Copy Estaciones
    arcpy.CopyFeatures_management(ESTACIONESSDE, ESTACIONES)

    # Process: Make Table View - Estaciones
    arcpy.MakeTableView_management(ESTACIONES, ESTACIONES_VIEW, "", "", g_ESRI_variable_9)

    # Process: Add Field
    arcpy.AddField_management(ESTACIONES_VIEW, "ID_ESTACION", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(ESTACIONES_VIEW, g_ESRI_variable_10, g_ESRI_variable_11, "PYTHON_9.3", "")

    # Process: Get layers

    CROKISGEO_LYR = arcpy.mapping.Layer(CROKISGEO_LYR)
    AMERICA_PAISES_LYR = arcpy.mapping.Layer(AMERICA_PAISES_LYR)

    NUMSUBRED = int(SUBRED[3:])
    if NUMSUBRED == 0:
        PLANTILLA_JPG = PLANTILLA_JPG_COLOMBIA
        PLANTILLA_GIF = PLANTILLA_GIF_COLOMBIA
    elif NUMSUBRED == 13:
        PLANTILLA_JPG = PLANTILLA_JPG_ALTI
        PLANTILLA_GIF = PLANTILLA_GIF_ALTI
    else:
        PLANTILLA_JPG = PLANTILLA_JPG_ZONA
        PLANTILLA_GIF = PLANTILLA_GIF_ZONA
    # Process: Calculate for each one
    for IDH in IDHS:
        NOMBRE_IMAGEN = "{}-{}-{}".format(BOLETIN, IDH, SUBRED)
        # Process: Make Table View - Data
        arcpy.MakeTableView_management(os.path.join(PATHPARAMS, "{}.CSV".format(IDH)), ARCHIVO_VIEW, "", "", g_ESRI_variable_12)

        #arcpy.AddMessage([row for row in arcpy.da.SearchCursor(ARCHIVO_VIEW, ["*"])])

        # Process: Add Join
        arcpy.AddJoin_management(ESTACIONES_VIEW, g_ESRI_variable_10, ARCHIVO_VIEW, g_ESRI_variable_13, "KEEP_COMMON")

        # Process: Make XY Event Layer
        arcpy.MakeXYEventLayer_management(ESTACIONES_VIEW, g_ESRI_variable_14, g_ESRI_variable_15, ESTACIONES_LAYER, "GEOGCS['GCS_MAGNA',DATUM['D_MAGNA',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119521E-09;0,001;0,001;IsHighPrecision", g_ESRI_variable_16)

        # Process: IDW
        TEMPENVIRONMENT = arcpy.env.extent
        arcpy.env.extent = COLOMBIA_CROQUIS
        #RESULT_IDW = arcpy.sa.Idw(ESTACIONES_LAYER, "{}.CSV.VALOR".format(IDH), 0.01, 2)
        arcpy.gp.Idw_sa(ESTACIONES_LAYER, "{}.CSV.VALOR".format(IDH), RESULT_IDW, "0,01", "2", "VARIABLE 12", "")
	        
        arcpy.env.extent = TEMPENVIRONMENT

        # Process: Extract by Mask
        SWITCH = Subred(BASESDE)
        SUBREDLYR = SWITCH.run(SUBRED)
        arcpy.gp.ExtractByMask_sa(RESULT_IDW, SUBREDLYR, RESULT_EXTRACT)

        # Process: Reclassify
        PARAM_RECLASS = "0 30 1;30 60 2;60 90 3;90 110 4;110 140 5;140 170 6;170 2000 7"
        arcpy.gp.Reclassify_sa(RESULT_EXTRACT, g_ESRI_variable_17, PARAM_RECLASS, RECLASS_EXTRACT, "NODATA")

        
        # Process: TIF
        
        arcpy.CopyRaster_management(RECLASS_EXTRACT, os.path.join(PATH, "{}.tif".format(NOMBRE_IMAGEN)))
        PRODUCTS.append("{}/{}.tif".format(LINK, NOMBRE_IMAGEN))
        arcpy.AddMessage(NOMBRE_IMAGEN)

        
    arcpy.env.workspace = PATH
    rasterlist = arcpy.ListRasters("*", "tif")
    arcpy.AddMessage(rasterlist)
    
   
    for r in rasterlist:

        MXD = arcpy.mapping.MapDocument(PLANTILLA_JPG)
        DF0 = arcpy.mapping.ListDataFrames(MXD)[0]
        
        raster = arcpy.MakeRasterLayer_management(r,'_'+r)
        LYR = raster.getOutput(0)
        
        # Process: Get result
        #LYR = arcpy.mapping.Layer(raster)

        # Process: Apply Symbology From Layer
        arcpy.ApplySymbologyFromLayer_management(LYR,
                                                 SYMBOLOGY)
        #GETTING NAME FOR FILES

        BASEFILE = r
        FILENAME = os.path.splitext(BASEFILE)[0]
        arcpy.AddMessage(FILENAME)

        # Process: JPG
        # - Process: Get map document and frames
        # - Process: Add date
        ELEMENTS = arcpy.mapping.ListLayoutElements(MXD)
        BUSCAR = [ELEM for ELEM in ELEMENTS if ELEM.type == "TEXT_ELEMENT" and ELEM.text.startswith("fecha_mapa")][0]
        DECADA = [ELEM for ELEM in ELEMENTS if ELEM.type == "TEXT_ELEMENT" and ELEM.text.startswith("decada_mapa")][0]
        BUSCAR.text = "{} de {}".format(MESES[MES], ANIO)
        
        NOMBRE_DECADA = (FILENAME[8])
        if NOMBRE_DECADA == '1':
            DECADA.text = "Primera d\xe9cada (1 al 10)"
        elif NOMBRE_DECADA == '2':
            DECADA.text = "Segunda d\xe9cada (11 al 20)"
        elif NOMBRE_DECADA == '3':
            DECADA.text = "Tercera d\xe9cada (21 al {})".format(calendar.monthrange(int(ANIO), int(MES))[1])
        else:
            DECADA.text = "Mensual"

        #DECADA.text = TEXTO_DECADA_JPG[IDH] -----OJO ------------PENDIENTE

        # - Process: Make products
        arcpy.mapping.AddLayer(DF0, LYR, "BOTTOM")
        if NUMSUBRED != 0:
            arcpy.mapping.AddLayer(DF0, AMERICA_PAISES_LYR, "BOTTOM")
        arcpy.mapping.AddLayer(DF0, CROKISGEO_LYR, "BOTTOM")

        if NUMSUBRED == 0:
            DF2 = arcpy.mapping.ListDataFrames(MXD)[2]
            DF3 = arcpy.mapping.ListDataFrames(MXD)[3]
            for dataFrame in [DF2, DF3]:
                arcpy.mapping.AddLayer(dataFrame, LYR, "BOTTOM")
                refLayer = None
                moveLayer = None
                for lyrtemp in arcpy.mapping.ListLayers(MXD, "", dataFrame):
                    arcpy.AddMessage(lyrtemp.name.lower())
                    if lyrtemp.name.lower() == "departamento":
                        refLayer = lyrtemp
                    if lyrtemp.name.lower() == "_{}.tif".format(FILENAME.lower()):
                        moveLayer = lyrtemp
                if refLayer and moveLayer:
                    arcpy.mapping.MoveLayer(dataFrame, refLayer, moveLayer, "BEFORE")

        elif NUMSUBRED != 13:
            ZONAPRODUCTORA = [ELEM for ELEM in ELEMENTS if ELEM.type == "TEXT_ELEMENT" and ELEM.text.startswith("zona_mapa")][0]
            ZONAPRODUCTORA.text = "Zona productora {}\n{}".format(NUMSUBRED, NOMBRE_SUBRED[SUBRED])
            LYRZONA = arcpy.mapping.ListLayers(MXD, "Zona_Productora", DF0)[0]
            LYRZONA.definitionQuery = "No_Zona = '{}'".format(NUMSUBRED)
            DF0.extent = LYRZONA.getExtent(True)
            arcpy.RefreshActiveView()
        
        refLayer = None
        moveLayer = None
        for lyrtemp in arcpy.mapping.ListLayers(MXD, "", DF0):
            arcpy.AddMessage(lyrtemp.name.lower())
            if lyrtemp.name.lower() == "modelo_sombras":
                refLayer = lyrtemp
            if lyrtemp.name.lower() == "_{}.tif".format(FILENAME.lower()):
                moveLayer = lyrtemp
        if refLayer and moveLayer:
            arcpy.mapping.MoveLayer(DF0, refLayer, moveLayer, "BEFORE")        
        arcpy.mapping.ExportToJPEG(MXD, os.path.join(PATH, "{}.jpg".format(FILENAME)), "", 2550, 3300, 150)
        
        del MXD

        PRODUCTS.append("{}/{}.jpg".format(LINK, FILENAME))
        arcpy.AddMessage("contruido el jpg {}".format(FILENAME))

        # Process: GIF
        # - Process: Get map document and frames
        MXD = arcpy.mapping.MapDocument(PLANTILLA_GIF)
        DF0 = arcpy.mapping.ListDataFrames(MXD)[0]
        
        # - Process: Add date
        ELEMENTS = arcpy.mapping.ListLayoutElements(MXD)
        BUSCAR = [ELEM for ELEM in ELEMENTS if ELEM.type == "TEXT_ELEMENT" and ELEM.text.startswith("fecha_mapa")][0]
        DECADA = [ELEM for ELEM in ELEMENTS if ELEM.type == "TEXT_ELEMENT" and ELEM.text.startswith("decada_mapa")][0]
        BUSCAR.text = "{} de {}".format(MESES[MES], ANIO)

        if NOMBRE_DECADA == '1':
            DECADA.text = "Primera d\xe9cada"
        elif NOMBRE_DECADA == '2':
            DECADA.text = "Segunda d\xe9cada"
        elif NOMBRE_DECADA == '3':
            DECADA.text = "Tercera d\xe9cada"
        else:
            DECADA.text = "Mensual"
        #DECADA.text = TEXTO_DECADA_GIF[IDH] -----OJO ------------PENDIENTE

        # - Process: Make products
        arcpy.mapping.AddLayer(DF0, LYR, "BOTTOM")
        if NUMSUBRED != 0:
            arcpy.mapping.AddLayer(DF0, AMERICA_PAISES_LYR, "BOTTOM")
        arcpy.mapping.AddLayer(DF0, CROKISGEO_LYR, "BOTTOM")
        if NUMSUBRED == 0:
            DF2 = arcpy.mapping.ListDataFrames(MXD)[1]
            DF3 = arcpy.mapping.ListDataFrames(MXD)[2]
            for dataFrame in [DF2, DF3]:
                refLayer = None
                moveLayer = None
                arcpy.mapping.AddLayer(dataFrame, LYR, "BOTTOM")
                for lyrtemp in arcpy.mapping.ListLayers(MXD, "", dataFrame):
                    if lyrtemp.name.lower() == "departamento":
                        refLayer = lyrtemp
                    if lyrtemp.name.lower() == "_{}.tif".format(FILENAME.lower()):
                        moveLayer = lyrtemp
                if refLayer and moveLayer:
                    arcpy.mapping.MoveLayer(dataFrame, refLayer, moveLayer, "BEFORE")
        elif NUMSUBRED != 13:
            ZONAPRODUCTORA = [ELEM for ELEM in ELEMENTS if ELEM.type == "TEXT_ELEMENT" and ELEM.text.startswith("zona_mapa")][0]
            ZONAPRODUCTORA.text = "Zona productora {}\n".format(NUMSUBRED)
            LYRZONA = arcpy.mapping.ListLayers(MXD, "Zona_Productora", DF0)[0]
            LYRZONA.definitionQuery = "No_Zona = '{}'".format(NUMSUBRED)
            DF0.extent = LYRZONA.getExtent(True)
            arcpy.RefreshActiveView()
        arcpy.mapping.ExportToGIF(MXD, os.path.join(PATH, "{}.gif".format(FILENAME)), "", 382, 495, 45)
        del MXD

        PRODUCTS.append("{}/{}.gif".format(LINK, FILENAME))

    arcpy.SetParameterAsText(4, json.dumps(PRODUCTS))
    arcpy.ClearWorkspaceCache_management(BASESDE)
    
    
    arcpy.Delete_management(RESULT_EXTRACT)
    arcpy.Delete_management(RECLASS_EXTRACT)
    arcpy.Delete_management(ESTACIONES)
    arcpy.Delete_management(ESTACIONES_VIEW)
    arcpy.Delete_management(ESTACIONES_LAYER)
    arcpy.Delete_management(ARCHIVO_VIEW)
    arcpy.Delete_management(RESULT_IDW)

    del ESTACIONESSDE, ESTACIONES
    del BASE, BASESDE, PATHPUBLIC, PATHGET, ENVIRO
    del COLOMBIA_CROQUIS, CROKISGEO_LYR, SYMBOLOGY, SWITCH, ESTACIONES_VIEW, ARCHIVO_VIEW, ESTACIONES_LAYER, RESULT_IDW, RESULT_EXTRACT, RECLASS_EXTRACT
    
except IOError:
    arcpy.AddError("No se encontró el recurso solicitado.")
except LicenseError:
    arcpy.AddError("La licencia de análisis espacial no está disponible.")
except ParamError:
    arcpy.AddError("No se encontraron los recursos solicitados.")
except arcpy.ExecuteError:
    MSGS = arcpy.GetMessages(2)
    arcpy.AddError(MSGS)
finally:
    # Check in the Spatial Analysis
    arcpy.CheckInExtension("Spatial")



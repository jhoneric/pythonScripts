# Esri start of added imports
import sys, os, arcpy
import time
# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = u'/u01/Data/Servicios/Conexiones/GDBIDEAM.sde'#Ruta archivo de conexión de la base de Pruebas/Oficial
#g_ESRI_variable_1 = os.path.join(arcpy.env.packageWorkspace,u'/u01/Data/Servicios/Conexiones/GDBIDEAM.sde')#Ruta archivo de conexión de la base de Pruebas/Oficial
#g_ESRI_variable_1 = os.path.join(arcpy.env.packageWorkspace,r"\\172.16.50.8\data\Servicios\Conexiones\\GDBIDEAM.sde")#Ruta archivo de conexión de la base de Pruebas/Oficial
#g_ESRI_variable_2 = os.path.join(arcpy.env.packageWorkspace,u'/u01/Data/Servicios/Conexiones/172.16.50.34 (GDBIDEAM).sde')#Ruta archivo de conexión de la base Operativa (NO MODIFICAR)
g_ESRI_variable_2 = u'/u01/Data/Servicios/Conexiones/172.16.50.4 (GDBIDEAM).sde'#Ruta archivo de conexión de la base Operativa (NO MODIFICAR)
#g_ESRI_variable_2 = os.path.join(arcpy.env.packageWorkspace,r'\\172.16.50.8\data\Servicios\Conexiones\\172.16.50.4 (GDBIDEAM).sde')#Ruta archivo de conexión de la base Operativa (NO MODIFICAR)
#g_ESRI_variable_3 = u'objectid objectid VISIBLE NONE;idestacion idestacion VISIBLE NONE;nombre nombre VISIBLE NONE;idcategoria idcategoria VISIBLE NONE;idtecnologiatm idtecnologiatm VISIBLE NONE;idtipotransmisiontm idtipotransmisiontm VISIBLE NONE;idestadoestaciontm idestadoestaciontm VISIBLE NONE;fechainstalacion fechainstalacion VISIBLE NONE;altitud altitud VISIBLE NONE;latitud latitud VISIBLE NONE;longitud longitud VISIBLE NONE;iddepartamento iddepartamento VISIBLE NONE;idmunicipio idmunicipio VISIBLE NONE;idareaoperativa idareaoperativa VISIBLE NONE;idareahidrografica idareahidrografica VISIBLE NONE;idzonahidrografica idzonahidrografica VISIBLE NONE;codigowmo codigowmo VISIBLE NONE;codigointerno codigointerno VISIBLE NONE;codigoiata codigoiata VISIBLE NONE;codigonesdsdis codigonesdsdis VISIBLE NONE;codigooaci codigooaci VISIBLE NONE;identidad identidad VISIBLE NONE;usuario usuario VISIBLE NONE;fechaultimamodificacion fechaultimamodificacion VISIBLE NONE;codigoorfeo codigoorfeo VISIBLE NONE;observacion observacion VISIBLE NONE;idcorriente idcorriente VISIBLE NONE;fechasuspension fechasuspension VISIBLE NONE;idaquarius idaquarius VISIBLE NONE;idgis idgis VISIBLE NONE;idsubzonahidrografica idsubzonahidrografica VISIBLE NONE;prop_cod prop_cod VISIBLE NONE;prop_sector prop_sector VISIBLE NONE;familia familia VISIBLE NONE;clase clase VISIBLE NONE;temp temp VISIBLE NONE;prop_nom prop_nom VISIBLE NONE;prop_tipo prop_tipo VISIBLE NONE;eliminado eliminado VISIBLE NONE;shape shape VISIBLE NONE;Categoria Categoria VISIBLE NONE;Mpio Mpio VISIBLE NONE;Depto Depto VISIBLE NONE;Tecnologia Tecnologia VISIBLE NONE;EstEstacion EstEstacion VISIBLE NONE;RuleID RuleID VISIBLE NONE'
g_ESRI_variable_4 = u'in_memory\\featureTemp'
g_ESRI_variable_5 = u'idcategoria'
g_ESRI_variable_6 = u'id_categoria'
g_ESRI_variable_7 = u'Categoria'
g_ESRI_variable_8 = u'!gdbideam.gdbideam.DOM_Categoria.nom_categoria!'
g_ESRI_variable_9 = u'idestadoestaciontm'
g_ESRI_variable_10 = u'ID_EstadoEstacion'
g_ESRI_variable_11 = u'EstEstacion'
g_ESRI_variable_12 = u'!gdbideam.gdbideam.DOM_EstadoEstacion.nom_estadoestacion!'
g_ESRI_variable_13 = u'idmunicipio'
g_ESRI_variable_14 = u'id_municpio'
g_ESRI_variable_15 = u'Mpio'
g_ESRI_variable_16 = u'!gdbideam.gdbideam.DOM_Municipios.nom_municipio!'
g_ESRI_variable_17 = u'iddepartamento'
g_ESRI_variable_18 = u'id_depto'
g_ESRI_variable_19 = u'Depto'
g_ESRI_variable_20 = u'!gdbideam.gdbideam.DOM_Depto.nom_depto!'
g_ESRI_variable_21 = u'idtecnologiatm'
g_ESRI_variable_22 = u'id_tecestacion'
g_ESRI_variable_23 = u'Tecnologia'
g_ESRI_variable_24 = u'!gdbideam.gdbideam.DOM_TecEstacion.nom_tecestacion!'
g_ESRI_variable_25 = u'nomruleid'
g_ESRI_variable_26 = u'RuleID'
g_ESRI_variable_27 = u'!gdbideam.gdbideam.DOM_RuleID.idruleid!'
# Esri end of added variables

# -*- #################
# -*- ###############
# -*- encoding: utf-8 -*-
# encoding: latin1

import arcpy
#import sys, os

arcpy.env.overwriteOutput = False

conSDEOfi = ''
conSDEOpe = ''
conGDBTemp = ''
estacionesOpe = ''
estacionesTmp = ''
estacionesOfi = ''
tablaCategoria = ''
tablaEstEstacion = ''
tablaMunicipio = ''
tablaDepartamento = ''
tablaTecnologia = ''
tablaRuleID = ''
DiccFeature = {}

#Función que inicializa todas las variables
def InicializarVariables():
	#Definiendo variables globales del script
    global conSDEOfi
    global conSDEOpe
    global conGDBTemp
    global DiccFeature
    global estacionesOpe
    global estacionesTmp
    global estacionesOfi
    global tablaCategoria
    global tablaEstEstacion
    global tablaMunicipio
    global tablaDepartamento
    global tablaTecnologia
    global tablaRuleID

    conSDEOfi = g_ESRI_variable_1 #Define la ruta de la conexión sde base oficial
    conSDEOpe = g_ESRI_variable_2 #Define la ruta de la conexión sde base operativa
    conGDBTemp = arcpy.env.scratchGDB #Define la ruta de la base temporal que apunta a la base scratch del arcgis server
	
	#Diccionario Python con los nombres y rutas relativas de Features requeridos en el script.
	#Si se cambia el nombre de la capa definitiva de actualiación de estaciones, se debe modificar la parte "GDBSGDHM.SGDHM//GDBSGDHM.CatalogoNalEstacionesV111_2018", por la nueva ruta, tener en cuenta incluir desde el Dataset
    DiccFeature={"EstacionesOpe":"gdbideam.gdbideam.CNE//gdbideam.gdbideam.Estaciones",
    "EstacionesOfi":"GDBIDEAM.Datos_Referencia//GDBIDEAM.CatalogoNalEstaciones",
    "EstacionesOpeTemp":"Estaciones",
    "TablaCategoria":"gdbideam.gdbideam.DOM_Categoria",
    "TablaMpio":"gdbideam.gdbideam.DOM_Municipios",
    "TablaDepto":"gdbideam.gdbideam.DOM_Depto",
    "TablaTecnologia":"gdbideam.gdbideam.DOM_TecEstacion",
    "TablaEstEstacion":"gdbideam.gdbideam.DOM_EstadoEstacion",
    "TablaRuleID":"gdbideam.gdbideam.DOM_RuleID"}
    
    
    estacionesOpe = os.path.join(conSDEOpe,DiccFeature["EstacionesOpe"])#Ruta definitiva feature estaciones en la base operativa
    estacionesTmp = os.path.join(conGDBTemp,DiccFeature["EstacionesOpeTemp"])#Ruta defitiva feature estaciones en la base temporal
    estacionesOfi = os.path.join(conSDEOfi,DiccFeature["EstacionesOfi"])#Ruta definitiva feature estaciones en la base oficial
    tablaCategoria = os.path.join(conSDEOpe,DiccFeature["TablaCategoria"])#Ruta definitiva tabla Categoria
    tablaEstEstacion = os.path.join(conSDEOpe,DiccFeature["TablaEstEstacion"])#Ruta definitiva tabla Estado Estación
    tablaMunicipio = os.path.join(conSDEOpe,DiccFeature["TablaMpio"])#Ruta definitiva tabla Municipio
    tablaDepartamento = os.path.join(conSDEOpe,DiccFeature["TablaDepto"])#Ruta definitia tabla Departamento
    tablaTecnologia = os.path.join(conSDEOpe,DiccFeature["TablaTecnologia"])#Ruta definitiva tabla Tecnologia
    tablaRuleID = os.path.join(conSDEOpe,DiccFeature["TablaRuleID"])#Ruta definitiva Tabla RuleID
    
    #conFeatureAppend="NOMBRE 'NOMBRE' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",nombre,-1,-1;CATEGORIA 'CATEGORIA' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Categoria,-1,-1;LONGITUD 'LONGITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",longitud,-1,-1;LATITUD 'LATITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",latitud,-1,-1;ALTITUD 'ALTITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",altitud,-1,-1;DEPARTAMEN 'DEPARTAMEN' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Depto,-1,-1;MUNICIPIO 'MUNICIPIO' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Mpio,-1,-1;ESTADO_EST 'ESTADO_EST' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",EstEstacion,-1,-1;"+u"TECNOLOG\xcd 'TECNOLOG\xcd' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Tecnologia,-1,-1;FECHA_INST 'FECHA_INST' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechainstalacion,-1,-1;FECHA_SUSP 'FECHA_SUSP' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechasuspension,-1,-1;RULEID 'RULEID' true true true 4 Long 0 0 ,First,#,"+estacionesTmp+",RuleID,-1,-1;OVERRIDE 'OVERRIDE' true true true 0 Blob 0 0 ,First,#"
    
    arcpy.AddMessage("Hecho Inicializar Variables")

#Función que realiza la creación de atributos adicionales al feature temporal copia de la capa estaciones de la base operativa
def ConfigurandoFeature():
    t1 = time.time()
    arcpy.CopyFeatures_management(estacionesOpe,estacionesTmp)
    t2 = time.time()
    duration2 = t2 - t1
    arcpy.AddMessage("copy of estaciones layer done, processing time : {} seconds".format(duration2))
    
    arcpy.AddField_management(estacionesTmp,"Categoria","TEXT",None,None,150,None,None,None,None)#Crea atributo categoria
    arcpy.AddField_management(estacionesTmp,"Mpio","TEXT",None,None,150,None,None,None,None)#Crea atributo Municipio
    arcpy.AddField_management(estacionesTmp,"Depto","TEXT",None,None,150,None,None,None,None)#Crea atributo Departamento
    arcpy.AddField_management(estacionesTmp,"Tecnologia","TEXT",None,None,150,None,None,None,None)#Crea atributo Tecnologia
    arcpy.AddField_management(estacionesTmp,"EstEstacion","TEXT",None,None,150,None,None,None,None)#Crea atributo estado estación
    arcpy.AddField_management(estacionesTmp,"RuleID","FLOAT",None,None,None,None,None,None,None)#Crea atributo RuleID

    t3 = time.time()
    duration1 = t3 -t1
    arcpy.AddMessage("created fields to the copy, time of processing: {} seconds".format(duration1))

#Función que realiza el llenado de los atributos creados en la función ConfigurandoFeature
def CalculoAtributos():
    t5 = time.time()
    #conFeature=g_ESRI_variable_3
    featureTemp=g_ESRI_variable_4
    #arcpy.MakeFeatureLayer_management(estacionesTmp,featureTemp,"","",conFeature)
    arcpy.MakeFeatureLayer_management(estacionesTmp,featureTemp,"","","")
    arcpy.AddMessage("creando layer temporal")
    #Calcula Categoria
    
    arcpy.AddJoin_management(featureTemp,g_ESRI_variable_5,tablaCategoria,g_ESRI_variable_6,"KEEP_ALL")
    arcpy.CalculateField_management(featureTemp,g_ESRI_variable_7,g_ESRI_variable_8, "PYTHON_9.3", "")
    arcpy.AddMessage("campo Categoria calculada")
    #Calcula Estado Estacion
    arcpy.AddJoin_management(featureTemp,g_ESRI_variable_9,tablaEstEstacion,g_ESRI_variable_10,"KEEP_ALL")
    arcpy.CalculateField_management(featureTemp,g_ESRI_variable_11,g_ESRI_variable_12, "PYTHON_9.3", "")
    arcpy.AddMessage("campo EStado estacion calculada")
    #Calculo Municipio
    arcpy.AddJoin_management(featureTemp,g_ESRI_variable_13,tablaMunicipio,g_ESRI_variable_14,"KEEP_ALL")
    arcpy.CalculateField_management(featureTemp,g_ESRI_variable_15,g_ESRI_variable_16, "PYTHON_9.3", "")
    arcpy.AddMessage("campo municipio calculada")
    #Calculo Departamento
    arcpy.AddJoin_management(featureTemp,g_ESRI_variable_17,tablaDepartamento,g_ESRI_variable_18,"KEEP_ALL")
    arcpy.CalculateField_management(featureTemp,g_ESRI_variable_19,g_ESRI_variable_20, "PYTHON_9.3", "")
    arcpy.AddMessage("campo depto calculada")
    #Calculo Tecnologia
    arcpy.AddJoin_management(featureTemp,g_ESRI_variable_21,tablaTecnologia,g_ESRI_variable_22,"KEEP_ALL")
    arcpy.CalculateField_management(featureTemp,g_ESRI_variable_23,g_ESRI_variable_24, "PYTHON_9.3", "")
    arcpy.AddMessage("campo tecnologia calculada")
    #Calculo RuleID
    arcpy.AddJoin_management(featureTemp,g_ESRI_variable_7,tablaRuleID,g_ESRI_variable_25,"KEEP_ALL")
    arcpy.CalculateField_management(featureTemp,g_ESRI_variable_26,g_ESRI_variable_27, "PYTHON_9.3", "")
    arcpy.AddMessage("campo ruleID calculada")
    estacionesFgdb = {}
    arcpy.AddMessage("hecho calculo de atributos")
    t6= time.time()
    duration3 = t6 -t5
    arcpy.AddMessage("total time attribute calculation: {} seconds".format(duration3))

#Función que realiza el borrado y llenado de la capa Estaciones en la base Pruebas/Oficial
def CargaFerature():
    t9 = time.time()
    featureDelete=os.path.join(conSDEOfi,DiccFeature["EstacionesOfi"])
    #conFeatureAppend="NOMBRE \"NOMBRE\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",nombre,-1,-1;CATEGORIA \"CATEGORIA\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Categoria,-1,-1;LONGITUD \"LONGITUD\" true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",longitud,-1,-1;LATITUD \"LATITUD\" true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",latitud,-1,-1;ALTITUD \"ALTITUD\" true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",altitud,-1,-1;DEPARTAMEN \"DEPARTAMEN\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Depto,-1,-1;MUNICIPIO \"MUNICIPIO\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Mpio,-1,-1;ESTADO_EST \"ESTADO_EST\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",EstEstacion,-1,-1;"+u"TECNOLOG\xc3\x8d \"TECNOLOG\xc3\x8d\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Tecnologia,-1,-1;FECHA_INST \"FECHA_INST\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechainstalacion,-1,-1;FECHA_SUSP \"FECHA_SUSP\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechasuspension,-1,-1;RULEID \"RULEID\" true true true 4 Long 0 0 ,First,#,"+estacionesTmp+",RuleID,-1,-1;OVERRIDE \"OVERRIDE\" true true true 0 Blob 0 0 ,First,#"
    #conFeatureAppend="NOMBRE 'NOMBRE' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",nombre,-1,-1;CATEGORIA 'CATEGORIA' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Categoria,-1,-1;LONGITUD 'LONGITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",longitud,-1,-1;LATITUD 'LATITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",latitud,-1,-1;ALTITUD 'ALTITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",altitud,-1,-1;DEPARTAMEN 'DEPARTAMEN' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Depto,-1,-1;MUNICIPIO 'MUNICIPIO' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Mpio,-1,-1;ESTADO_EST 'ESTADO_EST' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",EstEstacion,-1,-1;TECNOLOG\xc3\x8d 'TECNOLOG\xc3\x8d' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Tecnologia,-1,-1;FECHA_INST 'FECHA_INST' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechainstalacion,-1,-1;FECHA_SUSP 'FECHA_SUSP' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechasuspension,-1,-1;RULEID 'RULEID' true true true 4 Long 0 0 ,First,#,"+estacionesTmp+",RuleID,-1,-1;OVERRIDE 'OVERRIDE' true true true 0 Blob 0 0 ,First,#"
    #conFeatureAppend="NOMBRE \"NOMBRE\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",nombre,-1,-1;CATEGORIA \"CATEGORIA\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Categoria,-1,-1;LONGITUD \"LONGITUD\" true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",longitud,-1,-1;LATITUD \"LATITUD\" true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",latitud,-1,-1;ALTITUD \"ALTITUD\" true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",altitud,-1,-1;DEPARTAMEN \"DEPARTAMEN\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Depto,-1,-1;MUNICIPIO \"MUNICIPIO\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Mpio,-1,-1;ESTADO_EST \"ESTADO_EST\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",EstEstacion,-1,-1;TECNOLOG\xc3\x8d \"TECNOLOG\xc3\x8d\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Tecnologia,-1,-1;FECHA_INST \"FECHA_INST\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechainstalacion,-1,-1;FECHA_SUSP \"FECHA_SUSP\" true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechasuspension,-1,-1;RULEID \"RULEID\" true true true 4 Long 0 0 ,First,#,"+estacionesTmp+",RuleID,-1,-1;OVERRIDE \"OVERRIDE\" true true true 0 Blob 0 0 ,First,#"
    conFeatureAppend="NOMBRE 'NOMBRE' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",nombre,-1,-1;CATEGORIA 'CATEGORIA' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Categoria,-1,-1;LONGITUD 'LONGITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",longitud,-1,-1;LATITUD 'LATITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",latitud,-1,-1;ALTITUD 'ALTITUD' true true false 8 Double 0 0 ,First,#,"+estacionesTmp+",altitud,-1,-1;DEPARTAMEN 'DEPARTAMEN' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Depto,-1,-1;MUNICIPIO 'MUNICIPIO' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Mpio,-1,-1;ESTADO_EST 'ESTADO_EST' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",EstEstacion,-1,-1;"+u"TECNOLOG\xcd 'TECNOLOG\xcd' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",Tecnologia,-1,-1;FECHA_INST 'FECHA_INST' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechainstalacion,-1,-1;FECHA_SUSP 'FECHA_SUSP' true true false 254 Text 0 0 ,First,#,"+estacionesTmp+",fechasuspension,-1,-1;RULEID 'RULEID' true true true 4 Long 0 0 ,First,#,"+estacionesTmp+",RuleID,-1,-1;OVERRIDE 'OVERRIDE' true true true 0 Blob 0 0 ,First,#"
    arcpy.DeleteFeatures_management(featureDelete)
    arcpy.Append_management(estacionesTmp,featureDelete,"NO_TEST",conFeatureAppend,"")
    arcpy.AddMessage("Hecho carga de la tabla oficial")
    t10 = time.time()
    duration6 = t10-t9
    arcpy.AddMessage("total time feature charge: {} seconds".format(duration6))

#Función que realiza el llenado del atributo Código, debido a que este maneja tilde, fue necesario una función especial exclusivamente para este atributo
def actualizarCodigoGdbEnterprise(pCapaFileGdb,pCapaGdbEnterprise):
    t11 = time.time()
    estacionesFgdb = {}
    with arcpy.da.SearchCursor(pCapaFileGdb,["nombre","idestacion"]) as cursor:
        for row in cursor:
            estacionesFgdb[row[0]]= row[1]

    with arcpy.da.UpdateCursor(pCapaGdbEnterprise,["C\xc3\x93DIGO","NOMBRE"]) as cursor:
        for row in cursor:
            if estacionesFgdb.has_key(row[1]):
                row[0] = estacionesFgdb[row[1]]
                cursor.updateRow(row)
    arcpy.AddMessage("Hecho actualizacion capa")
    t12 = time.time()
    duration7 = t12-t11
    arcpy.AddMessage("total time feature update in Oficial SDE: {} seconds".format(duration7))

#Función encargada de realizar la impresión de mensajes de advertencia
def PrintMessage(message):
    arcpy.AddMessage(message)
    return

#Función principal del script
def main():
    ConfigurandoFeature()#Ejecuta la función ConfigurandoFeature
    CalculoAtributos()#Ejecuta la función CalculoAtributos
    CargaFerature()#Ejecuta la función CargaFerature
    actualizarCodigoGdbEnterprise(estacionesTmp,estacionesOfi)#Ejecuta la función actualizarCodigoGdbEnterprise y se lleva las variables correspondientes a la ubicación de la estacion en base temporal y estación en base oficial

    pass

if __name__ == '__main__':
    t0 = time.time()
    InicializarVariables()#Ejecuta la función InicializarVariables
    validarFeature=os.path.join(conGDBTemp,DiccFeature["EstacionesOpeTemp"])#Variable que define la ruta de la capa estaciones en la base temporal del sistema (scratch)
    arcpy.AddMessage(validarFeature)
    validador = arcpy.Exists(validarFeature)#Valida si existe el feature Estaciones en la gdb temporal del sistema (scratch)
    
    if validador == True: #Si existe el feature estaciones en la base temporal, ejecuta el codigo...
        arcpy.Delete_management(validarFeature)
        arcpy.AddMessage("Se ha borrado una version anterior de la capa temporal Estaciones")
        main()
    else:#Si no existe el feature estaciones en la base temporal, ejecuta todas las funciones en el orden de la función principal

        main()


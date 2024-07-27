import sys
import ac
import acsys
#import os
import time
#from pathlib import Path
import datetime as dt
from datetime import date
from datetime import datetime
velocidad_modulo = 0.0
#l_lapcount={0, 0, 0}
#lapcount={0, 0, 0}



#Datos configuración (añadir * si no hay dato),
#Nombre y apellidos conductor,Valero Pascual Gallego
##Edad conductor,55
#Carnet conductor,B1
#Puntos conductor,15

#ruta = Path(r'C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\telemetria_datos_configuracion')
#fichero_configuracion=os.path.join(ruta, 'configuración_assetto.csv')
#Fecha y hora actual
fichero_conf="C:\\Program Files (x86)\\Steam\\steamapps\\common\\assettocorsa\\telemetria_datos_configuracion\\Datos_prueba.csv"
with open (fichero_conf,"r") as configuracion: 
	configuracion.readline()#se lee primera linea
	campo = []
	valor = []
	for linea in configuracion:
		palabras = linea.split(",")
		campo.append(palabras[0].split("\n")[0])
		valor.append(palabras[1].split("\n")[0])
	configuracion.close()

#CABECERA DEL FICHERO DE RESULTADOS

#fichero_datos=os.path.join(ruta, valor[4])
#Fecha y hora actual
now = datetime.now()
circuito=ac.getTrackName(0)
fichero_destino_datos="C:\\Program Files (x86)\\Steam\\steamapps\\common\\assettocorsa\\telemetria_datos_configuracion\\"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(now.hour)+"-"+str(now.minute)+"-"+str(now.second)+"-"+circuito+"-"+valor[0]+".csv"
f = open (fichero_destino_datos,"w") 

auto=ac.getCarName(0)
momento_gravacion=str(datetime.now())
f.write("momento gravacion prueba;"+momento_gravacion+"\n")
f.write("automovil;"+auto+"\n")


f.write("Nombre circuito;"+circuito+"\n")

#conductor=ac.getDriverName(0)
#f.write("Nombre conductor=,"+conductor+"\n")
#f.write("Momento,X(m),Y(m),Z(m),Vx(m/s),Vy(m/s),Vz(m/s),V_modulo(m/s)\n")

# Lectora del fichero de configuración
nombre=valor[0]
f.write("Nombre conductor=;"+nombre+"\n")
f.write("Momento (s);")
f.write("X(m);Y(m);Z(m);")
f.write("Vx(m/s);Vy(m/s);Vz(m/s);")
f.write("V_modulo(km/h);")
f.write("Presion acelerador (0-1);")
f.write("Presion freno (0-1);")
f.write("Presion embrague (0-1);")
f.write("Marcha;")
f.write("RPM motor;")
f.write("Posicion norm pista;")
f.write("giro volante (-360º, 360º);")
f.write("X_Num_Gs_vehiculo;Y_Num_Gs_vehiculo;Z_Num_Gs_vehiculo;")
f.write("X_velocidad_angular_coche_CG;Y_velocidad_angular_coche_CG;Z_velocidad_angular_coche_CG;")
f.write("X_normal_rueda_RR;Y_normal_rueda_RR;Z_normal_rueda_RR;")
f.write("X_normal_rueda_RL;Y_normal_rueda_RL;Z_normal_rueda_RL;")
f.write("X_normal_rueda_FR;Y_normal_rueda_FR;Z_normal_rueda_FR;")
f.write("X_normal_rueda_FL;Y_normal_rueda_FL;Z_normal_rueda_FL;")
f.write("X_Punto_contacto_rueda_RR;Y_Punto_contacto_rueda_RR;Z_Punto_contacto_rueda_RR;")
f.write("X_Punto_contacto_rueda_RL;Y_Punto_contacto_rueda_RL;Z_Punto_contacto_rueda_RL;")
f.write("X_Punto_contacto_rueda_FR;Y_Punto_contacto_rueda_FR;Z_Punto_contacto_rueda_FR;")
f.write("X_Punto_contacto_rueda_FL;Y_Punto_contacto_rueda_FL;Z_Punto_contacto_rueda_FL;")
f.write("FX_Vector_ruedas_RR;FY_Vector_ruedas_RR;")
f.write("FX_Vector_ruedas_RL;FY_Vector_ruedas_RL;")
f.write("FX_Vector_ruedas_FR;FY_Vector_ruedas_FR;")
f.write("FX_Vector_ruedas_FR;FY_Vector_ruedas_FR")
f.write("\n")

def acMain(ac_version):
	global f
	global informacion
	
	
	ventana_informacion = ac.newApp("Telemetria") # el archivo tiene el nombre del app que tiene el nombre tamibén de la carppeta dentro de python de ...
	ac.setSize(ventana_informacion, 400, 100) # ventana donde ver telemetria
	
	informacion = ac.addLabel(ventana_informacion, "Informacion prueba: 0");
	ac.setPosition(informacion, 1, 25)
	#informacion = ac.addLabel(ventana_informacion, "Informacion prueba:");
	ac.setText(informacion, "Informacion prueba: {}".format("\nNombre del condiztor: "+nombre+"\n Circuito: "+circuito+"\n Momento de la gravación: "+momento_gravacion))
	
	return "Telemetria"

def acUpdate(deltaT):
	global f

	coor = [0.0,0.0,0.0]
	
	velocidad=[0.0,0.0,0.0]
	
	velocidad_modulo=[0.0,0.0,0.0]
	
	presion_pedal_acelerador=0.0
		
	presion_pedal_Brake=0.0
	
	presion_pedal_Clutch=0.0
	
	Marcha=0.0
	
	RPM_motor=0.0
	
	Posicion_coche_pista_normalizada=0.0
	
	Direccion_ruedas_delanteras=0.0
	
	Num_Gs_vehiculo=[0.0,0.0,0.0]
	

	
	

	#global l_lapcount, lapcount
	#time.sleep(int(valor[3])/1000)
	
	momento = str(time.time())
	f.write(momento+";")
	
	coor = ac.getCarState(0, acsys.CS.WorldPosition)
	coor_x=str(round(coor[0],4))
	coor_y=str(round(coor[1],4))
	coor_z=str(round(coor[2],4))
	f.write(coor_x+";"+coor_y+";"+coor_z+";")
			
	velocidad=ac.getCarState(0, acsys.CS.Velocity)
	velocidad_x=str(round(velocidad[0],4))
	velocidad_y=str(round(velocidad[1],4))
	velocidad_z=str(round(velocidad[2],4))	
	f.write(velocidad_x+";"+velocidad_y+";"+velocidad_z+";")	
	
	velocidad_modulo=ac.getCarState(0, acsys.CS.SpeedTotal)
	velocidadkmh=str(round(velocidad_modulo[0],4))
	f.write(velocidadkmh+";")
		
	presion_pedal_acelerador=ac.getCarState(0, acsys.CS.Gas)
	gas_presion_0_a_1=str(round(presion_pedal_acelerador,4))	
	f.write(gas_presion_0_a_1+";")
		
	presion_pedal_Brake=ac.getCarState(0, acsys.CS.Brake)
	brake_presion_0_a_1=str(round(presion_pedal_Brake,4))
	f.write(brake_presion_0_a_1+";")
		
	presion_pedal_Clutch=ac.getCarState(0, acsys.CS.Clutch)
	Clutch_presion_0_a_1=str(round(presion_pedal_Clutch,4))
	f.write(Clutch_presion_0_a_1+";")
		
	Marcha=ac.getCarState(0, acsys.CS.Gear)
	Marcha_str=str(round(Marcha,1))
	f.write(Marcha_str+";")
			
	RPM_motor=ac.getCarState(0, acsys.CS.RPM)
	RPM_motor_str=str(round(RPM_motor,4))
	f.write(RPM_motor_str+";")
		
	Posicion_coche_pista_normalizada=ac.getCarState(0, acsys.CS.NormalizedSplinePosition)
	Posicion_coche_pista_normalizada_str=str(round(Posicion_coche_pista_normalizada,4))
	f.write(Posicion_coche_pista_normalizada_str+";")
			
	Direccion_ruedas_delanteras=ac.getCarState(0, acsys.CS.Steer)
	Direccion_ruedas_delanteras_str=str(round(Direccion_ruedas_delanteras,4))
	f.write(Direccion_ruedas_delanteras_str+";")	
	
	Num_Gs_vehiculo=ac.getCarState(0, acsys.CS.AccG)
	X_Num_Gs_vehiculo_str=str(round(Num_Gs_vehiculo[0],4))
	Y_Num_Gs_vehiculo_str=str(round(Num_Gs_vehiculo[1],4))
	Z_Num_Gs_vehiculo_str=str(round(Num_Gs_vehiculo[2],4))	
	f.write(X_Num_Gs_vehiculo_str+";"+Y_Num_Gs_vehiculo_str+";"+Z_Num_Gs_vehiculo_str+";")
	
	Velocidad_angular_coche_CG=[0.0,0.0,0.0]		
	Velocidad_angular_coche_CG=ac.getCarState(0, acsys.CS.LocalAngularVelocity)
	X_velocidad_angular_coche_CG_str=str(round(Velocidad_angular_coche_CG[0],4))
	Y_velocidad_angular_coche_CG_str=str(round(Velocidad_angular_coche_CG[1],4))
	Z_velocidad_angular_coche_CG_str=str(round(Velocidad_angular_coche_CG[2],4))
	f.write(X_velocidad_angular_coche_CG_str+";"+Y_velocidad_angular_coche_CG_str+";"+Z_velocidad_angular_coche_CG_str+";")
	
	Normal_rueda_RR=[0.0,0.0,0.0]
	Normal_rueda_RR=ac.getCarState(0,acsys.CS.TyreContactNormal, acsys.WHEELS.RR)
	X_Normal_rueda_RR_str=str(round(Normal_rueda_RR[0],4))
	Y_Normal_rueda_RR_str=str(round(Normal_rueda_RR[1],4))
	Z_Normal_rueda_RR_str=str(round(Normal_rueda_RR[2],4))
	f.write(X_Normal_rueda_RR_str+";"+Y_Normal_rueda_RR_str+";"+Z_Normal_rueda_RR_str+";")
	
	Normal_rueda_RL=[0.0,0.0,0.0]
	Normal_rueda_RL=ac.getCarState(0,acsys.CS.TyreContactNormal, acsys.WHEELS.RL)
	X_Normal_rueda_RL_str=str(round(Normal_rueda_RL[0],4))
	Y_Normal_rueda_RL_str=str(round(Normal_rueda_RL[1],4))
	Z_Normal_rueda_RL_str=str(round(Normal_rueda_RL[2],4))
	f.write(X_Normal_rueda_RL_str+";"+Y_Normal_rueda_RL_str+";"+Z_Normal_rueda_RL_str+";")
	
	Normal_rueda_FR=[0.0,0.0,0.0]
	Normal_rueda_FR=ac.getCarState(0,acsys.CS.TyreContactNormal, acsys.WHEELS.FR)
	X_Normal_rueda_FR_str=str(round(Normal_rueda_FR[0],4))
	Y_Normal_rueda_FR_str=str(round(Normal_rueda_FR[1],4))
	Z_Normal_rueda_FR_str=str(round(Normal_rueda_FR[2],4))
	f.write(X_Normal_rueda_FR_str+";"+Y_Normal_rueda_FR_str+";"+Z_Normal_rueda_FR_str+";")
	
	Normal_rueda_FL=[0.0,0.0,0.0]
	Normal_rueda_FL=ac.getCarState(0,acsys.CS.TyreContactNormal, acsys.WHEELS.FL)
	X_Normal_rueda_FL_str=str(round(Normal_rueda_FL[0],4))
	Y_Normal_rueda_FL_str=str(round(Normal_rueda_FL[1],4))
	Z_Normal_rueda_FL_str=str(round(Normal_rueda_FL[2],4))
	f.write(X_Normal_rueda_FL_str+";"+Y_Normal_rueda_FL_str+";"+Z_Normal_rueda_FL_str+";")
	
	
	Punto_contacto_rueda_RR=[0.0,0.0,0.0]
	Punto_contacto_rueda_RR=ac.getCarState(0,acsys.CS.TyreContactPoint,acsys.WHEELS.RR)
	X_Punto_contacto_rueda_RR_str=str(round(Punto_contacto_rueda_RR[0],4))
	Y_Punto_contacto_rueda_RR_str=str(round(Punto_contacto_rueda_RR[1],4))
	Z_Punto_contacto_rueda_RR_str=str(round(Punto_contacto_rueda_RR[2],4))
	f.write(X_Punto_contacto_rueda_RR_str+";"+Y_Punto_contacto_rueda_RR_str+";"+Z_Punto_contacto_rueda_RR_str+";")
	
	Punto_contacto_rueda_RL=[0.0,0.0,0.0]
	Punto_contacto_rueda_RL=ac.getCarState(0,acsys.CS.TyreContactPoint,acsys.WHEELS.RL)
	X_Punto_contacto_rueda_RL_str=str(round(Punto_contacto_rueda_RL[0],4))
	Y_Punto_contacto_rueda_RL_str=str(round(Punto_contacto_rueda_RL[1],4))
	Z_Punto_contacto_rueda_RL_str=str(round(Punto_contacto_rueda_RL[2],4))
	f.write(X_Punto_contacto_rueda_RL_str+";"+Y_Punto_contacto_rueda_RL_str+";"+Z_Punto_contacto_rueda_RL_str+";")

	Punto_contacto_rueda_FR=[0.0,0.0,0.0]
	Punto_contacto_rueda_FR=ac.getCarState(0,acsys.CS.TyreContactPoint,acsys.WHEELS.FR)
	X_Punto_contacto_rueda_FR_str=str(round(Punto_contacto_rueda_FR[0],4))
	Y_Punto_contacto_rueda_FR_str=str(round(Punto_contacto_rueda_FR[1],4))
	Z_Punto_contacto_rueda_FR_str=str(round(Punto_contacto_rueda_FR[2],4))
	f.write(X_Punto_contacto_rueda_FR_str+";"+Y_Punto_contacto_rueda_FR_str+";"+Z_Punto_contacto_rueda_FR_str+";")
	
	Punto_contacto_rueda_FL=[0.0,0.0,0.0]
	Punto_contacto_rueda_FL=ac.getCarState(0,acsys.CS.TyreContactPoint,acsys.WHEELS.FL)
	X_Punto_contacto_rueda_FL_str=str(round(Punto_contacto_rueda_FL[0],4))
	Y_Punto_contacto_rueda_FL_str=str(round(Punto_contacto_rueda_FL[1],4))
	Z_Punto_contacto_rueda_FL_str=str(round(Punto_contacto_rueda_FL[2],4))
	f.write(X_Punto_contacto_rueda_FL_str+";"+Y_Punto_contacto_rueda_FL_str+";"+Z_Punto_contacto_rueda_FL_str+";")


	FX_Vector_ruedas_RR=0.0
	FY_Vector_ruedas_RR=0.0
	FX_Vector_ruedas_RR=ac.getCarState(0,acsys.CS.TyreHeadingVector,acsys.WHEELS.RR)
	FY_Vector_ruedas_RR=ac.getCarState(0,acsys.CS.TyreRightVector,acsys.WHEELS.RR)
	FX_Vector_ruedas_RR_str=str(round(FX_Vector_ruedas_RR,4))
	FY_Vector_ruedas_RR_str=str(round(FY_Vector_ruedas_RR,4))	
	f.write(FX_Vector_ruedas_RR_str+";"+FY_Vector_ruedas_RR_str+";")
	
	FX_Vector_ruedas_RL=0.0
	FY_Vector_ruedas_RL=0.0
	FX_Vector_ruedas_RL=ac.getCarState(0,acsys.CS.TyreHeadingVector,acsys.WHEELS.RL)
	FY_Vector_ruedas_RL=ac.getCarState(0,acsys.CS.TyreRightVector,acsys.WHEELS.RL)
	FX_Vector_ruedas_RL_str=str(round(FX_Vector_ruedas_RL,4))
	FY_Vector_ruedas_RL_str=str(round(FY_Vector_ruedas_RL,4))	
	f.write(FX_Vector_ruedas_RL_str+";"+FY_Vector_ruedas_RL_str+";")
	
	FX_Vector_ruedas_FR=0.0
	FY_Vector_ruedas_FR=0.0
	FX_Vector_ruedas_FR=ac.getCarState(0,acsys.CS.TyreHeadingVector,acsys.WHEELS.FR)
	FY_Vector_ruedas_FR=ac.getCarState(0,acsys.CS.TyreRightVector,acsys.WHEELS.FR)
	FX_Vector_ruedas_FR_str=str(round(FX_Vector_ruedas_FR,4))
	FY_Vector_ruedas_FR_str=str(round(FY_Vector_ruedas_FR,4))	
	f.write(FX_Vector_ruedas_FR_str+";"+FY_Vector_ruedas_FR_str+";")
	
	FX_Vector_ruedas_FL=0.0
	FY_Vector_ruedas_FL=0.0
	FX_Vector_ruedas_FL=ac.getCarState(0,acsys.CS.TyreHeadingVector,acsys.WHEELS.FL)
	FY_Vector_ruedas_FL=ac.getCarState(0,acsys.CS.TyreRightVector,acsys.WHEELS.FL)
	FX_Vector_ruedas_FL_str=str(round(FX_Vector_ruedas_FL,4))
	FY_Vector_ruedas_FL_str=str(round(FY_Vector_ruedas_FL,4))	
	f.write(FX_Vector_ruedas_FL_str+";"+FY_Vector_ruedas_FL_str)#+";")
	
	"""
	OO=ac.getCarState(0,acsys.CS.Aero, acsys.o.1)
	OO_str=str(round(OO,4))
	#Y_Punto_contacto_rueda_str=str(round(Punto_contacto_rueda[1],4))
	#Z_Punto_contacto_rueda_str=str(round(Punto_contacto_rueda[2],4))
	f.write(OO)
	"""
	f.write("\n")
	#informacion = ac.addLabel(ventana_informacion, "Informacion prueba:");
	#ac.setText(informacion, "Informacion prueba: {}".format("\nNombre del condiztor: "+nombre+"\n Circuito: "+circuito))
	#velocidadmph=str(round(velocidad_modulo[1],4))
	#velocidadms=str(round(velocidad_modulo[2],4))
"""	
	ac.console(momento+","
		+coor_x+","+coor_y+","+coor_z+","
		+velocidad_x+","+velocidad_y+","+velocidad_z+","
		+velocidadms+","
		+gas_presion_0_a_1+","
		+brake_presion_0_a_1+","
		+Clutch_presion_0_a_1+","
		+Marcha_str+","
		+RPM_motor_str+","
		+Posicion_coche_pista_normalizada_str+","
		+Direccion_ruedas_delanteras_str+","
		+Gs_vehiculo_str+","		
		+X_velocidad_angular_coche_CG_str+","+Y_velocidad_angular_coche_CG_str+","+Z_velocidad_angular_coche_CG_str)
		
	 #ac.setText("DATOS:\n {}".format("Momento ="+momento+"\n"
	#	+"x="+coor_x+"\n y="+coor_y+" \n z="+coor_z+"\n"
	#	+"Vx="+velocidad_x+"\n Vy="+velocidad_y+"\n Vz="+velocidad_z+"\n"
	#	+"Vmod(m/s)="+velocidadms+"\n"
	#	+"presion pedal ac. de 0 a 1="+gas_presion_0_a_1+"\n")) # informacion pantalla del automovil
		
	ac.log(momento+","
		+coor_x+","+coor_y+","+coor_z+","
		+velocidad_x+","+velocidad_y+","+velocidad_z+","
		+velocidadms+","
		+gas_presion_0_a_1+","
		+brake_presion_0_a_1+","
		+Clutch_presion_0_a_1+","
		+Marcha_str+","
		+RPM_motor_str+","
		+Posicion_coche_pista_normalizada_str+","
		+Direccion_ruedas_delanteras_str+","
		+Gs_vehiculo_str+","		
		+X_velocidad_angular_coche_CG_str+","+Y_velocidad_angular_coche_CG_str+","+Z_velocidad_angular_coche_CG_str+"\n")
"""
def acShutdown():	
	global f
	f.close()
	
		




import socket

#49152-6535 puertos disponibles
host='localhost'
port = 5005 #Puerto ocupado en TCP
BUFFER_SIZE = 2048

def crear_archivo(URL,HEADER):
	arch=open("URL.txt","a+")
	arch.write("###############################################################\n")
	arch.write("Pagina consultada:"+str(URL)+" \n")
	arch.write("Header obtenido: \n" )
	arch.write(str(HEADER))
	arch.write("\n ###############################################################\n")



def ConexionUDP(direccion_servidor,port,URL): #Funcion para la conexion TCP
	UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP		
	mensaje = "OK"                       
	UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(direccion_servidor,int(port))) #Enviamos el mensaje OK
	respuesta, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) #Obtenemos la respuesta del servidor
	print(respuesta.decode()) #Eliminar despues
	crear_archivo(URL,respuesta) #Guardamos HEADER en archivo
	print("Respuesta Guardada en archivo URL.txt")
	UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP





TCP_SOCKET_CLIENTE=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creamos Conexion TCP
TCP_SOCKET_CLIENTE.connect((host, port)) #Nos conectamos
mensaje=""
print("##################################################################################")
print("Conexión establecida con el servidor en el puerto "+str(port))
print("##################################################################################")
while mensaje!="terminate": 
	print("# Ingrese el nombre de la página a buscar o ingrese 'terminate' para cerrar conexión")
	mensaje=input("Ingrese opción: ") #Pedimos URL
	TCP_SOCKET_CLIENTE.send(mensaje.encode('utf-8'))
	if mensaje!='terminate':#verificamos que no se quiera terminar conexion
		data = TCP_SOCKET_CLIENTE.recv(BUFFER_SIZE)#recibimos resultado
		data=data.decode()
		print(data)
		print(data.strip().split("?|¿"))
		status,puerto=data.strip().split("?|¿")
		if status=="OK":
			ConexionUDP('localhost',puerto,mensaje)#Creamos conexion UDP


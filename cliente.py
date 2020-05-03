import socket

#49152-6535 puertos disponibles
host='localhost'
port = 5007 #Puerto ocupado en TCP
BUFFER_SIZE = 2048


def createFile(response,URL):
	arch=open(str(URL)+".txt","a+")
	arch.write("-------------------------------------------------")
	arch.write("Contenido Header de la URL: "+str(URL))
	arch.write(response)
	arch.close()
	


def ConexionUDP(direccion_servidor,port,URL): #Funcion para la conexion TCP
	UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP		
	mensaje = "OK"                       
	UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(direccion_servidor,int(port))) #Enviamos el mensaje OK		
	response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) #Obtenemos la respuesta del servidor	
	UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP
	createFile(response.decode(),URL)	
	print("# Header Recibido")			
	return





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
		status,puerto=data.strip().split("?|¿")
		if status=="OK":
			ConexionUDP('localhost',puerto,mensaje)#Creamos conexion UDP
		else:
			print("[°](Mensaje Servidor) No se encontro el sitio web o no estaba disponible")	
	print("-------------------------------------------") 	
TCP_SOCKET_CLIENTE.close() 	



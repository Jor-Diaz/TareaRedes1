import socket

#49152-6535 puertos disponibles
port = 5004 #Puerto ocupado en TCP
BUFFER_SIZE = 2048 




def getHeader(DOMAIN):       
    request = "GET / HTTP/1.1\nHost: "+DOMAIN+"\n\n"
    request = bytes(request, encoding="ascii") ### no borrar
    socketWeb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socketWeb.connect((DOMAIN, 80))
        socketWeb.send(request)
    except Exception as e:
        return "",-1        
    result = socketWeb.recv(2048)    
    result=result.decode().split("<HTML>")
    print("# Contenido del Header obtenido")            
    return result[0], 0


def ConexionUDP(respuesta):#Funcion para conexion UDP
    port = 5006 #Puerto ocupado en UDP
    UDP_SOCKET_SERVIDOR = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#Creamos el socket
    UDP_SOCKET_SERVIDOR.bind(('',port))    
    mensaje,direccion_cliente = UDP_SOCKET_SERVIDOR.recvfrom(BUFFER_SIZE)#Recibimos del cliente    
    print("[°] LLego el cliente")
    print("[°] Mensaje del Cliente: " + str(mensaje.decode()) )        
    UDP_SOCKET_SERVIDOR.sendto(respuesta.encode(),direccion_cliente)#Enviamos la respuesta 
    UDP_SOCKET_SERVIDOR.close() #Cerramos la conexion UDP
    return

## MAIN
#LRU=[('DOMINIO','RESPUESTA'),('DOMINIO','RESPUESTA'),('DOMINIO','RESPUESTA'),('DOMINIO','RESPUESTA')]
TCP_SOCKET_SERVIDOR=socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creamos un objeto socket tipo TCP
TCP_SOCKET_SERVIDOR.bind(('', port)) 
TCP_SOCKET_SERVIDOR.listen(1) # Esperamos la conexión del cliente 
print('# Conexión abierta. Escuchando solicitudes en el puerto ' +str(port)) 
TCP_SOCKET_CLIENTE, addr = TCP_SOCKET_SERVIDOR .accept() # Establecemos la conexión con el cliente 
print('# Conexión establecida con el cliente')
while True:
    # Recibimos bytes, convertimos en str
    data = TCP_SOCKET_CLIENTE.recv(BUFFER_SIZE)   
    try:
        URL = data.decode("utf-8")                
        print('# Mensaje recibido de cliente: {}'.format(data.decode('utf-8'))) 
        if URL == "terminate":                    
            print("# Conexión terminada")                    
            break                             
        else:    
            existe_en_LRU=0    
            #existe_en_LRU=BuscarEnLRU(URL)            
            print("# Buscando el HEADER de la url "+str(URL))
            header,estado = getHeader(URL)                                            
            if estado==-1 and existe_en_LRU==0:
                respuesta="FAIL?|¿5006"
                TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes       
                print("# No se encontro el sitio web o no esta disponible")                             
            else:            
                respuesta="OK?|¿5006"
                TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes              
                print("# Enviado mensaje para conexion UDP")
                ConexionUDP(header)#deberiamos remplazar el valor por el header                
                print("# Contenido del HEADER ENVIADO")
                print("# Regresando a Conexion TCP")                                                         
        print("-------------------------------------------")                                                         
    except Exception as e:
        raise TCP_SOCKET_CLIENTE.close() 
TCP_SOCKET_CLIENTE.close() 

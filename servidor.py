import socket

#49152-6535 puertos disponibles
port = 5005 #Puerto ocupado en TCP
BUFFER_SIZE = 2048 
END=False



def getHeader(DOMAIN):   
    #arch.write("###############################################################\n")
    #arch.write("Pagina consultada:"+str(DOMAIN)+" \n")
    #arch.write("Header obtenido: \n" )
    resp = ''
    request = "GET / HTTP/1.1\nHost: "+DOMAIN+"\n\n"
    request = bytes(request, encoding="ascii") ### no borrar
    socketWeb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketWeb.connect((DOMAIN, 80))
    socketWeb.send(request)
    result = socketWeb.recv(2048)
    print("header obtained")
    #arch=open(DOMAIN+".txt","a")
    while (len(result) > 0):
        resp = resp + str(result.decode())
        #arch.write(str(result.decode()))
        result = socketWeb.recv(2048)
    #arch.close()
    print("got it")
    return resp

def ConexionUDP(DOMAIN):#Funcion para conexion UDP
    port = 5006 #Puerto ocupado en UDP
    UDP_SOCKET_SERVIDOR = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#Creamos el socket
    UDP_SOCKET_SERVIDOR.bind(('',port))    
    mensaje,direccion_cliente = UDP_SOCKET_SERVIDOR.recvfrom(BUFFER_SIZE)#Recibimos del cliente    
    print("##LLego el cliente")
    print("##Mensaje del Cliente: " + str(mensaje.decode()) )
    respuesta = getHeader(DOMAIN)
    UDP_SOCKET_SERVIDOR.sendto(respuesta.encode(),direccion_cliente)#Enviamos la respuesta 
    UDP_SOCKET_SERVIDOR.close() #Cerramos la conexion UDP


## MAIN

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
            #PeticionGet(URL) esta deberia ser la funcion que nos trae el header de la cosa
            #Aca deberia ir un if si la pagina esta disponible y obtuvimos el header
            print("#Buscando el HEADER de la url "+str(URL))
            print()
            respuesta="OK?|¿5006"                  
            TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes      
            print("Enviado mensaje para conexion UDP")
            ConexionUDP(URL)#deberiamos remplazar el valor por el header
            print()
            print("#Contenido del HEADER ENVIADO")
            print("#Regresando a Conexion TCP")
            print()
    except Exception as e:
        raise e
TCP_SOCKET_CLIENTE.close() 
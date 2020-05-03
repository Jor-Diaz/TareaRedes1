import socket

#49152-6535 puertos disponibles
port = 5007 #Puerto ocupado en TCP
BUFFER_SIZE = 2048 
LRU = [ ]



def save_cache_LRU():
    arch=open("cache.txt","w")
    for i in LRU:
        arch.write(i[0])        
        arch.write("\n")
        arch.write("!!!!\n")        
        arch.write(i[1])
        arch.write("\n")
        arch.write("#######\n")
    arch.close()

def cargar_LRU():
    arch=open("cache.txt","r")
    a=0
    dominio=""
    aux=""
    header=""    
    for i in arch:
        if a==1:
            if i=="#######\n":                
                LRU.append(tuple((dominio, header)))
                header=""
                a=0
            else:
                header+=i  
        if a==0:        
            if i=="!!!!\n":                
               dominio=aux.strip()               
               a=1
            aux=i            

    arch.close()

cargar_LRU()
for i in LRU:
    print(i[0])
def searchInLRU(domain):   
    pos=0 
    for t in LRU:
        if domain in t:
            return pos
        pos+=1        
    return -1

def obtenerDeLRU(domain):
    index = searchInLRU(domain)
    if index != -1:
        return LRU[index][1]
    else:
        return "Error"

def add_to_LRU(domain, response):
    if len(LRU) == 5:
        LRU.append(tuple((domain, response)))
        LRU.pop(0)
    else:
        LRU.append(tuple((domain, response)))


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
    result=result[0].split("<html>")
    result=result[0].split("<!DOCTYPE")
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
    URL = data.decode("utf-8")                
    print('# Mensaje recibido de cliente: {}'.format(data.decode('utf-8'))) 
    if URL == "terminate":                    
        print("# Conexión terminada")                    
        break                             
    else:    
        inLRU=0    
        inLRU= searchInLRU(URL)                                                                            
        if inLRU!=-1:
            print("# HEADER de la url "+str(URL)+" esta en la LRU")   
            header = obtenerDeLRU(URL)
            respuesta="OK?|¿5006"
            TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes              
            print("# Enviado mensaje para conexion UDP")
            ConexionUDP(header)#deberiamos remplazar el valor por el header                
            print("# Contenido del HEADER ENVIADO")
            print("# Regresando a Conexion TCP")    

        else:
            print("# Buscando el HEADER de la url "+str(URL))   
            header,estado = getHeader(URL)
            if estado==-1 : # si el url no se encuentra en la web ni en la LRU
                respuesta="FAIL?|¿5006"
                TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes       
                print("# No se encontro el sitio web o no esta disponible")                                                             
            else: #existe peroooo no la tengo en la LRU
                add_to_LRU(URL, header)                    
                respuesta="OK?|¿5006"                    
                TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes              
                print("# Enviado mensaje para conexion UDP")
                ConexionUDP(header)#deberiamos remplazar el valor por el header                
                print("# Contenido del HEADER ENVIADO")
                print("# Regresando a Conexion TCP")                                                         
    print("-------------------------------------------")                                                             
save_cache_LRU()
TCP_SOCKET_CLIENTE.close() 

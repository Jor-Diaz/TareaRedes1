import socket

#49152-6535 puertos disponibles
port = 5007 #Puerto ocupado en TCP
BUFFER_SIZE = 2048 
LRU = [ ]



def save_cache_LRU():#Funcion para guardar lo existente en la LRU en un archivo
    arch=open("cache.txt","w")#Abrimos el archivo Cache
    for i in LRU:#Escribimos el contenido de la URL
        arch.write(i[0])#Escribimos el dominio        
        arch.write("\n")
        arch.write("!!!!\n")#Escribimos un separador        
        arch.write(i[1])#Escribimos el header
        arch.write("\n")
        arch.write("#######\n")#Separador 
    arch.close()#Cerramos el archivo

def cargar_LRU():#Cargamos la data de la LRU
    arch=open("cache.txt","r")#Leemos el archivo cache 
    a=0#variable auxiliar para saber si hemos o no detectado un header
    dominio=""
    aux=""#variable auxiliar para almacenar el dominio 
    header="" #variable auxiliar para almacenar el header   
    for i in arch:
        if a==1:#ya encontramos un dominio
            if i=="#######\n":            #Termino el header    
                LRU.append(tuple((dominio, header)))#Cargamos a la LRU
                header=""#Seteamos denuevo las variables
                a=0
            else:
                header+=i  #Seguimos guardando header
        if a==0:  # Aun no encontramos dominio
            if i=="!!!!\n": #Encontramos dominio               
               dominio=aux.strip()#almacenamos el dominio               
               a=1#Marcamos la variable auxiliar
            aux=i            
    arch.close()#Cerramos el archivo

def searchInLRU(domain):#Buscamos el dominio en La LRU
    pos=0 
    for t in LRU:
        if domain in t:
            return pos#Retornamos la posicion si es que esta
        pos+=1        
    return -1#Retornamos -1 si no esta

def obtenerDeLRU(domain):#obtenemos el header de un dominio en la LRU
    index = searchInLRU(domain)#buscamos la posicion
    if index != -1:#si si esta retornamos el contenido
        return LRU[index][1]
    else:
        return "Error"#sino error por que antes fue verificada

def add_to_LRU(domain, response):#agregamos un dominio y su contenido a la LRU
    if len(LRU) == 5:#Largo maximo LRU por enunciado de la tarea
        LRU.append(tuple((domain, response)))#Agregamos el contenido
        LRU.pop(0)#sacamos uno
    else:
        LRU.append(tuple((domain, response)))#agregamos


def getHeader(DOMAIN):       
    request = "GET / HTTP/1.1\nHost: "+DOMAIN+"\n\n" #Creamos la peticion http 
    request = bytes(request, encoding="ascii") # codificamos la peticion
    socketWeb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creamos el socket para conectarnos
    try:#vemos si existe el sitio
        socketWeb.connect((DOMAIN, 80))#nos conectamos al dominio en el puerto 80
        socketWeb.send(request) #hacemos la peticion

    except Exception as e:#si no existe retornamos el -1
        return "",-1        
    result = socketWeb.recv(2048) #Recibimos la respuesta
    #hacemos split a al header de diferentes tipos para limpiar el contenido   
    result=result.decode().split("<HTML>")
    result=result[0].split("<html>")
    result=result[0].split("<!DOCTYPE")
    socketWeb.close()#Cerramos el socket
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
cargar_LRU()
TCP_SOCKET_SERVIDOR=socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creamos un objeto socket tipo TCP
TCP_SOCKET_SERVIDOR.bind(('', port)) 
TCP_SOCKET_SERVIDOR.listen(1) # Esperamos la conexión del cliente 
print('# Conexión abierta. Escuchando solicitudes en el puerto ' +str(port)) 
TCP_SOCKET_CLIENTE, addr = TCP_SOCKET_SERVIDOR .accept() # Establecemos la conexión con el cliente 
print('# Conexión establecida con el cliente')
while True:    
    # Recibimos bytes, convertimos en str
    data = TCP_SOCKET_CLIENTE.recv(BUFFER_SIZE)       
    URL = data.decode()                
    print('# Mensaje recibido de cliente: {}'.format(data.decode('utf-8'))) 
    if URL == "terminate":                    
        print("# Conexión terminada")                    
        break                             
    else:    
        inLRU=0    
        inLRU= searchInLRU(URL)#recibisamos si esta en la LRU                                                                            
        if inLRU!=-1:#Si esta en la LRU
            print("# HEADER de la url "+str(URL)+" esta en la LRU")   
            header = obtenerDeLRU(URL)#obtenemos el header de la LRU
            respuesta="OK?|¿5006"
            TCP_SOCKET_CLIENTE.send(respuesta.encode()) # enviamos el ok al clinete
            print("# Enviado mensaje para conexion UDP")
            ConexionUDP(header)#Comenzamos la conexion udp para enviar el header            
            print("# Contenido del HEADER ENVIADO")
            print("# Regresando a Conexion TCP")    

        else:
            print("# Buscando el HEADER de la url "+str(URL))   
            header,estado = getHeader(URL)#vemos si existe la pagina web  y buscamos el header
            if estado==-1 : # si el url no se encuentra en la web ni en la LRU
                respuesta="FAIL?|¿5006"
                TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes       
                print("# No se encontro el sitio web o no esta disponible")                                                             
            else: #existe peroo no la tengo en la LRU
                add_to_LRU(URL, header)#lo agregamos a la LRU                    
                respuesta="OK?|¿5006"                    
                TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Enviamos el ok al cliente para la conexion UDP
                print("# Enviado mensaje para conexion UDP")
                ConexionUDP(header)#Comenzamos la conexion udp para enviar el header                
                print("# Contenido del HEADER ENVIADO")
                print("# Regresando a Conexion TCP")                                                         
    print("-------------------------------------------")                                                             
save_cache_LRU()#Salvamos la LRU en el archivo cache
TCP_SOCKET_CLIENTE.close()#terminamos la conexion TCP

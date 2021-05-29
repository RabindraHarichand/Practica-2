import socket
import sys
import base64
import hashlib

#Ingresar datos
ip= (input('Escriba su ip '))
user= (input('Escriba un usuario '))
try:
    #Establecer conexión TCP hacial servidor por el puerto 19876
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 19876))
    s.settimeout(20)
    #Enviar comando helloiam junto con nombre de usuario
    s.send(bytes("helloiam "+user, "utf-8"))

    #Recibir respuesta del servidor
    data = s.recv(1024)
    print('Received', repr(data))

    # Pedir longitud del mensaje
    s.send(bytes("msglen", "utf-8"))

    #Recibir respuesta del servidor
    data = s.recv(1024)
    print('Received', repr(data))


    #Pedir Mensaje al servidor
    s.send(bytes("givememsg 15601","utf-8"))
    data = s.recv(1024)
    #Cliente UDP
    UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPSocket.bind(('', 15601))

    UDPSocket.settimeout(10)
    i =0
    while i < 10:
        try:
            dataU = UDPSocket.recvfrom(5000)
        except socket.timeout as e:  
            print ("Ocurrio un error por tiempo espera superado del UDP")
        i+=1
    try:
        if not(dataU == ()): 
            message = dataU[0]
            address = dataU[1]
    except NameError as e:
        print("Error de conexión, el mensaje no pudo ser retirado, intentelo mas tarde")
        sys.exit()  
    
    msg = base64.b64decode(message)
    mensage=msg.decode('utf-8')
    print(repr(mensage))
    # md5 y paso a hexadecimal
    Dec=hashlib.md5(msg).hexdigest()

    #validacion del mensaje
    s.send(bytes("chkmsg "+ Dec,"utf-8"))
    data = s.recv(1024)
    print('Received', repr(data))

    #salida
    s.send(bytes("bye","utf-8"))
    data = s.recv(1024)
    print('Received', repr(data))

except Exception as e:  
    print (e)
# PIBL

## Tabla de contenidos
[INTRODUCCIÓN](#INTRODUCCIÓN)  
[DESARROLLO](#DESARROLLO)      
[Lenguajes y programas](#Lenguajes-y-programas)
[Uso y creación](#Uso-y-creación)   
[Archivo configuraciones.py](#Archivo-configuraciones.py)     
[Archivo RoundRobinn.py](#Archivo-RoundRobinn.py)  
[Archivo proxy.py](#Archivo-proxy.py)       
[funciones](#funciones:)

[CONCLUSIONES](#CONCLUSIONES)   
[DESARROLLADO POR](#DESARROLLADO-POR)  
[REFERENCIAS](#REFERENCIAS) 

# INTRODUCCIÓN

Este proyecto está basado en una arquitectura cliente/servidor utilizando la API sockets, haciendo uso de la técnica del multi hilo, usando un algoritmo balanceador de carga llamado round-robbin y creando un proxy inverso.

Basado en lo anteriormente mencionado, el algoritmo balanceador de
carga 'round-robin', se encarga de distribuir las peticiones entrantes por parte de los clientes hacia un conjunto de servidores de manera balanceada, luego por cada petición, el servidor debe devolver una respuesta al cliente.

El proxy inverso implementado se encarga de interceptar las peticiones del cliente y la envía al servidor anteriormente asignado por el round-robbin con la capacidad de procesar esa información para luego enviarse una respuesta al cliente.

# DESARROLLO

## Lenguajes y programas

El lenguaje de programación que usamos fue Python debido a la capacidad y el manejo que tiene de los hilos, hace que sea un poco más sencillo de entender la técnica y la aplicabilidad.
El programa que usamos es Visual Studio Code porque tiene muy buenas extensiones las cuales hacen que codificar sea más cómodo y tiene muy buen manejo de las ejecuciones de múltiples lenguajes.


## Uso y creación

En este creamos 3 archivos.py.

- Para la configuración que trae la conexión con el servidor, un archivo llamado configuraciones.py.
- Para el proxy inverso encargado de la comunicación cliente/servidor, un archivo llamado proxy.py.
- Para el round-robin encargado de balancear la carga, un archivo llamado RoundRobinn.py.

### Archivo configuraciones.py

En este archivo asignamos como variables las necesarias para configurar la conexión con el servidor, pasándole los puertos, el lenguaje que entiende, un tamaño para el buffer, y el host donde se aloja.

```python

PUERTO = 8080
PUERTOI = 80
HOST = '127.0.0.1'
FORMATO = 'utf-8'
IP = ''
TAMAÑO = 4050

```

### Archivo RoundRobinn.py

En este archivo nos encargamos de la creación de todo el algoritmo de round-robin para balancear la carga entre los servidores como sigue:

```python
def roundRobin():
  listaInstancias = ['18.234.185.41', '44.204.176.223', '44.204.176.223']

  with open("robin.txt", 'r') as f:
    i = f.readline()
    f.close()

  if i == '0':
    i = int(i) + 1 
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[0]
  elif i == '1':
    i = int(i) + 1
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[1]
  elif i == '2':
    i = 0
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[2]

if __name__ == "__main__":
  roundRobin()

```
En resumen lo que hace es guardar los servidores en un arreglo, luego abrir y crear un archivo.txt llamado robin.txt, dentro de este tiene un numero 0, luego se comprueba que numero tiene ese archivo en caso de ser 0, lo modifica a 1, y trae la posición 0 del arreglo anteriormente creado es decir el primer servidor, luego como el archivo tiene un 1, al leerlo, modifica el valor a 2, y trae la posición 1 del arreglo anteriormente creado es decir el segundo servidor, y por ultimo lee en el robin.txt un 2, lo que hace es modificarlo nuevamente a 0, y leer la tercera posición del arreglo, es decir, el tercere servidor, y así sucesivamente ya que nuevamente está en cero.

En otras palabras, cada que entre un nuevo cliente lo asigna de 1 en 1 en cada servidor.

### Archivo proxy.py

En este archivo nos encargamos de la comunicación cliente/servidor, haciendo uso también de los anteriores 2 archivos.py creados.

en este caso debemos hacer las siguientes importaciones:

```python
import socket
import time
import os
import threading
import configuraciones
import RoundRobinn
```
- La librería de sockets, para la creación de los sockets que sirven para realizar las conexiones entre cliente/servidor.

- La librería de tiempo para calcular cuánto tiempo se debe almacenar la cache.
- La librería del sistema operativo, para el manejo de los ficheros y rutas.
- La librería de threading para permitir el uso de varios clientes en la parte del servidor (multi hilo).
- Hacemos llamado de los dos archivos.py anteriormente creados que son configuraciones.py y RoundRobinn.py.

Luego se hace la creación de las funciones

#### funciones:

- creamos la función proxy() encargada de configurar los sockets, llamarlos para hacer las peticiones dependiendo del puerto dado en el archivo de configuraciones, y validar si está conectado.

```python
def proxy():
  sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sockets.bind((configuraciones.HOST, configuraciones.PUERTO))
  sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #configurar el tipo de socket
  print(f'Escuchando peticiones en el puerto {configuraciones.PUERTO}')
  sockets.listen(5)

  while True:
    try:
      conectado, direccion = sockets.accept()
      Uconectado = f'Usuario conectado {direccion} con : {conectado}'
      print(Uconectado)
      loggin(Uconectado)
      thread = threading.Thread(target = multiUsuario, args = (conectado, direccion))
      thread.start()
    except:
      print("Coneccion terminada")
      break
  sockets.close()
```

- Esta función permite conectar multiples usuarios al servidor al mismo tiempo, permitiendoles hacer peticiones simultaneamente y recibir su respectiva respuesta por parte del mismo.

```python
def multiUsuario(conectado, direccion):
  contenidoHttp = ''
  while True:
    try:
      contenidoHttp1 = conectado.recv(configuraciones.TAMAÑO)
      print(f'Solicitud del usuario : {contenidoHttp1}')
      if contenidoHttp1 != b'':
        contenidoHttp = contenidoHttp1.decode()
        print(contenidoHttp)
        solicitud = contenidoHttp.split('\n')[0]
        loggin(solicitud)
        IPusuario = contenidoHttp.split('\n')[1]
        direccionHost = IPusuario.lstrip("Host:") 
        print(f'solicitud : {solicitud}')
        print(f'direccion Host: {direccionHost}')
        coneccionInstancia(conectado,direccion, contenidoHttp1, solicitud, direccionHost)
        #eliminar la direccion y direccionHost
      else:
        print("En el else de multiusuario")
        break
    except:
      print("en el except")
      break
```
- en esta funcion llamamos la funcion de cache() dependiendo de la coneccion de la instancia, entonces se toma el tiempo actual y se resta con el inicial, permitiendo saber cuanto tiempo ha pasado para poder borrar luego y no tener la cache permanente.  
cuando se envian los datos, lo que hace la funcion es averiguar si ya existe un archivo con la solicitud, en caso de que no seria hacerlo y almacenar las peticiones dadas por el usuario. en caso de que ya exista, ya sea por haber recargado la pagina, empieza a contar el tiempo de almacenamiento para luego ser borrado.

```python
def coneccionInstancia(conectado, direccionC, contenidoHttp, solicitud, cliente):
  #eliminar direccion c y cliente  
  socketN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  solicitud1 = solicitud.split(' ')[1]
  solicitud1 = solicitud1.replace("/", '')
  solicitud1 = solicitud1.replace(":", '')
  solicitud1 = solicitud1 + '.txt'
  
  nombreArchivos = os.listdir('cache/')
  contadorCache = 0

  if solicitud1 in nombreArchivos:
    tiempoFinal = time.time()
    with open(f'cache/{solicitud1}', 'rb') as archivo:
      tiempoArchivo = archivo.readline().decode()
    tiempoTotal = tiempoFinal - float(tiempoArchivo)
    if tiempoTotal >= 60:
      print("elminando el archivo")
      os.remove(f'cache/{solicitud1}')
      contadorCache = 0
    else:
      contadorCache = 1
  else:
    contadorCache = 0

  if contadorCache == 1:
    print("entro en el cache")
    with open(f'cache/{solicitud1}', 'rb') as archivo:
      datosCache = archivo.readlines()[1:]
    datosCache = b''.join(datosCache)
    envioDataCliente(conectado, direccionC, cliente, datosCache)
    socketN.close()
  else:
    RoundRobin = RoundRobinn.roundRobin()
    print(RoundRobin)
    socketN.connect((RoundRobin, configuraciones.PUERTOI))
    print(contenidoHttp)
    socketN.sendall(contenidoHttp)
    print("consultando a la intancia")
    
    while True:
      rInstancia = []
      datos = socketN.recv(configuraciones.TAMAÑO)
      rInstancia.append(datos)
      while len(datos) != 0:
        datos = socketN.recv(configuraciones.TAMAÑO)
        rInstancia.append(datos)
      rInstancia = b''.join(rInstancia)
      
      if len(rInstancia) != 0:
        tiempoInicial = time.time()
        cache(solicitud, rInstancia, tiempoInicial)
        envioDataCliente(conectado, direccionC, cliente, rInstancia)
        break
      else:
        print("no se recibieron datos de la instancia")
        break
    socketN.close()
```
- envioDataCliente() es la encargada de que en la parte del servidor envie los datos de la instancia o servidor al cliente en caso de estar conectado

```python
def envioDataCliente(conectado, direccionC, cliente, rInstancia):
  conectado.sendall(rInstancia)
  print("datos enviados al cliente")
```
- loggin() es la encargada de crear un log de lo que ocurre entre el servidor y los clientes que se conectaron, es decir un registro de lo que ocurrió y los datos enviados entre ambas entidades, guardando así un archivo llamado loggin.txt con la información anteriormente mencionada.


```python
def loggin(texto):
  f = open ('loggin.txt','a')
  texto = texto + '\n'
  f.write(texto)
  f.close()
```
- Esta funcion es la encargada de crear el archivo de cache, para administrarlo luego en la función de coneccionInstancia(), lo que hace es almacenar un archivo con la información que el cliente envia al servidor, con el tiempo de cuándo se creó.

```python
def cache(solicitud, response, tiempo):
  solicitud = (solicitud).split(' ')[1]
  solicitud = solicitud.replace("/", '')
  solicitud = solicitud.replace(":", '')
  f = open(f'cache/{solicitud}.txt', 'ab')
  f.write(str(tiempo).encode() + '\n'.encode())
  f.write(response)
  f.close()
```
- por ultimo para su ejecución final se hace llamado al proxy en un main, para que funcione de la manera que se requiere.
```python
if __name__ == "__main__":
  proxy()
```

# CONCLUSIONES

- Logramos entender el funcionamiento y cómo hacer uso de los sockets, como escuchar, conectar, recibir y demás funcionalidades de los sockets.
- Aprendimos cómo crear un proxy inverso, su aplicabilidad y cómo se usarlo de intermediario en la conexión entre cliente/servidor para hacer que haya un balance de cargas aplicando la técnica del round-robin.
- Entendimos el funcionamiento de la cache, y como persistir datos enviados por parte del cliente al servidor y almacenarlo en un tiempo asignado.
- Entendimos la importancia de un log, para así tener todas las peticiones y respuestas entre los clientes y el servidor, para manejar de manera más sencilla algunos posibles errores y estar al tanto de lo que ocurre entre las comunicaciones entre las entidades.
- Hubo muy buen trabajo en equipo y buena coordinación, por lo que la practica se pudo hacer y enteder de manera clara.



# DESARROLLADO POR

[Tomás Marín Aristizabal](https://github.com/tmarina1).  
[Juan Andrés Vera Álvarez](https://github.com/Vera3588).   
[Samuel Salazar Salazar](https://github.com/ssalazar11).



# REFERENCIAS
[TCP Sockets](https://realpython.com/python-sockets/#tcp-sockets).                                   
             [Solicitudes HTTP](https://unipython.com/solicitudes-http-en-python-con-requests/).                
[Sockets server](https://docs.python.org/es/3/library/socketserver.html).   
[Timer functions](https://www.delftstack.com/es/howto/python/python-timer-functions/).    
[OS module](https://www.tutorialsteacher.com/python/os-module#:~:text=The%20OS%20module%20in%20Python,with%20the%20underlying%20operating%20system).

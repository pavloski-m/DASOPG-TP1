import json
import socket
import sys
import csv
import sched, time
import signal

PORT_SERVER = 10000
ITER_TIME = 30

def readFile():
    try:
        with open("config.txt", 'r') as configFile:
            auxString = configFile.readline()
            auxString = auxString.strip()
            auxString = auxString.split('=')
            fileCSV = auxString[1]
    except IOError:
        print("No pudo abrirse el dato de configuración")
    
    try:
        with open(fileCSV, 'r') as csv_file:
            datos_csv = csv.DictReader(csv_file)
            data = list(datos_csv)
            dataTx = json.dumps(data)
    except IOError:
        print("No pudo abrirse el archivo de datos CSV")

    return dataTx

def updatePrices(datos):
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', PORT_SERVER)

    try:
        # Send data
        print('enviando actualización de precios...')
        sent = sock.sendto(datos.encode('ascii'), server_address)

    finally:
        print('closing socket')
        sock.close()

def signal_handler(sig, frame):
    print('-----Proceso terminando-----')
    sys.exit(0)

def do_something(sc): 
    print("nueva iteración...")
    
    datos = readFile()
    updatePrices(datos)    
    
    sc.enter(ITER_TIME, 1, do_something, (sc,))


signal.signal(signal.SIGINT, signal_handler)

s = sched.scheduler(time.time, time.sleep)

datos = readFile()
updatePrices(datos) 

s.enter(ITER_TIME, 1, do_something, (s,))
s.run()
from azure.storage.blob import BlobService
from time import sleep
import socket
import threading
import sys
from email.utils import formatdate

def StateThread():
    
    global initializeNow
    global isPrimary
    while 1:
        try:
            currentHost = socket.gethostname()
            blob_service = BlobService(account_name=azureStorageAccountName, account_key=azureStorageAccountKey)
            if (initializeNow == True):
                initializeNow = False
                print("Initializing '" + currentHost + "' as primary.")
                newContents = currentHost
                blob_service.create_container(container)
                blob_service.put_block_blob_from_text(container, blob, newContents)

            while 1:
                print("Downloading current state.")
                currentContents = blob_service.get_blob_to_text(container, blob)
                if (currentContents==currentHost):
                    isPrimary = True
                    print("isPrimary = True")
                    # we have now received status, if second thread NOT running, start
                    if (t2.isAlive() == False):
                        t2.start()
                elif (currentContents!=currentHost and currentContents.count>0):
                    isPrimary = False
                    print("isPrimary = False")
                    # we have now received status, if second thread NOT running, start
                    if (t2.isAlive() == False):
                        t2.start()
                sleep(.1)
        except Exception as e:
            print ("Error in MainStateThread: " + e)

def TcpProbeThread():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
 
    #Bind socket to local host and port
    try:
        s.bind((hostToListenTo, portToListenTo))
    except socket.error as msg:
        print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
        sys.exit()
    print("Socket bind complete")
    while 1:
        try:
            s.listen(10)
            print("Socket now listening...")
            conn, addr = s.accept()
            print("New TCP connection accepted.")
            headers = "Date: " + formatdate(timeval=None, localtime=False, usegmt=True) + "\nContent-Type: text/html\nContent-Length: 13\n\n<html></html>\n"
            if (isPrimary):
                print("Sending HTTP/1.1 200 OK")
                s.send("HTTP/1.1 200 OK\n" + headers)
                print ("Sent.")
            else:
                print("Sending HTTP/1.1 503 Service Unavailable")
                s.send("HTTP/1.1 503 Service Unavailable\n" + headers)
                print ("Sent.")
            print("Connected with " + addr[0] + ":" + str(addr[1]))
            s.close()
        except Exception as e:
            print ("Error in TcpProbeThread: " + e)

# Main Code
hostToListenTo = "" # no value indicates any address
portToListenTo = 14301
 
azureStorageAccountName = "[removed]"
azureStorageAccountKey = "[removed]"
container = "ilbcp1"
blob = "currentprimary.dat"
initializeNow = False
primaryToInitialize = "hostname1"
isPrimary = True
thisHostHasAcknowledged = False
currentPrimary = ""
acknowleged = []

print ("Starting..")
t1 = threading.Thread(target=StateThread, args=[])
t2 = threading.Thread(target=TcpProbeThread, args=[])
t1.start()
while 1:
    # keep main thread running
    sleep(10)
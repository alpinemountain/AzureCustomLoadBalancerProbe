from azure.storage.blob import BlobService
import socket
import sys
 
azureStorageAccountName = "removed"
azureStorageAccountKey = "removed"
container = "ilbcp1"
blob = "currentprimary.dat"
retryCount = 0
while 1:
    # keep main thread running
    try:
        print ("Started.")
        currentHost = socket.gethostname()
        print ("Setting as primary...")
        blob_service = BlobService(account_name=azureStorageAccountName, account_key=azureStorageAccountKey)
        newContents = currentHost
        blob_service.create_container(container)
        blob_service.put_block_blob_from_text(container, blob, newContents)
        print ("Done.")
        sys.exit()
    except Exception as e:
        print("Exception!") # e ?
        retryCount = retryCount + 1
        if retryCount>5:
            print ("Permanently failed.")
            sys.exit()
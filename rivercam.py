#!/usr/bin/python

import os
import datetime
from picamera import PiCamera
from time import sleep
from azure.storage.blob import BlobClient

# Path to temporary local image file
localpic = '/home/pi/rivercam/image.jpg'

# Take photo 
camera = PiCamera()
sleep(5)
camera.capture(localpic)

# Create the variable to use for the filename
dt = str(datetime.datetime.now())
newdt = dt.replace(":", "-")
newdt = newdt.replace(" ", "-")
newdt = newdt.replace(".", "-")
newdt = newdt[0:16]
newname = newdt+'.jpg'

# Upload to local IoT Edge Blob Service
blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=http;BlobEndpoint=http://192.168.0.201:11002/azurepistorage;AccountName=azurepistorage;AccountKey=[LOCAL-IOT-EDGE-BLOB-KEY]", container_name="pisynccontainer", blob_name=newname)

with open(localpic, "rb") as data:
    blob.upload_blob(data)

# Delete the local file now that it's been uploaded
os.remove(localpic)
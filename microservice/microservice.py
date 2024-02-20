import os
import urllib.request

import requests.exceptions
import zmq
import shutil

# URL of image to fetch - DO NOT CHANGE
URL = "https://camstills.cdn-surfline.com/wc-agatebeachor/latest_full.jpg"

# filepath where image will be saved
os.chdir("C:/Users/micha/Desktop/image-scraper/microservice/")
current_directory = os.getcwd()
image_filepath = current_directory + "/" + "agate_beach.jpg"
cached_image = current_directory + "/" + "cache.jpg"
image_to_send = image_filepath

# set up PyZMQ socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("microservice connected and ready")

while True:
    message = socket.recv()
    if message.decode() == "cam_image":
        print("microservice received request!")
        try:
            urllib.request.urlretrieve(URL, image_filepath)
            image_to_send = image_filepath
            shutil.copy(image_filepath, cached_image)
        except:
            print("There was an error! Sending cached image")
            image_to_send = cached_image
        finally:
            socket.send(image_to_send.encode())
    else:
        print(message.decode())
        print("microservice quitting!")
        socket.send(b"quitting")
        break

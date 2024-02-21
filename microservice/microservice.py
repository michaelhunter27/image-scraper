import os
import urllib.request
import zmq
import shutil
import pathlib

# URL of image to fetch
URL = "https://camstills.cdn-surfline.com/wc-agatebeachor/latest_full.jpg"

# directory where image will be saved (if different from the directory this file is in)
WORKING_DIRECTORY = "./microservice"
os.chdir(WORKING_DIRECTORY)

# filepath where downloaded image will be saved
DOWNLOAD_IMAGE_FILEPATH = "./agate_beach.jpg"

# filepath where cached image will be saved
CACHED_IMAGE_FILEPATH = "./cache.jpg"

# set up PyZMQ socket
PORT = "5555"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:" + PORT)

while True:
    message = socket.recv()
    if message.decode() == "cam_image":
        image_to_send = DOWNLOAD_IMAGE_FILEPATH
        try:
            # fetch image
            urllib.request.urlretrieve(URL, DOWNLOAD_IMAGE_FILEPATH)
            # save to cache for future use
            shutil.copy(DOWNLOAD_IMAGE_FILEPATH, CACHED_IMAGE_FILEPATH)
        except Exception as e:
            print("There was an error:", e, "\nSending cached image")
            # send cached image if there was an error
            image_to_send = CACHED_IMAGE_FILEPATH
        finally:
            f = open(image_to_send, 'rb')
            message_to_send = bytearray(f.read())
            socket.send(message_to_send)
            f.close()

            # remove downloaded image
            if os.path.isfile(DOWNLOAD_IMAGE_FILEPATH):
                pathlib.Path(DOWNLOAD_IMAGE_FILEPATH).unlink()

    elif message.decode() == "quit":
        socket.send(b"quitting")
        break

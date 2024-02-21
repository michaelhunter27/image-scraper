import os
import zmq
import subprocess

# filepath to microservice python code (relative or absolute)
MICROSERVICE_FILEPATH = "./microservice/microservice.py"

# image save location (relative filepath)
IMAGE_FILEPATH = "./agate_beach.jpg"

# starts the microservice in another process
subprocess.Popen("Python " + MICROSERVICE_FILEPATH)

# set up PyZMQ socket
PORT = "5555"
context = zmq.Context()
print("connecting to server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:" + PORT)

# Main loop
input_string = ""
while input_string != "2":
    # print menu
    print("type 1 to get an image")
    print("type 2 to exit")
    # Get user input
    input_string = input()

    if input_string == "1":
        # request image
        print("requesting image")
        socket.send(b"cam_image")

        # receive image
        image = socket.recv()
        print("image received")

        # save image to file
        f = open(IMAGE_FILEPATH, 'wb')
        bytes_to_write = bytearray(image)
        f.write(bytes_to_write)
        f.close()

        # opens image
        os.startfile("agate_beach.jpg")

# sends message to stop microservice
socket.send(b"quit")

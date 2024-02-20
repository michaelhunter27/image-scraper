import os
import zmq
import subprocess

# filepath to microservice python code
MICROSERVICE_FILEPATH = "./microservice/microservice.py"

# starts the microservice in another process
subprocess.Popen("Python " + MICROSERVICE_FILEPATH)

# set up PyZMQ socket
context = zmq.Context()
print("connecting to server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Main loop
input_string = ""
while input_string != "2":
    # print menu
    print("type 1 to get an image")
    print("type 2 to exit")
    # Get user input
    input_string = input()

    if input_string == "1":
        print("requesting image!")
        socket.send(b"cam_image")
        image = socket.recv()
        print("image received!")
        print(image.decode())
        os.startfile(image.decode())

# sends message to stop microservice
socket.send(b"quit")

from socket import *
import sys
import select

address = ('localhost', 6006)
client_socket = socket(AF_INET, SOCK_DGRAM)

#WARNING !!!! Each motor can accept values in mm, from 0 to 50

data = "0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0_" #sending one value per motors (12 motors here)
#data = "a|0.0_" # sending the same value to all
data = "s_"    # sending the stop event, for exiting the server

client_socket.sendto(data, address)

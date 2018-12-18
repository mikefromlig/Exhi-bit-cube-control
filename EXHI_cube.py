#!/usr/bin/python
#Michael ORTEGA - 08 dec 2015

from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes
import time
import sys
import socket


######################
# globals
stop        = False

# Boards
servos      = [AdvancedServo(), AdvancedServo()] # two boards for the cube
serials     = [392856, 392822]  # Boards IDs
actuators   = [8, 4] #8 motors on the first board (top and vertical edges), and 4 motors for the other board



# a socket for listening UDP messages and then update actuators
address     = ('localhost', 6006)
sock        = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)

######################
# funcs
def engage():
    """Engage the 8 actuators and set position to 0"""
    f_pos = 0 #final position

    print "\n---\nInitializing the Boards and the actuators :"

    for i in range(len(servos)):
        servos[i].openPhidget(serials[i])
        try:
            servos[i].waitForAttach(5000)
            for j in range(actuators[i]):
                servos[i].setServoType(j, ServoTypes.PHIDGET_SERVO_FIRGELLI_L12_50_100_06_R)
                servos[i].setEngaged(j, True)
            time.sleep(2)
            print "Board "+str(serials[i])+" Attached"
        except:
            print "Board "+str(serials[i])+" Not Attached !!!"
            servos[i] = None


    # Set position to 0
    for i in range(len(servos)):
        if servos[i]:
            for j in range(actuators[i]):
                servos[i].setPosition(j, f_pos)


    # Wait until position is reached
    follow = True
    while follow:
        follow = False
        for i in range(len(servos)):
            if servos[i]:
                for j in range(actuators[i]):
                    if servos[i].getPosition(j) != f_pos:
                        follow = True
        time.sleep(.1)

    print "\tDone !\n---\n"


def disengage():
    """Disengage the 8 actuators and close the board"""
    for i in range(len(servos)):
        if servos[i]:
            for j in range(actuators[i]):
                servos[i].setEngaged(j, False)
    time.sleep(2)
    for i in range(len(servos)):
        if servos[i]:
            servos[i].closePhidget()


def setPositions(p):
    """Set the position of each actuators"""

    # Set
    for i in range(len(servos)):
        if servos[i]:
            for j in range(actuators[i]):
                servos[i].setPosition(j, p[i][j])

    # Wait until position is reached
    follow = True
    while follow:
        follow = False
        for i in range(len(servos)):
            if servos[i]:
                for j in range(actuators[i]):
                    if servos[i].getPosition(j) != p[i][j]:
                        follow = True
        time.sleep(.1)
    return


#########################
# main
engage()
while (not stop):
    data, addr = sock.recvfrom(1024)
    commands = data.split("_")
    for c in commands[0:-1]:
        if c[0] == "s":
            print "Exit signal received"
            stop = True
        else:
            if c[0] == "a":
                val = c.split("|")
                res = round(float(val[1]), 1)
                if res < 0:
                    res = 0
                elif res > 50:
                    res = 50
                vals_f = [res]*12
            else:
                vals = c.split("|")
                vals_f = []
                for v in vals:
                    res = round(float(v), 1)
                    if res < 0:
                        res = 0
                    elif res > 50:
                        res = 50
                    vals_f.append(res)

            print "Setting positions :", vals_f
            setPositions([vals_f[:8], vals_f[8:]])
            print "\t Done"
disengage()

#!/usr/bin/env pybricks-micropython

from time import sleep
import random

from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.parameters import Port,Direction,Stop
from pybricks.iodevices import I2CDevice
from pybricks.ev3devices import TouchSensor,ColorSensor,UltrasonicSensor
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.ev3devices import Motor
from pixycamev3.pixy2 import Pixy2
from pybricks.parameters import Port,Stop,Color
from time import sleep
# Initialize the EV3 Brick.
ev3 = EV3Brick()
pixy2 = Pixy2(port=1, i2c_address=0x54)
us=UltrasonicSensor(Port.S2)
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)
mm=Motor(Port.C)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=155)

cs=ColorSensor(Port.S3)

y_ref=165
flag=False

SERVER = 'ev3dev'
client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)
client.connect(SERVER)


def turn(x):
    
    if x>0 and x<=72 :
        robot.turn(30)

    elif x>=73 and x<=145:
        robot.turn(15)

    elif x>=171 and x<=242 :
        robot.turn(-15)

    elif x>=243 and x<315 :
        robot.turn(-30)

def check(s):
    if s==2:
        robot.drive(-800,0)
        sleep(3)
        robot.stop()
    if cs.color() ==Color.BLUE :
        robot.drive(-800,0)
        sleep(3)
        robot.stop()
       
    if us.distance()<50:
        robot.drive(-100,0)
        sleep(0.5)
        robot.stop()
        robot.turn(90)
    
def initial_code():
    robot.drive(1000,0)
    sleep(1.1)
    robot.stop()
    mm.run_angle(1000, 37, then=Stop.BRAKE)
    mm.run_angle(1000, -37, then=Stop.BRAKE)
    robot.drive(1000,0)
    sleep(0.5)
    robot.stop()
    mm.run_angle(1000, 37, then=Stop.BRAKE)
    mm.run_angle(1000, -37, then=Stop.BRAKE)
    robot.drive(-1000,0)
    sleep(1.7)
    robot.stop()
    robot.turn(-90)
    robot.drive(1000,0)
    sleep(0.85)
    robot.stop()
    robot.turn(90)
    robot.drive(1000,0)
    sleep(0.9)
    robot.stop()
    mm.run_angle(1000, 37, then=Stop.BRAKE)
    mm.run_angle(1000, -37, then=Stop.BRAKE)
    robot.drive(1000,0)
    sleep(0.5)
    robot.stop()
    mm.run_angle(1000, 37, then=Stop.BRAKE)
    mm.run_angle(1000, -37, then=Stop.BRAKE)
        
def code():
    while 1:
        check(0)
        nr_blocks, blocks = pixy2.get_blocks(3, 1)
        # Extract data of first (and only) block
        if nr_blocks >= 1:
            x = blocks[0].x_center
            y = blocks[0].y_center
            check(blocks[0].sig)     
        else:
            x=y=0
        check(0)
        if x>0 and x<=315 and y>0 and y<=207 and blocks[0].sig==1:
            turn(x)
            check(0)
            robot.drive(800,0)
            sleep(1)
            robot.stop()
            mm.run_angle(1000, 40, then=Stop.BRAKE)
            mm.run_angle(1000, -40, then=Stop.BRAKE)

        else:
            robot.drive(-100,0)
            sleep(1)
            robot.stop()


while 1:
    if mbox.read()=='start':
        print('starting...')
    initial_code()
    code()

Илюша, [22.03.18 00:34]
#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep


sensor = UltrasonicSensor("in1")
motorLeft = LargeMotor("outA")
motorRight = LargeMotor("outB")

run = True

desiredLength = 25
speed = 350

threshold = 20
error = 0
lastError = 0
proportional = 0
integral = 0
derivative = 0

pidValue = 0

kP = 10
kI = 0.01
kD = 0.4

motorLeft.run_timed(time_sp=10000, speed_sp=(speed))
motorRight.run_timed(time_sp=10000, speed_sp=(speed))

while run:
    sensorValue = sensor.value() / 10

    error = sensorValue - desiredLength
    if abs(error) < threshold:
        integral += error
    else:
        integral = 0
    derivative = error - lastError
    lastError = error
    pidValue = error*kP + integral*kI + derivative*kD

    if pidValue > 250:
        pidValue = 250
    elif pidValue < -1 * 250:
        pidValue = -1*250

    motorRight.run_timed(time_sp=10000, speed_sp=(speed + pidValue))
    motorLeft.run_timed(time_sp=10000, speed_sp=(speed - pidValue))

motorRight.stop()
motorLeft.stop()

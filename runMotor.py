#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time
import argparse

def handleCmdArgs():
    ''' handles command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("pin_PWM", help="BCM pin number to use for speed", type=int)
    parser.add_argument("pin_dir_A", help="BCM pin number to use for direction A", type=int)
    parser.add_argument("pin_dir_B", help="BCM pin number to use for direction B", type=int)

    parser.add_argument("--waittime", help="wait time in seconds between toggle", type=int, default=2)
    parser.add_argument("--freq", help="frequency in Hz for the PWM signal", type=int, default=50)
    parser.add_argument("--speed", help="speed in percent for the PWM signal", type=int, default=75)

    args = parser.parse_args()
    return args

def setupMotorGpio( params ):
    ''' Sets parameters for the IOs

        params: an object with the following properties
        params.pin_dir_B: motor direction pin A
        params.pin_dir_A: motor direction pin b
        params.pin_PWM: pin to output PWM signals to (for speed)
        params.freq: frequency for PWM signal

        returns the motor object
    '''

    # set the pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # set pin for output
    GPIO.setup( params.pin_dir_A, GPIO.OUT )
    GPIO.setup( params.pin_dir_B, GPIO.OUT )
    GPIO.setup( params.pin_PWM, GPIO.OUT )
    motor = GPIO.PWM( params.pin_PWM, params.freq )

    return motor


def cleanupGpio():
    ''' code to ensure that the IO ports are in a good state after
        the program is run
    '''
    GPIO.cleanup()

def getDirectionBits( count ):
    ''' based on the integer given, the direction loops between left-stop-right-stop
        if direction bit differ, we rotate.

        returns an (,)-tuple
    '''
    directions = ((0,0), (0, 1), (1, 1), (1, 0))
    directionCount = len(directions)

    return directions[count%directionCount] # trick to loop through the list nomatter the "count value"

def setMotorDirection( direction, pin_dir_A, pin_dir_B ):
    ''' sets the IO pins to control motor direction
    '''
    GPIO.output( pin_dir_A, direction[0])
    GPIO.output( pin_dir_B, direction[1])

def setMotorSpeed( doIdle, speed ):
    ''' sets the motor speed by updating the IO pins.
        idle: a boolean used to stop the motor pwm output
    '''

    # we only run when supposed to
    # altenatively we will do "active breaking", ie. use energy to make the wheels not turn
    if doIdle:
        motor.stop()
    else:
        motor.start( speed )


def runMotorLoop( motor, params ):
    # loop initial values
    count = 0

    # loop forever
    while (True):
        directionBits = getDirectionBits(count)
        beIdle = (directionBits[0] == directionBits[1]) # if the same, then we want to idle

        print "%3d Turning motor %3s, direction %s"%(count, "off" if beIdle else "on", directionBits )

        setMotorDirection( directionBits, params.pin_dir_A, params.pin_dir_B )
        setMotorSpeed( beIdle, params.speed )

        time.sleep( params.waittime )
        count = count +1

def runMotor( params ):
    ''' start motor rotation. Parameter are in the "params" object
    '''

    motor = setupMotorGpio( params )

    # to catch ctrl+c in a nice way
    try:
        runMotorLoop( motor, params )
    except KeyboardInterrupt:
        print "cleanup"

    cleanupGpio()


# run if this is the "main" program (as opposed to included as module)
if __name__ == "__main__":
        config = handleCmdArgs()
        print "Using"
        print "- pwm output:", config.pin_PWM
        print "- dir output A:", config.pin_dir_A
        print "- dir output B:", config.pin_dir_B
        print "- pwm frequency:", config.freq
        print "- pwm run speed:", config.speed
        print "- run/stop wait time:", config.waittime

        runMotor( config )

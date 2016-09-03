#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time
import argparse

def handleCmdArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("pin", help="BCM pin number to read from", type=int)
    parser.add_argument("--waittime", help="wait time in seconds between toggle", type=int, default=2)

    args = parser.parse_args()
    return args

def readPin( pinNo, waitTime=2 ):
    ''' pinNo: the BCM numbered pin to use
        waitTime: the time in seconds between toggling
        '''

    # set the pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # set pin for output
    GPIO.setup( pinNo, GPIO.IN )

    # to catch ctrl+c in a nice way
    try:
        # loop initial values
        val = 1
        count = 0

        # loop forever
        while (1):

            val = GPIO.input( pinNo )
            print "%3d Read pin %d: %d"%(count, pinNo, val )
            time.sleep( waitTime )
            count = count +1

    except KeyboardInterrupt:
        print "cleanup"

    GPIO.cleanup()


# run if this is the "main" program (as opposed to included as module)
if __name__ == "__main__":
        config = handleCmdArgs()
        readPin( config.pin, config.waittime )

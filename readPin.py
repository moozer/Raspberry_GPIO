#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time
import argparse

def handleCmdArgs():
    ''' handles command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("pin", help="BCM pin number to read from", type=int)
    parser.add_argument("--waittime", help="wait time in seconds between toggle", type=int, default=2)

    args = parser.parse_args()
    return args

def setupGpio( pinNo ):
    ''' Sets parameters for the IOs
    '''

    # set the pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # set pin for output
    GPIO.setup( pinNo, GPIO.IN )

def cleanupGpio():
    ''' code to ensure that the IO ports are in a good state after
        the program is run
    '''
    GPIO.cleanup()

def printPinValueLoop( pinNo, waitTime ):
    ''' loops forever and shows current value of the input pin
    '''
    # count is a counter to make ouput look nice
    count = 0

    # loop forever
    while (True):
        val = GPIO.input( pinNo )
        print "%3d Read pin %d: %d"%(count, pinNo, val )
        time.sleep( waitTime )
        count = count +1

def readPin( pinNo, waitTime=2 ):
    ''' Reads the specified pin a given intervals and outputs
        the result on the terminal
        pinNo: the BCM numbered pin to use
        waitTime: the time in seconds between toggling
        '''

    setupGpio( pinNo )

    # to catch ctrl+c in a nice way
    try:
        printPinValueLoop( pinNo, waitTime )
    except KeyboardInterrupt:
        print "Done"

    cleanupGpio()

# run if this is the "main" program (as opposed to included as module)
if __name__ == "__main__":
        config = handleCmdArgs()
        readPin( config.pin, config.waittime )

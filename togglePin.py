# importing modules
import RPi.GPIO as GPIO
import time
import argparse

def handleCmdArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("pin", help="BCM pin number to toggle", type=int)
    parser.add_argument("--waittime", help="wait time in seconds between toggle", type=int, default=2)
    
    args = parser.parse_args()
    return args

def togglePin( pinNo, waitTime=2 ):
    ''' pinNo: the BCM numbered pin to use
        waitTime: the time in seconds between toggling
        '''
    
    # set the pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # set pin for output
    GPIO.setup( pinNo, GPIO.OUT )

    # to catch ctrl+c in a nice way
    try:
        # loop initial values
        val = 1
        Count = 0

        # loop forever
        while (1):

            print "%3d Turning pin %d on"%(count, pinNo, "on" if val else "off" )
            GPIO.output( pinNo, val)
            time.sleep( waitTime )
            val = 1 - val # toggle 0 and 1
            count = count +1 

    except:
        print "cleanup"

    GPIO.cleanup()


# run if this is the "main" program (as opposed to included as module)
if __name__ == "__main__":
        config = handleCmdArgs()
        togglePin( config.pin, config.waittime )

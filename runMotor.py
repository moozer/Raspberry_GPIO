#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time
import argparse

def handleCmdArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("pin_PWM", help="BCM pin number to use for speed", type=int)
    parser.add_argument("pin_dir_A", help="BCM pin number to use for direction A", type=int)
    parser.add_argument("pin_dir_B", help="BCM pin number to use for direction B", type=int)
    
    parser.add_argument("--waittime", help="wait time in seconds between toggle", type=int, default=2)
    parser.add_argument("--freq", help="frequency in Hz for the PWM signal", type=int, default=50)
    parser.add_argument("--speed", help="speed in percent for the PWM signal", type=int, default=75)
    
    args = parser.parse_args()
    return args

def runMotor( params ):
    ''' pinNo: the BCM numbered pin to use
        waitTime: the time in seconds between toggling
        '''
    
    # set the pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # set pin for output    
    GPIO.setup( params.pin_dir_A, GPIO.OUT )
    GPIO.setup( params.pin_dir_B, GPIO.OUT )
    GPIO.setup( params.pin_PWM, GPIO.OUT )
    motor = GPIO.PWM( params.pin_PWM, params.freq )

    # to catch ctrl+c in a nice way
    try:
        # loop initial values
        directions = ((0,0), (0, 1), (1, 1), (1, 0))
        count = 0

        # loop forever
        while (1):

            print "%3d Turning motor %3s, direction %s"%(count, "on" if count%2 else "off", directions[count%4] )

            GPIO.output( params.pin_dir_A, directions[count%4][0])
            GPIO.output( params.pin_dir_B, directions[count%4][1])
            
            if count %2:
	        motor.start( params.speed )
            else:
                motor.stop()

            time.sleep( params.waittime )
            count = count +1 

    except KeyboardInterrupt:
        print "cleanup"

    GPIO.cleanup()


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

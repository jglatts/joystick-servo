#!/usr/bin/env python
#------------------------------------------------------
#
#		This is a program for JoystickPS2 Module.
#
#		This program depend on ADC0832 ADC chip.
#               
#		Update 07/01/2018 to use servo Motor.
#	       
#
#------------------------------------------------------


import ADC0832_tmp
import RPi.GPIO as GPIO
import time
import signal
import atexit
from time import sleep

btn = 15	# Define button pin


def setup():
	""" Setup Raspberry Pi """

	ADC0832_tmp.setup()				# Setup ADC0832
	GPIO.setmode(GPIO.BOARD)	# Numbers GPIOs by physical location
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Setup button pin as input an pull it up
    	GPIO.setup(16, GPIO.OUT)	# Servo Output pin
	global state
	state = ['up', 'down', 'left', 'right']	
	p = GPIO.PWM(16, 50) # Servo PWM pin
   	p.start(7.5)


def getResult():
	"""get joystick results """

	if ADC0832_tmp.getResult1() == 0:
		return 1	#up
	if ADC0832_tmp.getResult1() == 255:
		return 2	#down
	if ADC0832_tmp.getResult() == 0:
                servoguy()	#call servo myguy
                print('Servo Running!')
		return 3	#left, and servo starts to run
	if ADC0832_tmp.getResult() == 255:
                servoguy()
                print('Servo Running!')
		return 4		#right, and servo starts to run
	if GPIO.input(btn) == 0:
		print 'Button is pressed!'		# Button pressed
		

def servoguy():
    ''' Run the Servo '''

    try:
        p.ChangeDutyCycle(1.5)
        time.sleep(.5)
        p.ChangeDutyCycle(12.5)
        time.sleep(.5)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
        print('You have cancelled the program!')
        


def loop():
	while True:
		tmp = getResult()
		if tmp != None:
			print state[tmp - 1]

def destory():
	GPIO.cleanup()		# Release resource

if __name__ == '__main__':	# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()
		print('You have cancelled the program!')

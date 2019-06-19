#https://www.youtube.com/watch?v=K-fMRIN5iSA&feature=youtu.be&fbclid=IwAR0lFnK0rxBouxxaYz5Cgz44SsTqGBOy53PYWfQqZ7t703cU-8kB27T-dhw

import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BOARD)

BTN_G = 22 # G25
BTN_R = 12 # G18
BTN_Y = 13 # G27
BTN_B = 15 # G22

LED_G = 29 # G5
LED_R = 31 # G6
LED_Y = 32 # G12
LED_B = 33 # G13

btn2led = {
	BTN_G: LED_G,
	BTN_R: LED_R,
	BTN_Y: LED_Y,
	BTN_B: LED_B,
}

GPIO.setwarnings(False)
GPIO.setup([BTN_G, BTN_R, BTN_Y, BTN_B], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup([LED_G, LED_R, LED_Y, LED_B], GPIO.OUT, initial=GPIO.HIGH)

def blink_thread(BTNcolor):
	x = GPIO.HIGH
	y = GPIO.LOW
	blink = False
	blink_delay = 0.1 # blinks

	print("Enter blinking mode")
	while True:
		if GPIO.input(BTN_G) and GPIO.input(BTN_R):
			print("G and R pushed to start blinking")
			started = time.time()
			while True:
				if GPIO.input(BTNcolor):
					GPIO.output([LED_G, LED_R, LED_Y, LED_B], True)
					print("pushed button to exit blinking mode")
					break

				if time.time() - started > 10:
					GPIO.output([LED_G, LED_R, LED_Y, LED_B], True)
					print("10 sec passed, exiting blinking mode")
					break
				GPIO.output(LED_G, x)
				GPIO.output(LED_R, y)
				if x == GPIO.LOW:
					x = GPIO.HIGH
					y = GPIO.LOW
				else:
					x = GPIO.LOW
					y = GPIO.HIGH

				time.sleep(blink_delay)
			break
	print("returning now")
	return

def handle(pin):
	GPIO.output(btn2led[pin], not GPIO.input(pin))

	t = None
	if pin == BTN_B or BTN_Y:
		if GPIO.input(BTN_B):
			print("starting b thread")
			t = threading.Thread(target=blink_thread(BTN_Y))
			t.daemon = True
			t.start()
			t.join()
			print("finished thread")
			time.sleep(0.5)

		if GPIO.input(BTN_Y):
			print("starting y thread")
			t = threading.Thread(target=blink_thread(BTN_B))
			t.daemon = True
			t.start()
			t.join()
			time.sleep(0.5)
			print("finished thread")

GPIO.add_event_detect(BTN_G, GPIO.BOTH, handle)
GPIO.add_event_detect(BTN_R, GPIO.BOTH, handle)
GPIO.add_event_detect(BTN_Y, GPIO.BOTH, handle)
GPIO.add_event_detect(BTN_B, GPIO.BOTH, handle)

# pause
while True:
	time.sleep(1e6)

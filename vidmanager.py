from omxplayer import OMXPlayer
from thread import start_new_thread
import RPi.GPIO as GPIO
import time
import schedule
import datetime
import sys
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP) #pin 11 - Play button
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP) #pin 12 - Reset Shift
GPIO.setup(27, GPIO.OUT) #pin 13 - Playing light
GPIO.setup(23, GPIO.OUT) #pin 16 - Status of system light

CNY = '/home/pi/CNY_captions.mp4'
MASON = '/home/pi/mason.mp4'
video = OMXPlayer(CNY,args=['-b'])
print "Initialized"
print datetime.datetime.now()

loopy = False


def stopListener():
	loopy = True
	GPIO.output(27, GPIO.HIGH)
	while loopy:#loop until player reaches 11 mins or both buttons are pressed then pause and reset.
		if (video.position() > (video.duration() - 2)) or (GPIO.input(18) == GPIO.LOW and GPIO.input(17) == GPIO.LOW):#11 mins OR (reset shift AND play button pressed)
			if(GPIO.input(18) == GPIO.LOW and GPIO.input(17) == GPIO.LOW):
				print "Video playback force stopped by user. " + str(datetime.datetime.now())
			else:
				print "End of playback. "  + str(datetime.datetime.now())
			video.pause()
			time.sleep(.5)
			video.set_position(0.0)
			loopy = False
			GPIO.output(27, GPIO.LOW)
		time.sleep(1)

def playVid(video_file):
	global video
	if video.playback_status() == "Paused":
		if(video_file != video.get_filename()):
			video.quit()
			video = OMXPlayer(video_file,args=['-b'])
			print video_file + "loaded"
		video.play()
		start_new_thread(stopListener, ())
		print "Playing " + video_file + " at " + str(datetime.datetime.now())
	else: #already playing, must have been forced to play
		print "Already Playing - " + str(datetime.datetime.now())

def quitForDay():
	print "Quitting for day." + str(datetime.datetime.now())
	GPIO.output(23, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)
	video.quit()
	os.system("/usr/bin/sudo /sbin/shutdown -h now")
	sys.exit()

schedule.every().day.at("10:00").do(playVid, CNY)
schedule.every().day.at("11:00").do(playVid, CNY)
schedule.every().day.at("12:00").do(playVid, MASON)
schedule.every().day.at("13:00").do(playVid, CNY)
schedule.every().day.at("14:00").do(playVid, CNY)
schedule.every().day.at("15:00").do(playVid, MASON)
schedule.every().day.at("16:00").do(playVid, CNY)

schedule.every().day.at("9:15").do(playVid, CNY)
schedule.every().day.at("10:15").do(playVid, CNY)
schedule.every().day.at("11:15").do(playVid, CNY)
#schedule.every().day.at("12:15").do(playVid, CNY)
schedule.every().day.at("13:15").do(playVid, CNY)
schedule.every().day.at("14:15").do(playVid, CNY)
schedule.every().day.at("15:15").do(playVid, CNY)
schedule.every().day.at("16:15").do(playVid, CNY)

schedule.every().day.at("9:30").do(playVid, CNY)
schedule.every().day.at("10:30").do(playVid, CNY)
schedule.every().day.at("11:30").do(playVid, CNY)
#schedule.every().day.at("12:30").do(playVid, CNY)
schedule.every().day.at("13:30").do(playVid, CNY)
schedule.every().day.at("14:30").do(playVid, CNY)
schedule.every().day.at("15:30").do(playVid, CNY)
schedule.every().day.at("16:30").do(playVid, CNY)

schedule.every().day.at("9:45").do(playVid, CNY)
schedule.every().day.at("10:45").do(playVid, CNY)
schedule.every().day.at("11:45").do(playVid, CNY)
#schedule.every().day.at("12:45").do(playVid, CNY)
schedule.every().day.at("13:45").do(playVid, CNY)
schedule.every().day.at("14:45").do(playVid, CNY)
schedule.every().day.at("15:45").do(playVid, CNY)
#schedule.every().day.at("16:45").do(playVid)

schedule.every().day.at("16:45").do(quitForDay)
GPIO.output(23, GPIO.HIGH)
GPIO.output(27, GPIO.LOW)

while True:
	schedule.run_pending()#go through scheduled events above
	if(GPIO.input(17) == GPIO.LOW and GPIO.input(18) == GPIO.HIGH):#play button pushed but no reset shift held
		time.sleep(.05)
		if(GPIO.input(17) == GPIO.LOW and GPIO.input(18) == GPIO.HIGH):#still pressed after .05 seconds. execute play function.
			playVid(CNY)
	time.sleep(.1)


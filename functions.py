import RPi.GPIO as GPIO
import time
from time import sleep
from bar import *;
from routes import *;
from models import *;


def rchoice():
	pick=[]
	for count in range(1,3):
		p=Pumps.query.get(count)
		pick.append(p.pinout)
	choice=(random.choice(pick))
        making=[choice,33.0]
	return making;


def allshots2():
        shots=set()
        allshots=[]
	shot=[]
	pump=[]
	c=PumpCount.query.get(1)
	camt=c.pump_count+1
        st=Shots.query.all()
	
        for d in st:
                shots.add(d.shot_name)
        total=len(shots)
	for s in shots:
		sk=Shots.query.filter_by(shot_name=s).all()
		iamt=len(sk)
		if iamt<camt:
			shot.append(s)
	shot.sort()
	
        for s in shot:
		sk=Shots.query.filter_by(shot_name=s).first()
		allshots.append(sk.id)
                allshots.append(sk.shot_name)
	return allshots;

def pour(making):
        #get the size of the list
        tz=len(making)
        GPIO.setmode(GPIO.BOARD)
        #to make sure the button is on (so you don't make a mess because
        #there is no glass underneath the spout)
        GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        input_value=GPIO.input(40)
        if input_value==1:
			GPIO.cleanup()
			flash("Are you sooo drunk that you forgot to put a glass? ","danger")
			flash("Place a glass down, hit the back button on your browser and try again!","warning")
                        return;

        #setme is the pump number setme+1 is the how long the pump is running
        flash("It's ready Drink Up!","info")
        for setme in range(0,tz,2):
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(int(making[setme]),GPIO.OUT)
                GPIO.output(int(making[setme]),False)
                time.sleep(making[setme+1])
                GPIO.output(int(making[setme]),True)
                GPIO.cleanup()
	return;

def caltime(amt,flow):
	#change the lenght of how long it takes your pump to pour out
	#the right amount in liquid here
	amount=10*amt*flow
	return amount;


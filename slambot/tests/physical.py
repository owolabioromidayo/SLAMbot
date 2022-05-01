import sys, os, time

from slambot.sensors.adc import ADC
from slambot.sensors.buzzer import Buzzer
from slambot.sensors.ultrasonic import Ultrasonic
from slambot.sensors.led import LED

from slambot.actuators.motor import Motor
from slambot.actuators.servo import Servo

from slambot.tracking.infrared import Line_Tracking

class TestEmulation:
    def __init__(self):
        self.run()

    def test_adc(self):
        adc = ADC()
        for i in range(3):
            print (f"The photoresistor voltage on the left is {adc.recvADC(0)}V")
            print (f"The photoresistor voltage on the right is {adc.recvADC(1)}V")
            print (f"The battery voltage is {adc.recvADC(2)}V \n")
            time.sleep(1)
          

    def test_buzzer(self):
        B = Buzzer()
        B.run('1')
        time.sleep(3)
        B.run('0')
        print("Buzzer Tests passed.")

    def test_motors(self):
        PWM = Motor()
        try:
            for fn in [PWM.goForward, PWM.goBackwards, PWM.goLeft, PWM.goRight, PWM.stop]:
                fn()
                time.sleep(1)
        except KeyboardInterrupt:
            PWM.stop()

        print("Motor Tests passed.")


    def test_servos(self):
        pwm = Servo()
        pwm.setServoPwm('0',10)
        pwm.setServoPwm('1',25)
        pwm.home()
          
        print("Servo Tests passed.")


    def test_ultrasonic(self):
        ultrasonic = Ultrasonic()
        for i in range(3):
            print(f"Obstacle distance is {ultrasonic.get_distance()}cm")
        
        print("Ultrasonic Tests passed.")


    def test_line_tracking(self):
        line = Line_Tracking()
        for i in range(3):
            L, M, R = GPIO.input(line.IR01), GPIO.input(line.IR02), GPIO.input(line.IR03)

            if [L, M, R] == [False, True, False]:
                print ('Middle')
            elif [L, M, R] == [False, False, True]:
                print ('Right')
            elif [L, M, R] == [True, False, False]:
                print ('Left')



    def test_led(self):
        led = LED("emulate")
        try:
            for i in range(3):
                print ("Chaser animation")
                led.colorWipe(led.strip, (255,0, 0))  # Red wipe
                led.colorWipe(led.strip, (0, 255, 0))  # Green wipe
                led.colorWipe(led.strip, (0, 0, 255))  # Blue wipe
                led.theaterChaseRainbow(led.strip)
                print ("Rainbow animation")
                led.rainbow(led.strip)
                led.rainbowCycle(led.strip)
                #all tuples except this one should be in form Color(0,0,255) from Adafruit
                led.colorWipe(led.strip, (0,0,0),10) 
        except KeyboardInterrupt:  
            led.colorWipe(led.strip, (0,0,0),10)




    def run(self):
        self.test_adc()
        self.test_buzzer()
        self.test_motors()
        self.test_servos()
        self.test_ultrasonic()
        self.test_led()
        self.test_line_tracking()

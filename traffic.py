import machine
from time import sleep

# Initialize LEDs and buttons
RED_LED = machine.Pin(18, machine.Pin.OUT)  # LED1 is on GP18
YELLOW_LED = machine.Pin(19, machine.Pin.OUT)  # LED2 is on GP19
GREEN_LED = machine.Pin(20, machine.Pin.OUT)  # LED3 is on GP20

LOOP_SENSOR_BUTTON = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)  
RESET_BUTTON = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)  

car_count = 0

def reset_lights():
    RED_LED.value(0)
    YELLOW_LED.value(0)
    GREEN_LED.value(0)

def check_car():
    global car_count
    if not LOOP_SENSOR_BUTTON.value():  # Button pressed (active low)
        car_count += 1
        sleep(0.2)  # Debounce

while True:
    reset_lights()
    state = "RED"
    
    while state == "RED":
        RED_LED.value(1)
        if not RESET_BUTTON.value():  # If reset button is pressed
            break
        sleep(1)  # Check every second
        if car_count > 5:  # If heavy traffic is detected
            state = "GREEN"
    
    reset_lights()
    while state == "GREEN":
        GREEN_LED.value(1)
        check_car()
        if not RESET_BUTTON.value():  # If reset button is pressed
            break
        sleep(1)  # Check every second
        if car_count > 5:  # If heavy traffic is detected
            state = "YELLOW"
    
    reset_lights()
    while state == "YELLOW":
        YELLOW_LED.value(1)
        if not RESET_BUTTON.value():  # If reset button is pressed
            break
        sleep(5)  # Stay yellow for 5 seconds
        state = "RED"
    
    car_count = 0  # Reset car count after each cycle

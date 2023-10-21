import machine
import utime
from ds3231 import DS3231  

# Initialize DS3231 RTC
i2c = machine.I2C(0)  # Create I2C instance on bus 0
rtc = DS3231(i2c)

# Initialize the button on Pin 14
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

# Function to wait for button press
def wait_for_button():
    print("Waiting for button press...")
    while button.value():
        utime.sleep_ms(10)
    print("Button pressed!")
    while not button.value():
        utime.sleep_ms(10)

# Main game loop
while True:
    print("Press the button to start counting...")
    wait_for_button()
    
    start_time = rtc.datetime()  # Get the current time from RTC
    print("Count 15 seconds in your head and press the button again...")
    wait_for_button()
    
    end_time = rtc.datetime()  # Get the current time after button press
    elapsed_time = (end_time[4]*60 + end_time[5]) - (start_time[4]*60 + start_time[5])  # Calculate elapsed time in seconds
    
    print(f"You counted {elapsed_time} seconds!")
    
    # Write to log file
    with open('log.txt', 'a') as f:
        f.write(f"{elapsed_time}\n")
    
    # Ask user if they want to play again
    choice = input("Do you want to play again? (yes/no): ")
    if choice.lower() != 'yes':
        break

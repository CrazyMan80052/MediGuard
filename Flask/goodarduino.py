import serial
from datetime import datetime
import time
import threading

# Connect to Arduino
arduino = serial.Serial('COM17', 9600)  # Adjust the port for your system
time.sleep(2)  # Wait for connection

scheduled_times ="8:10 PM"  # Set time patients_data["1"]["schedule"][]["time"]

def run_scheduler():
    while True:
        # Get current time in AM/PM format
        now = datetime.now().strftime("%I:%M %p")  
        
        # Convert both current time and scheduled time to datetime objects for proper comparison
        now_time = datetime.strptime(now, "%I:%M %p")
        scheduled_time = datetime.strptime(scheduled_times, "%I:%M %p")
        # for drug in patients_data["1"]["schedule"]:
        #     if now >= drug["time"]:  # If it's time or past it
        #         print("Turning on LED...")
        #         arduino.write(b'LED ON\n')  # Send command to Arduino
        #         break  # Stop checking time
        if now_time >= scheduled_time:  # If it's time or past it
            print("Turning on LED...")
            arduino.write(b'LED ON\n')  # Send command to Arduino
            break  # Stop checking time

        time.sleep(30)  # Check every 30 seconds
run_scheduler()
# Start background thread
#threading.Thread(target=run_scheduler, daemon=True).start()
import network
import socket
import time
import select  # Import select module for checking if data is available
#from voltage import voltage_calculation  # Import voltage calculation
from machine import Pin
from time import sleep
#from voltage_measurement import get_voltage
#from wall_fol import wall_follow, motor_stop
#from Sumo_version2 import follow_line_and_detect
# Wi-Fi credentials
ssid = "ARRIS-24D6_EXT"
password = "tHc3GuTq7rPT"
#ssid = "ITEK 2nd"
#password = "2nd_Semester_E24a"

pin = Pin("LED", Pin.OUT)

# Connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print(f"Connected to Wi-Fi. IP address: {wlan.ifconfig()[0]}")


# Call the function to connect to Wi-Fi
print("Connect to wifi")
connect_to_wifi()
print("Connected")
# UDP server setup
port = 5005
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind(("", port))
UDPServerSocket.setblocking(False)  # Non-blocking mode

print("UDP server listening on port", port)


def get_message():
    try:
        # Use select to check if data is available to be read
        ready = select.select([UDPServerSocket], [], [], 0.1)  # 100ms timeout
        if ready[0]:
            message, address = UDPServerSocket.recvfrom(1024)
            print(f"Message received from {address}: {message.decode()}")
            return message.decode(), address
        else:
            return None, None
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None, None


while True:
    
    message, address = get_message()

    if message:
        print(f"Received message: {message} from {address}")
        #if message == 'voltage':
         #   pin.off()
          #  voltage = voltage_calculation()
           # UDPServerSocket.sendto(str(voltage).encode(), address)
            #print(f"Sent voltage: {voltage} V to {address}")

        if message == 'on':
            
            pin.on()
            sleep(5)
        elif message == 'off':
            
            pin.off()
            sleep(5)
        elif message=='volt':
            get_voltage()
        
        elif message == 'wall':
            wall_follow ()
            print ("test")
        elif message == 'sumo':
            
            follow_line_and_detect ()
        
        elif message == 'stop':
            
            motor_stop ()    
        
        else:
            UDPServerSocket.sendto(b'Invalid command', address)

    time.sleep(0.1)



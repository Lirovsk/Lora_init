import time
import spidev
import RPi.GPIO as GPIO
import radio

# Pin definitions
CS_PIN = 8      # NSS
DIO0_PIN = 4    # GPIO4
SCK_PIN = 11    # GPIO11
MISO_PIN = 9    # GPIO9
MOSI_PIN = 10   # GPIO10
RESET_PIN = 22  # NRESET

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.setup(RESET_PIN, GPIO.OUT)

# Initialize LoRa module
def lora_init():
    GPIO.output(CS_PIN, GPIO.HIGH)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.1)

    # Create a LoRa radio instance
    rfm9x = radio.RFM9x(spi, CS_PIN, RESET_PIN, 915.0)

    # Configure LoRa module settings
    rfm9x.tx_power = 23
    # More settings can be configured here as needed

if __name__ == "__main__":
    try:
        lora_init()
        print("LoRa module initialized successfully.")
        while True:
            packet_size = rfm9x.receive()
            if packet_size:
                onReceive(packet_size)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

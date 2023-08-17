import time
import spidev
import RPi.GPIO as GPIO
from sx127x import SX127x

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
    rfm9x = SX127x(spi=spidev.SpiDev(), reset=RESET_PIN, cs=CS_PIN, irq=DIO0_PIN, lora_frequency=915.0)

if __name__ == "__main__":
    try:
        lora_init()
        print("LoRa module initialized successfully.")
        while True:
            rfm9x.set_mode(rfm9x.MODE_RX_CONTINUOUS)  # Start continuous reception
            while True:
                if rfm9x.get_irq_flags().rx_done:
                    packet = rfm9x.read_payload()
                    onReceive(len(packet), packet)
                time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()

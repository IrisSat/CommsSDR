"""
Example project to send data each second to a FSK modulator listening on port 12345
"""
import socket
from time import sleep

from ax25_framer import AX25Framer

TRANSMITTER_URL = "127.0.0.1"
TRANSMITTER_PORT = 50248

if __name__ == '__main__':

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            data = "Hello world :)"

            ax25_frame = AX25Framer(to_call="TOCALL", to_ssid=0,
                                    from_call="FROM", from_ssid=0,
                                    payload=data.encode("ISO-8859-1"))

            sock.sendto(ax25_frame.get_pdu(), (TRANSMITTER_URL, TRANSMITTER_PORT))

            print("Sending PDU...")
            sleep(1)  # Can be a lot faster too!


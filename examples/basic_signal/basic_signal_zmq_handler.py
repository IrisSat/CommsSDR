"""
Simple ZMQ Handler to print out incoming PDUs from decoded satellite signals
"""
import zmq
from zmq import Socket


def connect_to_gnuradio() -> Socket:
    """
    Creates the ZMQ socket to the decoded data stream
    """
    context = zmq.Context()
    zmq_socket = context.socket(zmq.SUB)
    zmq_socket.connect("tcp://0.0.0.0:50252")
    zmq_socket.subscribe("")

    return zmq_socket


if __name__ == '__main__':
    zmq_socket = connect_to_gnuradio()

    while True:
        data = zmq_socket.recv()

        print(f"Received data: {data}")

        # You can handle data in which ever way you want

        # Combine frames to an image, insert to database, etc...

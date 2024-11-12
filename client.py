import socket
import sys

class Client:
    # Initialize the client
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(TIMEOUT)
        self.seq_num = 0 

    # Send data to the server
    def send_data(self):
        while True:
            # Get user input
            input_string = input("Enter message: ")
            if not input_string:
                break

            # Send each character in the input string
            for char in input_string:
                message = "DATA {} {}\n".format(self.seq_num, char)
                while True:
                    self.sock.sendto(message.encode(), SERVER_ADDRESS)
                    print("send: {}\n".format(message))
                    
                    # Wait for ACK
                    try:
                        ack, _ = self.sock.recvfrom(1024)
                        ack_num = int(ack.decode().split()[1])
                        print("recv: ACK {}\n".format(ack_num))

                        if ack_num == self.seq_num:
                            self.seq_num = (self.seq_num + 1) % MAX_SEQUENCE_NUMBER
                            break

                    # Resend message if timeout occurs
                    except socket.timeout:
                        print("Timeout, resending: {}\n".format(message))

if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python3 client.py <server-name> <port#> <MAXSEQ#>")
        sys.exit(1)

    SERVER_NAME = sys.argv[1]
    PORT = int(sys.argv[2])
    MAX_SEQUENCE_NUMBER = int(sys.argv[3])
    SERVER_ADDRESS = (SERVER_NAME + '.utdallas.edu', PORT)
    TIMEOUT = 5 

    # Start the client
    client = Client()
    client.send_data()

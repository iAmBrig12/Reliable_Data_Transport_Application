import socket
import threading
import sys

class Server:
    # Initialize the server
    def __init__(self, port, max_seq_num):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port)) 
        self.clients = {}
        self.max_seq_num = max_seq_num

    # Handle the client's message
    def handle_client(self, data, client_address):
        # Initialize the expected sequence number for the new client if not already
        if client_address not in self.clients:
            self.clients[client_address] = 0
        
        # Parse the message
        message_parts = data.decode().split()
        msg_type, seq_num, char = message_parts[0], int(message_parts[1]), message_parts[2]
        
        # Validate DATA message and sequence number
        if msg_type == "DATA" and seq_num == self.clients[client_address]:
            print("recv: {} {} {}\n".format(msg_type, seq_num, char))
            self.clients[client_address] = (self.clients[client_address] + 1) % self.max_seq_num
            ack_message = "ACK {}\n".format(seq_num)
        else:
            # Send a duplicate ACK if sequence number is unexpected
            ack_message = "ACK {}\n".format((self.clients[client_address] - 1) % self.max_seq_num)

        # Send the ACK back to the client
        self.sock.sendto(ack_message.encode(), client_address)
        print("send: {}\n".format(ack_message))

    # Start the server and listen for clients
    def start_server(self):
        print("Server started and listening for clients...\n" + "-"*40)
        while True:
            data, client_address = self.sock.recvfrom(1024)
            # Handle each client in a new thread
            threading.Thread(target=self.handle_client, args=(data, client_address)).start()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <port> <MAXSEQ#>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    max_seq_num = int(sys.argv[2])
    
    server = Server(port, max_seq_num)
    server.start_server()

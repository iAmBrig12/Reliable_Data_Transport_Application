# RDT Project

This project consists of a UDP server and client that communicate using a simple protocol with sequence numbers and acknowledgments.

## Running the Server

To run the server, use the following command:

python3 server.py <port#> <MAXSEQ#>


## Running the Client

python3 client.py <server-name> <port#> <MAXSEQ#>

## Example 
python3 server.py 1234 2

python3 client.py net01 1234 2

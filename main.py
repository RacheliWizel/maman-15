import os
import helper
import selectors
import socket
from request import Request

HOST = ""

sel = selectors.DefaultSelector() # Create a selector object for multiplexing I/O events

def accept(sock, mask):
     conn, addr = sock.accept() # Accept incoming connection
     print('accepted', conn, 'from', addr) # Log that a new connection has been accepted
     conn.setblocking(False) # Set the connection to non-blocking mode
     sel.register(conn, selectors.EVENT_READ, read) # Register the connection with the selector and specify the callback function

def read(conn, mask):
    data = conn.recv(1024) # Read incoming data from the client
    if data: # If data was successfully read
         print('echoing', repr(data), 'to', conn) # Log that the data is being echoed back to the client
         request = Request(data) # Create a new Request object, passing in the incoming data
         response = request.handel_request() # Handle the incoming request and generate a response
         if response != 'no message': # If there is a response to send back
            conn.sendall(response) # Send the response back to the client
    else: # If no data was read (e.g. the client closed the connection)
         print('closing', conn ) # Log that the connection is closing
         sel.unregister(conn) # Unregister the connection from the selector
         conn.close() # Close the connection

def main():
    port = helper.get_port() # Get the port number to use from the helper module
    helper.create_files_folder() # Create the folder for storing uploaded files, using the helper module
    helper.init_data_base() # Initialize the database, using the helper module
    sock = socket.socket() # Create a new socket object
    sock.bind((HOST, port)) # Bind the socket to the host and port
    sock.listen(100) # Listen for incoming connections
    sock.setblocking(False) # Set the socket to non-blocking mode
    sel.register(sock, selectors.EVENT_READ, accept) # Register the socket with the selector and specify the callback function
    while True: # Loop indefinitely
        events = sel.select() # Wait for I/O events
        for key, mask in events: # For each I/O event
            callback = key.data # Get the callback function associated with the event
            callback(key.fileobj, mask) # Call the callback function with the relevant arguments



if __name__ == '__main__':
    main()

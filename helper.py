import os
import sqlite3
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import hashlib
import pycksum

# Function to get the port number
def get_port():
    # Check if the file port.info.txt exists
    if not os.path.isfile("port.info.txt"):
        print("WORN: FILE PORT.INFO DOESN'T EXIST")
        port = "1234"
    else:
        # Read the port number from port.info.txt
        with open("port.info.txt", 'r') as f:
            port = f.read()
            f.close()
    return port

# Function to create the files folder
def create_files_folder():
    # Check if the folder files exists
    if not os.path.exists("./files"):
        # Create the folder files
        os.makedirs("./files")

# Function to initialize the database
def init_data_base():
    # Connect to the database server.db
    conn = sqlite3.connect("server.db")
    # If the database doesn't exist, create it
    if conn == None:
        print("new server.db created")
        # Create the clients and files tables
        conn.executescript("""CREATE TABLE clients
        (ID INT PRIMARY KEY NOT NULL,
         Name VARCHAR(255),
         PublicKey VARCHAR(160),
         LastSeen VARCHAR(255),
         AES INT)""")
        conn.executescript("""CREATE TABLE files
         PRIMARY KEY (FileName VARCHAR(255),
         PathName VARCHAR(255)),
         Verified BOOL)""")
    else:
        # If the database exists, load the data
        print("reload data base")#todo how to load data
    # Close the connection to the database
    conn.close()

# Function to execute a query on the database
def execute_query(query):
    # Connect to the database server.db
    conn = sqlite3.connect("server.db")
    # Create a cursor object
    cur = conn.cursor()
    # Execute the query
    cur.execute(query)
    # Get all the results
    all = cur.fetchall()
    # Commit the changes to the database
    conn.commit()
    # Close the connection to the database
    conn.close()
    # Return the results
    return all

# Function to create an AES key and encrypt it using the user's public key
def create_AES_key(user_public_key):
    # Generate a random 128-bit AES key
    aes_key = get_random_bytes(128)
    # Import the user's public key
    public_key = RSA.import_key(user_public_key)
    # Create an RSA cipher object
    cipher_rsa = PKCS1_OAEP.new(public_key)
    # Encrypt the AES key using the RSA cipher
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    # Return both the AES key and the encrypted AES key
    return aes_key, encrypted_aes_key

# Function to decrypt a file using an AES key
def decrypet_file(file_content, AES_key):
    # Create an RSA cipher object with the AES key
    cipher = PKCS1_OAEP.new(AES_key)
    # Decrypt the file content using the RSA cipher
    file_decrypted_content = cipher.decrypt(file_content)
    # Convert the decrypted content to a string
    return (file_decrypted_content.decode("utf-8"))

def check_file_sum(file_decrypted_content):
    ck = pycksum.cksum(file_decrypted_content)
    return ck















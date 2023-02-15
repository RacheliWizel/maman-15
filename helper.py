import os
import sqlite3
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

def get_port():
    if not os.path.isfile("port.info.txt"):
        print("WORN: FILE POTR.INFO DOESN'T EXIST")
        port = "1234"
    else:
        with open("port.info.txt", 'r') as f:
            port = f.read()
            f.close()
    return port

def init_data_base():
    conn = sqlite3.connect("server.db")
    if conn == None:
        print("new server.db created")
        conn.executescript("""CREATE TABLE clients
        (ID INT PRIMARY KEY NOT NULL,
         Name VARCHAR(255),
         PublicKey VARCHAR(160),
         LastSeen DATE-TIME,
         AES INT)""")
        conn.executescript("""CREATE TABLE files
        (ID INT PRIMARY KEY NOT NULL,
         FileName VARCHAR(255),
         PathName VARCHAR(255),
         Verified BOOL)""")
    else:
        print("reload data base")#todo how to load data
    conn.close()

def execute_query(query):
    conn = sqlite3.connect("server.db")
    cur = conn.cursor()
    cur.execute(query)
    all = cur.fetchall()
    conn.commit()
    conn.close()
    return all

def create_AES_key(user_public_key):
    aes_key = get_random_bytes(32)
    public_key = RSA.import_key(user_public_key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return encrypted_aes_key













import os
import sqlite3
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import hashlib

def get_port():
    if not os.path.isfile("port.info.txt"):
        print("WORN: FILE PORT.INFO DOESN'T EXIST")
        port = "1234"
    else:
        with open("port.info.txt", 'r') as f:
            port = f.read()
            f.close()
    return port

def create_files_folder():
    if not os.path.exists("./files"):
        os.makedirs("./files")

def init_data_base():
    conn = sqlite3.connect("server.db")
    if conn == None:
        print("new server.db created")
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
    aes_key = get_random_bytes(128)
    public_key = RSA.import_key(user_public_key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return aes_key, encrypted_aes_key

def decrypet_file(file_content, AES_key):
    cipher = PKCS1_OAEP.new(AES_key)
    file_decrypted_content = cipher.decrypt(file_content)
    return (file_decrypted_content.decode("utf-8"))

def check_file_sum(file_decrypted_content):
    m = hashlib.md5() # todo change func to a working one
    m.update(file_decrypted_content)
    return m.hexdigest()















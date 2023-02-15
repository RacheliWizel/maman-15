import sqlite3
import datetime

conn = sqlite3.connect("server.db")
# conn.executescript("""CREATE TABLE clients
#        (ID INT PRIMARY KEY NOT NULL,
#         Name VARCHAR(255),
#         PublicKey VARCHAR(255),
#         LastSeen DATETIME,
#         AES INT)""")
# conn.executescript("""CREATE TABLE files
#        (ID INT PRIMARY KEY NOT NULL,
#         FileName VARCHAR(255),
#         PathName VARCHAR(255),
#         Verified BOOL)""")
# time_now = datetime.date.today()
# conn.execute("""INSERT INTO clients VALUES (16,"as","15",14/02/2023,14) """)
# conn.execute("""INSERT INTO clients VALUES (15,"as","15",14/02/2023,14)""")
# conn.execute("""INSERT INTO clients VALUES (12,"as","15",14/02/2023,14) """)
cur = conn.cursor()
cur.execute("SELECT AES, PublicKey, Name FROM clients WHERE ID = 16")
all = cur.fetchall()
conn.commit()
print(all)

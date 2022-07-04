import socket, threading, pickle, linecache, os.path
from sqlalchemy import insert, create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

from mainwebsite.datamodels import *

HEADER = 64
PORT = 6464
SERVER = linecache.getline('monitoring.txt', 5).rstrip('\n')
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

# AF_INET = IPv4, SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Connecting to the DB
DB_NAME = "customers.db"
dbPath = '../customers.db'
print(os.path.exists(dbPath))
engine = create_engine('sqlite:///%s' % dbPath, echo=True)

metadata = MetaData(engine)

session = scoped_session(sessionmaker(bind=engine))

res = session.query(User).all()

print(res)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        data = conn.recv(4096)
        data_variable = pickle.loads(data)
        print(data_variable)

        new_data = Clients_data(hostname=data_variable["hostname"],
                                os=data_variable["os"],
                                boot_time=data_variable["boot_time"],
                                cpu_percent=data_variable["cpu_percent"],
                                memory_percent=data_variable["memory_percent"],
                                virtual_mem=data_variable["virtual_mem"],
                                avg_load=data_variable["avg_load"],
                                server_ip=data_variable["ip"],
                                timestamp=data_variable["timestamp"])
        session.add(new_data)
        session.commit()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()

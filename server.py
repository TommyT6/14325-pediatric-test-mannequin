import socket
import threading
import time
import pandas as pd
import datetime
import numpy as np

#Change this to number of Picos the server should be connected to
numOfPicos = 4
picoCount = 0
#Change this for max size of messages in bytes
buffSize = 255

def main():
    global picoCount
    #create server side socket
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #server.setblocking(False)
    host = socket.gethostname()
    port = 5000
    print("Server started")
    print("Now looking for Picos")


    #establish connection between all clients
    server.bind((host,port))

    #specify max num of picos to connect to and start accepting connections
    server.listen(numOfPicos) 

    #Start accepting any connections we find
    while True:
        try:
            c, addr = server.accept()
        except:
            time.sleep(0.5)
            continue
        t = threading.Thread(target=receive_data,args=(c,addr), daemon=True)
        t.start()
        print("Connected to a Pico")
        picoCount +=1
        print("Number of Picos Connected: ", picoCount)


#threads that look for messages from clients
#currently only saves data to a csv once connection to stream is broken, can add keyboard or some other way to save 
#also only works for a bno data, will need a way to identify which data to save!
def receive_data(clientsocket,addr):
    close = 0
    bno_df = pd.DataFrame(columns = ['Time','BNO1_Accel','BNO1_Gyro', 'BNO1_Euler','BNO2_Accel','BNO2_Gyro','BNO2_Euler'])
    while True:
        try:
            data = clientsocket.recv(buffSize)
        except Exception as e:
            print(e)
            continue
        data = data.decode('utf-8')
        #check if data is valid if not skip
        if data != str(): #if valid
            now = datetime.now()
            #process_data(addr, data)
            bno_df = record_data(bno_df,data,now)
            print("Pico from ", clientsocket.getpeername()[0], "is sending ", data)
        else:
            #only if connection is broken
            break

    print("Socket from ",str(addr), "closed")
    bno_df.to_csv("Data/bno.csv")
    clientsocket.close()

#preprocessing data function needs heavy work, need to figure out type of preprocessing to be done first
def process_data(addr, data):
    if addr == ('172.16.150.144', 62132): #acceleration
        print("Acceleration = ", data)
    elif addr == 2: #angular velocity
        print("Angular Veloctiy = ", data)
    elif addr == 3: #absolute orientation
        print("Absolute Orientation = ", data)
    elif addr == 4: #FSRs
        print("FSR = ", data)
    elif addr == 5: #Force Scale
        print('Force Scale = ', data)
    else:
        print("Pico from ", addr, " has sent has an invalid classifier, please check the data being sent")
    print(data)

logger = logging.getLogger(__name__)
def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        logger.exception("unexpected exception when checking if a socket is closed")
        return False
    return False


def record_data(df,data,time):
    #need to add if else statements figuring out which data is which
    #currently this only supports 1 BNO streaming data
    accel = float(data[1])
    gyro = float(data[2])
    euler = float(data[3])
    if data[0] == "1":
        df.loc[len(df.index)] = [time,accel,gyro,euler,np.nan,np.nan,np.nan] 
    elif data[0] == "2":
        df.loc[len(df.index)] = [time,np.nan,np.nan,np.nan,accel,gyro,euler] 
    return df

main()

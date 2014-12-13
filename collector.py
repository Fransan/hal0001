import socket
import psycopg2
import time
import json


class Collector(object):
    """docstring for Collector"""
    def __init__(self):
        super(Collector, self).__init__()
        self.HOST = ''
        self.PORT = 8448  
        self.initSocket()
		
    def initSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def start(self):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        while 1:
            self.data = self.conn.recv(1024)
            if not self.data: break
            print self.addr
            print self.data
            self.readData()
            self.insertData()
        self.conn.close()
    
    def readData(self):
        self.data = self.data.split(',')

    def insertData(self):
        if self.data[2] :
            dataQuery = "INSERT INTO sensors_sensordata (sensor_id_id, value, timestamp) VALUES (%s, %s, %s);"
            conn = psycopg2.connect("dbname=hal user=hal password=hal")
            cur = conn.cursor()
            cur.execute(dataQuery, (self.data[0], self.data[2], time.time()))
            conn.commit()
            cur.close()
            conn.close()

if __name__ == "__main__" :
    tempCollector = Collector()
    tempCollector.start()
    time.sleep(1)
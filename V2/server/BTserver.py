import bluetooth
import threading
from uuid import uuid4
from time import sleep


class BTserver(threading.Thread):
    def __init__(self,uuid = "00000000-0000-0000-0000-000000000000", name = "Bluetooth server"):
        threading.Thread.__init__(self)
        self.name = name
        self.uuid = uuid
        self.socket = None
        self.target_socket = None
        self.target_address = None
        self.running = False

    def run(self):
        self.set_uuid()
        self.start_socket()
        self.advertise_service()
        self.running = True
        while self.running:
            if not self.connected():
                self.target_socket, self.target_address = self.socket.accept()
            else:
                sleep(1)


    def stop(self):
        self.running = False

    def start_socket(self,socket_type = bluetooth.RFCOMM):
        self.socket = bluetooth.BluetoothSocket(socket_type)
        self.socket.bind(("",0))
        self.socket.listen(1)

    def advertise_service(self):
        bluetooth.advertise_service(self.socket,self.name,self.uuid)

    def get_uuid(self):
        return self.uuid

    def set_uuid(self,uuid = "00000000-0000-0000-0000-000000000000"):
        self.uuid = uuid

    def send_data(self,data):
        print "sending data:",data
        try:
            self.target_socket.send(data)
        except bluetooth.BluetoothError:
            print "bluetooth error while sending"
            #pass

    def connected(self):
        if self.target_socket is None:
            return False
        try:
            self.target_socket.getpeername()
            return True
        except bluetooth.BluetoothError:
            return False

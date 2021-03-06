import bluetooth
from threading import Thread
from random import random
from time import sleep


class BtServer(Thread):

    class State:
        stop = 0
        starting = 1
        listening = 2
        connected = 3
        stopping = 4

    def __init__(self):
        Thread.__init__(self)
        self.name = "BtServer"

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.port = 0

        self.client_sock = None

        self.buff = []

        self.state = self.State.stop

    def run(self):
        self.state = self.State.starting
        self.server_sock.bind(("", self.port))
        self.state = self.State.listening
        self.server_sock.listen(1)
        print("listening on port %d" % self.port)
        uuid = "5d6101f4-3c07-4c0e-b9c2-39e1df5690cc"
        bluetooth.advertise_service(self.server_sock, self.name, uuid)
        self.client_sock, address = self.server_sock.accept()
        #self.client_sock.settimeout(10)
        self.state = self.State.connected
        print("Accepted connection from ", address)
        while 0 < self.state < self.State.stopping:
            while len(self.buff) > 0:
                success = self.send_data(self.buff[0])
                if success:
                    self.buff.pop()
        self.state = self.State.stop
        print("Connection lost")

    def stop(self):
        self.state = self.State.stopping
        if self.client_sock is not None:
            self.client_sock.close()
        if self.server_sock is not None:
            self.server_sock.close()
        self.state = self.State.stop

    def send_data(self, data):
        if not self.is_connected():
            return False
        try:
            packet = '['+data+']'
            self.client_sock.sendall(packet)
            return True
        except bluetooth.BluetoothError:
            return False

    def queue_data(self, data):
        if len(self.buff) >= 50:
            return False
        self.buff.append(data)
        return True

    def queue_full(self):
        return len(self.buff) >= 50

    def is_connected(self):
        return self.state == self.State.connected


if __name__ == "__main__":
    server = BtServer()
    server.daemon = True
    server.start()
    sleep(0.1)
    try:
        while True:
            # print "Loop"
            if server.State.stop < server.state:
                if not server.is_connected():
                    sleep(0.1)
                else:
                    data = str(random())
                    print(server.state,data)
                    completed = server.send_data(data)
                    if not completed:
                        server.stop()
            else:
                print("Restarting")
                del server
                server = BtServer()
                server.daemon = True
                server.start()
                sleep(0.1)

    except KeyboardInterrupt:
        pass
    if server is not None:
        server.stop()
        server.join()
    print("Server stopped")

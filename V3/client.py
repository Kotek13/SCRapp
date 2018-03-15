import bluetooth
from threading import Thread
from time import sleep


class BtClient(Thread):

    class State:
        stop = 0
        searching = 1
        connecting = 2
        connected = 3
        stopping = 4

    def __init__(self):
        Thread.__init__(self)
        self.uuid = "5d6101f4-3c07-4c0e-b9c2-39e1df5690cc"
        self.name = "BtClient"
        self.state = self.State.stop
        self.buff = []
        self.sock = None

    def run(self):
        self.state = self.State.searching
        service_matches = []
        while len(service_matches) == 0:
            service_matches = bluetooth.find_service(uuid=self.uuid)

        # TODO selecting devices
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]
        self.state = self.State.connecting
        print "connecting to \"%s\" on %s" % (name, host)
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((host, port))
        self.state = self.State.connected
        try:
            while 0 < self.state < self.State.stopping:
                _data = self.sock.recv(1024)
                self.buff.append(_data)
        except bluetooth.BluetoothError:
            pass
        self.stop()

    def stop(self):
        self.state = self.State.stopping
        if self.sock is not None:
            self.sock.close()
            del self.sock
            self.sock = None
        self.state = self.State.stop

    def get_data(self):
        if len(self.buff) == 0:
            return None
        return self.buff.pop()

    def is_connected(self):
        return self.state == self.State.connected


if __name__ == "__main__":
    client = BtClient()
    client.daemon = True
    client.start()
    try:
        while client.isAlive():
            while not client.is_connected():
                sleep(0.1)
            data = client.get_data()
            if data is not None:
                print data
    except KeyboardInterrupt:
        pass
    client.stop()

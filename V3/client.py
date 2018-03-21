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
        self.buff = ""
        self.host_port = None
        self.host_name = None
        self.host_address = None
        self.host_protocol = None
        self.sock = None
        self.buff_max_size = 1024*10
        self.packets = []
        self.tmp_packet = ""

    def run(self):
        self.state = self.State.searching
        service_matches = []
        while len(service_matches) == 0:
            service_matches = bluetooth.find_service(uuid=self.uuid)

        # TODO selecting devices
        first_match = service_matches[0]
        self.host_port = first_match["port"]
        self.host_name = first_match["name"]
        self.host_address = first_match["host"]
        self.host_protocol = first_match["protocol"]
        self.state = self.State.connecting
        print "connecting to \"%s\" on %s" % (self.host_name, self.host_address)
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.host_address, self.host_port))
        self.state = self.State.connected
        try:
            while 0 < self.state < self.State.stopping\
                    and len(self.buff) <= self.buff_max_size:
                _data = self.sock.recv(1024)
                self.buff += _data
                self.packet_creator()
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

    def packet_creator(self):
        start = self.buff.find('[')
        end = self.buff.find(']')
        while len(self.buff) > 0 and start != -1 and end != -1:
            if end<start:
                self.packets.append(self.buff[:end-1])
                self.buff = self.buff[end+1:]
            else:
                self.packets.append(self.buff[start+1:end-1])
                self.buff = self.buff[end + 1:]

    def get_data(self):
        if len(self.packets) == 0:
            return None
        else:
            return self.packets.pop()

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

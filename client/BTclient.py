import bluetooth
import threading
from time import sleep
from Queue import Queue


class BTsearcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.services = []
        self.running = False
        self.service_uuid = "00000000-0000-0000-0000-000000000000"

    def run(self):
        self.running = True
        while self.running:
            print "searching"
            services = bluetooth.find_service()
            print "found", len(services), "services"
            for device in services:
                if device not in self.services:
                    self.services.append(device)
        self.running = False

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def get_services(self):
        return self.services

    def set_uuid(self, uuid):
        self.service_uuid = uuid

    def get_uuid(self):
        return self.service_uuid

class BTreciever(threading.Thread):
    def __init__(self, name="BTreciever"):
        threading.Thread.__init__(self)
        self.name = name

        self.running = False

        self.socket = None
        self.target_address = None
        self.target_port = None
        self.target_protocol = None

        self.buff = Queue(50)

    def run(self):
        self.running = True
        while self.running:
            if self.connected():
                data = self.socket.recv(1024)
                self.buff.put(data)
        self.running = False

    def stop(self):
        self.running = False
        if self.connected():
            self.socket.shutdown(2)
            self.socket.close()

    def connect(self, target_address, target_port,
                target_protocol):
        self.target_address = target_address
        self.target_port = target_port
        self.target_protocol = target_protocol
        self.socket = bluetooth.BluetoothSocket(target_protocol)
        self.socket.connect((self.target_address,self.target_port))
        self.socket.settimeout(5)

    def is_running(self):
        return self.running

    def connected(self):
        if self.socket is None:
            return False
        try:
            self.socket.getpeername()
            return True
        except bluetooth.BluetoothError:
            return False

    def getData(self):
        if self.buff.empty():
            return None
        return self.buff.get()




class BTclient(threading.Thread):
    def __init__(self,
                 name="BTclient"):
        threading.Thread.__init__(self)
        self.name = name


        self.BTsearcher = BTsearcher()
        self.BTsearcher.daemon = True

        self.BTreciever = BTreciever()
        self.BTreciever.daemon = True

        self.search_for_devices = False
        self.search_started = False
        self.running = False



    def run(self):
        #print "client started"
        self.running = True
        while self.running:
            if self.search_for_devices and not self.BTsearcher.is_running() and not self.search_started:
                self.search_started = True
                #print "starting BT searcher"
                self.BTsearcher.start()
            elif not self.search_for_devices and self.BTsearcher.is_running():
                #print "stopping BT searcher"
                self.search_started = False
                self.BTsearcher.stop()
            elif self.search_for_devices and self.search_started:
                sleep(0.2)

    def stop(self):
        self.BTsearcher.stop()
        self.BTreciever.stop()
        self.search_for_devices = False
        self.running = False

    def join(self, timeout=None):
        self.BTsearcher.join(timeout)
        self.BTreciever.join(timeout)
        threading.Thread.join(self,timeout)

    def search(self):
        #print "search started"
        self.search_for_devices = True

    def stop_search(self):
        self.search_for_devices = False
        self.BTsearcher.stop()

    def get_services(self):
        return self.BTsearcher.get_services()

    def get_data(self):
        return self.BTreciever.getData()

    def set_uuid(self,uuid):
        self.BTsearcher.set_uuid(uuid)

    def connect(self,address,port,protocol):
        self.BTreciever.connect(address,port,protocol)
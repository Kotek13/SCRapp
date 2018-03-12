import bluetooth
import threading
from uuid import uuid4
from time import sleep


class BTsearcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.devices = {}
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            print "searching"
            devices = bluetooth.discover_devices(duration=5,lookup_names=True)
            for device in devices:
                address = device[0]
                name = device[1]
                if not self.devices.has_key(address):
                    self.devices[address] = name
        self.running = False

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def get_devices(self):
        return self.devices

    def get_device(self, address):
        return self.devices[address]

class BTclient(threading.Thread):
    def __init__(self,
                 uuid="00000000-0000-0000-0000-000000000000",
                 name="BTclient"):
        threading.Thread.__init__(self)
        self.name = name

        self.socket = None
        self.target_address = None
        self.target_port = None
        self.target_protocol = None
        self.target_uuid = uuid

        self.BTsearcher = BTsearcher()
        self.BTsearcher.daemon = True

        self.search_for_devices = False
        self.search_started = False
        self.running = False

    def run(self):
        print "client started"
        self.running = True
        while self.running:
            if self.search_for_devices and not self.BTsearcher.is_running() and not self.search_started:
                self.search_started = True
                print "starting BT searcher"
                self.BTsearcher.start()
            elif not self.search_for_devices and self.BTsearcher.is_running():
                print "stopping BT searcher"
                self.search_started = False
                self.BTsearcher.stop()
            elif self.search_for_devices and self.search_started:
                sleep(0.2)

    def stop(self):
        self.BTsearcher.stop()
        self.search_for_devices = False
        self.running = False

    def join(self, timeout=None):
        self.BTsearcher.join(timeout)
        threading.Thread.join(self,timeout)

    def connect(self, target_address, target_port,
                target_protocol=bluetooth.RFCOMM):
        self.target_address = target_address
        self.target_port = target_port
        self.target_protocol = target_protocol
        self.socket = bluetooth.BluetoothSocket(target_protocol)

    def search(self):
        print "search started"
        self.search_for_devices = True

    def stop_search(self):
        self.search_for_devices = False

    def get_uuid(self):
        return self.target_uuid

    def set_uuid(self, uuid=str(uuid4())):
        self.target_uuid = uuid

    def get_devices(self):
        return self.BTsearcher.get_devices()

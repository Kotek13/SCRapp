import bluetooth
import threading
from uuid import uuid4


class BTsearcher(bluetooth.DeviceDiscoverer):
    def __init__(self):
        bluetooth.DeviceDiscoverer.__init__(self)
        self.devices = {}
        self.searching = False

    def pre_inquiry(self):
        self.searching = True

        def device_discovered(self, address, device_class, rssi, name):
            if not self.devices.has_key(address):
                self.devices[address] = (name, rssi, device_class)

        def inquiry_complete(self):
            self.searching = False

        def get_devices(self):
            return self.devices

        def get_device(self, address):
            return self.devices[address]

        def is_searching(self):
            return self.searching


class BTclient(threading.Thread):
    def __init__(self,
                 uuid="00000000-0000-0000-0000-000000000000",
                 name="BTclient"):
        threading.Thread.__init__(self)
        self.socket = None
        self.target_address = None
        self.target_port = None
        self.target_protocol = None
        self.target_uuid = uuid
        self.name = name
        self.BTsearcher = BTsearcher()
        self.search_for_devices = False
        self.running = False

    def run(self):
        while self.running:
            if self.search_for_devices and not self.BTsearcher.is_searching():
                self.search()

    def stop(self):
        self.search_for_devices = False
        self.running = False

    def connect(self, target_address, target_port,
                target_protocol=bluetooth.RFCOMM):
        self.target_address = target_address
        self.target_port = target_port
        self.target_protocol = target_protocol
        self.socket = bluetooth.BluetoothSocket(target_protocol)

    def search(self):
        self.search_for_devices = True
        self.BTsearcher.find_devices(lookup_names=True)

    def stop_search(self):
        self.search_for_devices = False
    def get_uuid(self):
        return self.uuid

    def set_uuid(self, uuid=str(uuid4())):
        self.uuid = uuid

    def get_devices(self):
        return self.BTsearcher.get_devices()

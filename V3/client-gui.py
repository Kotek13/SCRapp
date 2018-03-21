import appJar
from client import BtClient
from threading import Thread
from time import sleep

class BtClientApp():
    def __init__(self):
        self.gui = appJar.gui("Bluetooth client demo")
        self.client = BtClient()
        self.init_gui()
        self.connected = False
        self.gui.thread(self.update_status)
        self.gui.thread(self.update_data)

    def init_gui(self):
        self.gui.startLabelFrame("Connection",0,0)

        self.gui.addLabel("Status", "Status:disconnected")

        self.gui.addButtons(["connection_button", "Default UUID"], [self.connection_button, self.default_uuid])
        self.gui.setButton("connection_button","Connect")

        self.gui.addEntry("UUID")
        self.gui.setEntry("UUID", self.client.uuid)
        self.gui.setEntryWidth("UUID",33)

        self.gui.addLabel("Address", "Address:")
        self.gui.addLabel("Protocol", "Protocol:")
        self.gui.addLabel("Port", "Port:")

        self.gui.stopLabelFrame()

        self.gui.startLabelFrame("Data",0,1)
        self.gui.addScrolledTextArea("Data")
        self.gui.stopLabelFrame()

    def start_app(self):
        self.gui.go()

    def disconnect(self):
        self.client.stop()

    def connection_button(self):
        if self.connected:
            self.client.stop()
            self.gui.setButton("connection_button", "Connect")
            self.connected = False
            self.client = BtClient()
            self.client.daemon = True
        else:
            self.client = BtClient()
            self.client.daemon = True
            self.client.uuid = self.gui.getEntry("UUID")
            self.client.start()
            self.gui.setButton("connection_button", "Disconnect")
            self.connected = True

    def default_uuid(self):
        self.gui.setEntry("UUID","5d6101f4-3c07-4c0e-b9c2-39e1df5690cc")

    def update_status(self):
        while True:
            if self.client.state == self.client.State.stop:
                self.gui.setLabel("Status", "Status:disconnected")
            elif self.client.state == self.client.State.searching:
                self.gui.setLabel("Status", "Status:searching")
            elif self.client.state == self.client.State.connecting:
                self.gui.setLabel("Status", "Status:connecting")
            elif self.client.state == self.client.State.connected:
                self.gui.setLabel("Status", "Status:connected")
            elif self.client.state == self.client.State.stopping:
                self.gui.setLabel("Status", "Status:stopping")

            if self.client.host_addr is not None:
                self.gui.setLabel("Address", "Address:" + self.client.host_addr)
            else:
                self.gui.setLabel("Address", "Address:")

            if self.client.host_prot is not None:
                self.gui.setLabel("Protocol", "Protocol:" + self.client.host_prot)
            else:
                self.gui.setLabel("Protocol", "Protocol:")

            if self.client.host_port is not None:
                self.gui.setLabel("Port", "Port:" + str(self.client.host_port))
            else:
                self.gui.setLabel("Port", "Port:")

            sleep(0.2)

    def update_data(self):
        while True:
            print "buff:",len(self.client.buff)
            data = self.client.get_data()
            if data is not None:
                self.gui.setTextArea("Data", self.gui.getTextArea("Data")+"\n"+data)


if __name__ == "__main__":
    print "GUI started"
    app = BtClientApp()
    app.start_app()
    print "Add ended"
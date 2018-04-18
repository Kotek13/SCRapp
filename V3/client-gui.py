import appJar
from client import BtClient
from time import sleep, time
from logger import DataLogger
from speedcounter import SpeedCounter

class BtClientApp:
    def __init__(self):
        self.gui = appJar.gui("Bluetooth client demo","1300x300")
        self.gui.thread(self.update_status)
        self.gui.thread(self.update_data)

        self.connected = False

        self.client = BtClient()
        self.logger = DataLogger()
        self.BTspeed = SpeedCounter()

        self.init_gui()

    def init_gui(self):
        self.gui.startLabelFrame("Connection", 0, 0)
        self.gui.setStretch("row")

        self.gui.addLabel("Status", "Status:disconnected")

        self.gui.addButtons(["connection_button", "Default UUID"], [self.connection_button, self.default_uuid])
        self.gui.setButton("connection_button", "Connect")

        self.gui.addEntry("UUID")
        self.gui.setEntry("UUID", self.client.uuid)
        self.gui.setEntryWidth("UUID", 33)

        self.gui.addLabel("Address", "Address:")
        self.gui.addLabel("Protocol", "Protocol:")
        self.gui.addLabel("Port", "Port:")

        self.gui.stopLabelFrame()

        self.gui.startLabelFrame("Data", 0, 1)
        self.gui.addLabel("buffer_size", "Buffer size:"+str(len(self.client.buff)))
        self.gui.addLabel("buffer", self.client.buff)
        self.gui.addLabel("packets", "Packets waiting:"+str(len(self.client.packets)))
        self.gui.addLabel("data_label", "Data:")
        # self.gui.addMeter("data_meter")
        # self.gui.startLabelFrame("Log File",4,1)
        self.gui.addLabelFileEntry("log_file")
        self.gui.setLabel("log_file", "Path")
        self.gui.setEntry("log_file", "data.log")
        # self.gui.addLabelEntry("log_name")
        # self.gui.setLabel("log_name", "Name")
        # self.gui.stopLabelFrame()
        self.gui.stopLabelFrame()
        self.gui.startLabelFrame("plot",0,2)
        self.gui.addPlot("p1", [0], [0])
        self.gui.stopLabelFrame()

    def start_app(self):
        self.BTspeed.start()
        self.gui.go()

    def disconnect(self):
        self.client.stop()

    def connection_button(self):
        if self.connected:
            self.client.stop()
            self.logger.stop()
            self.gui.setButton("connection_button", "Connect")
            self.connected = False
            # self.client = BtClient()
            # self.client.daemon = True
        else:
            self.client = BtClient()
            self.client.daemon = True
            self.client.uuid = self.gui.getEntry("UUID")
            self.client.start()
            self.logger.start(self.gui.getEntry("log_file"))
            self.gui.setButton("connection_button", "Disconnect")
            self.connected = True

    def default_uuid(self):
        self.gui.setEntry("UUID", "5d6101f4-3c07-4c0e-b9c2-39e1df5690cc")

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

            if self.client.host_address is not None:
                self.gui.setLabel("Address", "Address:" + self.client.host_address)
            else:
                self.gui.setLabel("Address", "Address:")

            if self.client.host_protocol is not None:
                self.gui.setLabel("Protocol", "Protocol:" + self.client.host_protocol)
            else:
                self.gui.setLabel("Protocol", "Protocol:")

            if self.client.host_port is not None:
                self.gui.setLabel("Port", "Port:" + str(self.client.host_port))
            else:
                self.gui.setLabel("Port", "Port:")
            speed = self.BTspeed.get_speed()
            # print(speed)
            # speed = [(0,1),(1,2),(3,2)]
            curr_time = time()
            x = [round(i[0]-curr_time, 3) for i in speed]
            y = [i[1] for i in speed]
            self.gui.updatePlot("p1", x, y)

            sleep(0.2)

    def update_data(self):
        while True:
            # print "buff:",len(self.client.buff)
            data = self.client.get_data()
            self.gui.setLabel("buffer_size", "Buffer size:" + str(len(self.client.buff)))
            self.gui.setLabel("buffer", self.client.buff)
            self.gui.setLabel("packets", "Packets waiting:" + str(len(self.client.packets)))
            if data is not None:
                self.gui.setLabel("data_label", "Data:"+data)
                # self.gui.setMeter("data_meter", round(Decimal(data)*100), data)
                self.logger.log(data)
                self.BTspeed.add_data(len(data))
            else:
                sleep(0.1)


if __name__ == "__main__":
    print("GUI started")
    app = BtClientApp()
    app.start_app()
    print("App ended")

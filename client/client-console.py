from BTclient import BTclient
from time import sleep
from tabulate import tabulate
import bluetooth

client = BTclient()

client.daemon = True
client.set_uuid("5d6101f4-3c07-4c0e-b9c2-39e1df5690cc")
client.start()
scan = True
target = None
while scan:
    client.search()
    for i in reversed(range(1,30)):
        print i
        sleep(1)
    client.stop_search()
    services = client.get_services()
    if len(services) == 0:
        print "None devices found"

    else:
        print "Found",len(services),"devices:"
        table = []
        for i in range(0,len(services)):
            table.append([i+1,
                          services[i]["host"],
                          services[i]["name"],
                          services[i]["port"],
                          services[i]["service-id"],
                          services[i]["protocol"]])
        print tabulate(table,headers=["No.","Address","Name","Port","UUID","Protocol"])

    print "select device to connect or -1 to rescan"
    while True:
        selection = input("Selection:")
        if selection == "q":
            client.stop()
            client.join()
            exit(0)
        elif int(selection) == -1:
            break;
        elif 1<=int(selection) and int(selection)<=len(services):
            scan = False
            target = services[selection-1]
            break

if target is None:
    print "unspecified target"
    exit(0)
if target["protocol"] == "RFCOMM":
    client.connect(target["host"],int(target["port"]),bluetooth.RFCOMM)
elif target["protocol"] == "L2CAP":
    client.connect(target["host"],int(target["port"]),bluetooth.L2CAP2)

try:
    while True:
        data = client.get_data()
        if data is not None:
            print data
        print "buff empty"
except KeyboardInterrupt:
    print "Keyboard interruption"

client.stop()
client.join()
print "client stopped"


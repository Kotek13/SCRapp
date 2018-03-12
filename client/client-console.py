from BTclient import BTclient
from time import sleep

client = BTclient()

client.daemon = True
client.set_uuid("5d6101f4-3c07-4c0e-b9c2-39e1df5690cc")
client.start()
scan = True
while scan:
    client.search()
    for i in reversed(range(1,30)):
        print i
        sleep(1)
    client.stop_search()
    devices = client.get_devices()
    if len(devices) == 0:
        print "None devices found"
    else:
        address = devices.keys()
        print "Found",len(devices),"devices:"
        for i in range(0,len(address)):
            print i, ".\t", address[i], devices[address[i]]
    print "select device to connect or -1 to rescan"
    while True:
        selection = int(input("Selection:"))
        if selection == -1:
            break;
        elif 0<=selection and selection<len(devices):
            scan = False
            target =




client.stop()
client.join()
print "client stopped"
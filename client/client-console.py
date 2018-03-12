from BTclient import BTclient
from time import sleep

client = BTclient()

client.daemon = True
client.set_uuid("5d6101f4-3c07-4c0e-b9c2-39e1df5690cc")
client.start()
client.search()
for i in reversed(range(1,30)):
    print i
    sleep(1)
client.stop_search()
devices = client.get_devices()
if len(devices) == 0:
    print "None devices found"
else:
    print "Found",len(devices),"devices:"
    for i in range(1,len(devices)):
        print i, ".\t", devices[i]

client.stop()
client.join()
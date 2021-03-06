from BTserver import BTserver
from random import random
from time import sleep

server = BTserver();
server.daemon = True
print "UUID:"
server.set_uuid(uuid = "5d6101f4-3c07-4c0e-b9c2-39e1df5690cc")
print server.get_uuid()
try:
    print "server started"
    server.start()
    while server.isAlive():
        #print "server alive"
        while server.connected():
            #print "sending data"
            server.send_data(str(random()))
        sleep(0.1)
    print "server thread died"
except KeyboardInterrupt:
    print "keyboard interruption"
else:
    print "exception raised"
finally:
    server.stop()
    print "server stopped"


from BTclient import BTsearcher
from time import sleep

searcher = BTsearcher()
searcher.daemon = True
searcher.start()

for i in reversed(range(1,15)):
    print i
    sleep(1)

searcher.stop()
devices = searcher.get_devices()
print devices

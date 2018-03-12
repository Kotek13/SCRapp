from BTclient import BTsearcher
from time import sleep

searcher = BTsearcher()
searcher.daemon = True
searcher.start()
searcher.enable_searching()

for i in reversed(range(1,30)):
    print i
    sleep(1)

searcher.disable_serching()
searcher.stop()
devices = searcher.get_devices()
print devices

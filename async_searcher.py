import select
from BTclient import BTclient

d = BTclient()

try:
	while True:
		print "search started"
		d.find_devices(lookup_names = True,duration = 15)
		readfiles = [ d, ]
		while not d.done:
			print "loop..."
			rfds = select.select( readfiles, [], [] )[0]
			if d in rfds:
				d.process_event()
except KeyboardInterrupt:
	print ""

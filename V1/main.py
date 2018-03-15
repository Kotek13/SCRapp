
import bluetooth

target_name = None
target_address = None

scan_attempt_number = 0
device_address_list = []

scan_flag = True

while scan_flag:
	scan_attempt_number += 1
	print "Searching for devices, attempt number ",scan_attempt_number
	nearby_devices = bluetooth.discover_devices(lookup_names = True)
	print "Found ", len(nearby_devices), " devices"
	for device in nearby_devices:
		print "[%s] - %s" % (device[0],device[1])
		if device not in device_address_list:
			device_address_list.append(device)
		
	print "Found %d devices in total" % len(nearby_devices)
	print "Num \t Addr      Name"
	for i in range(0,len(device_address_list)):
		print "%d. \t%s - %s"%(i,device_address_list[i][0],device_address_list[i][1])
	
	print "Type:"
	print "-1     - rescan for new devices"
	print "q      - for quitting"
	print "number - for connecting with listed device"
	while True:
		usr_input = raw_input("Selection [None = rescan]: ")
		if usr_input == "":
			break
		if usr_input == "q":
			scan_flag = False
			break
		try:
			val = int(usr_input)
			if val==-1:
				break
			elif  0<= val and val < len(device_address_list):
				scan_flag = False
				[target_address, target_name] = device_address_list[val]
				break
			else:
				print "Value out of range:",val
		except ValueError:
			print "Invalid selection:",usr_input
	print "\n"
	
print "Selected device",target_address,"name:",target_name




import pypixet
pypixet.start()

pixet = pypixet.pixet

devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)

if not devices:
    print("No devices connected")
    exit()
    
device = devices[0]

temp = device.temperature(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)
rounded_temperature = '{0:.5g}'.format(temp)

print("Temperature (C): " + rounded_temperature)

pypixet.exit()
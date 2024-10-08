import VXTCUevo 

# Create a TCU object
TCU = VXTCUevo.TCUevo()
TCU.initialize()
TCU.conncect(ip = '192.168.33.1', port = 50000)
TCU.start()
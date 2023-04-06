import binascii
import pyvisa as visa


wave_points = [0x8000, 0x3f06]

def create_wave_file():
    f = open('wave1.bin','wb')
    for a in wave_points:
        b = hex(a)
        b = b[2:]
        len_b = len(b)
        if(0 == len_b):
            b = '0000'
        elif(1 == len_b):
            b = '000' + b
        elif(2 == len_b):
            b = '00' + b
        elif(3 == len_b):
            b = '0' + b
        c = binascii.a2b_hex(b)
        f.write(c)
    f.close()


def main():

    rm = visa.ResourceManager()
    inst = None
    if len(rm.list_resources()) == 0:
    	print("No Devices Attatched, Check USB Cable")
    	return
    else:
    	if not len(rm.list_resources()) == 1:
    		print(rm.list_resources())
    		deviceName = input("Enter device name(from list above):")
    	for resource in rm.list_resources():
    		if not len(rm.list_resources()) == 1 and not deviceName in resource:
    			continue
    		inst = rm.open_resource(resource)
    		if not "SDG2042X" in inst.query('*IDN?'):
    			print("Incorrect device attatched.")
    			return
    		else:
    			break 
    type = input("Please type (Demo, File, or Manual): ").lower()
    values = None  
    if type == "demo":
    	create_wave_file()
    	f = open('wave1.bin', 'rb')
    	data = f.read().decode('latin1')
    	values = [ord(c) for c in data]
    	f.close()
    elif type == "file":

    	file = input("Please input file name: ")
    	f = None
    	try:
    	    f = open(file, 'rb')
    	except FileNotFoundError:
    		print("Oops! Invalid file.", end="")
    		return
    	data = f.read().decode('latin1')
    	values = [ord(c) for c in data]
    	f.close()
    else:
    	values = []
    	i = 0
    	while True:
    		value = input("Index %d (\'stop\' to end): "%(i))	
    		if len(value) == 0 or value.lower() == "stop":
    			break
    		if not value.isdigit():
    			print("Please input a number! \"%s\" is not a valid number."%(value))
    			continue
    		i+=1
    		values.append(int(value))
    print('Sending waveform...', end="")
    
    inst.write_ascii_values('C1:WVDT WVNM,wave1,WAVEDATA,', values)
    inst.write_ascii_values('C1:ARWV NAME,wave1', {})
    

if __name__ == '__main__':
    proc = main()

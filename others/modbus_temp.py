import emodbus as emb

def main_process(callback):
    print("Main process started.")
    print("Doing some tasks.")
    result = "Task completed."
    callback(result)  # Call the callback function with the result
    print("Main process finished.")

def my_callback_function(message):
    print(f"Inside the callback: {message}")

# main_process(my_callback_function)
# print(str(type(my_callback_function))=="<class 'function'>")

# connect to bus of devices
tcp = emb.ConnTCP('192.168.1.45')
rtu = emb.ConnRTU('/dev/ttyUSB0') # linux
# rtu = emb.ConnRTU('COM4') # windows

# Other way to input parameters
# rtuParam={
#     'port': 'COM1',
#     'baudrate': 9600,
#     'bytesize': 8,
#     'stopbits': 1,
#     'timeout': 0.1
# }
# rtu = emb.ConnRTU(**rtuParam)
#
# rtuParamLst=['COM1',9600,8]
# rtu = emb.ConnRTU(*rtuParamLst)
#

# define default MIB
# {name: (Address:int,functionCode:int,callbackFunction_modbustype:'None|str|tuple|list'),....},

# tipo=emb.modbustypes.Dec()
# tipo.dec=1

mib = {  # Management Information Bases
    # 'Temperature': [1, 4, tipo],
    'Temperature': [1, 4, ['Dec', {'dec': 1,'format':'{:.1f}°',}]],
    'Humidy': [2, 4, ['Dec', {'dec': 1}]],
    'TemperatureRaw': [1, 4],
    'HumidyRaw': [2, 4],
}

# Define default MIB to slave
emb.Conn.defSlave(1, mib)

# # Read MIB of any slave of the connection
print('TCP MIB Slave 1', tcp.slave(1)(), sep=':')
print()

# define MIB of connection/slave
# tcp.slave(1, mib)
# rtu.slave(1, mib)

# read all MIB
# slaves = list(range(11,16))+list(range(31,37))
slaves = [1]
for slave in slaves:
    print('Read All Slave ', slave)
    print('TCP', tcp.read(slave), sep=':')
    print('RTU', rtu.read(slave), sep=':')
print()

# read only some address
addr = ['Temperature', 'xxxxxxxxxx', 'Humidy']
for slave in slaves:
    print('Read Slave '+str(slave), addr, sep=':')
    r=tcp.read(slave, addr)
    print('TCP', r, sep=':')
    print(r['Temperature'])
    print('RTU', rtu.read(slave, addr), sep=':')

# Demostration
# addrValues = {
#     'Temperature': 30.1,
#     'xxxxxxxxxx': 40.2,
#     'Humidy': 40.5,
#     'TemperatureRaw': 301,
# }
# slave=1
# tcp.write(slave,addrValues)


# import json as js

# rtuParam="""{
#     "port": "COM1",
#     "baudrate": 9600,
#     "bytesize": 8,
#     "stopbits": 1,
#     "timeout": 0.1
# }"""
# res=js.loads(rtuParam)
# print(type(rtuParam),rtuParam)
# print(type(res),res)
# print(res['port'])



# list all serial ports
# import serial.tools.list_ports as ls
# print([p.device for p in ls.comports()])
# print()

# Next generation MIB
mib2 = {  # Management Information Bases
    'version': 'xxxdd',
    'data': {
        'vendor': 'xxxxxx',
        'model': 'xxxxxx',
    },
    'imports': [],
    'addrs': {
        # 'Temperature': [1, 4, tipo],
        'Temperature': [1, 4, ['Dec', {
            'dec': 1, 
            'format':'{.1f}°',
            'descr': 'sadhfj sadlçkfj çlaskdj çlk',
        }]],
        'Humidy': [2, 4, ['Dec', {'dec': 1}]],
        'TemperatureRaw': [1, 4],
        'HumidyRaw': [2, 4],
    },
}
# Fix implement descr attribute to types
# Fix __str__ to print with format when exists

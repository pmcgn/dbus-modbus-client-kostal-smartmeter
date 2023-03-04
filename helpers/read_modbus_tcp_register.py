from pymodbus.client.tcp import ModbusTcpClient as ModbusClient

client = ModbusClient(method='tcp', host='192.168.2.53', port='502')

client.connect()

read=client.read_holding_registers(address = 8193, count = 2, slave = 1) 

data=read.registers[0]

for value in read.registers:
    print("DEC: " , value , ", HEX: " , hex(value))

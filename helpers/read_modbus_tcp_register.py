from pymodbus.client.tcp import ModbusTcpClient as ModbusClient

client = ModbusClient(method='tcp', host='192.168.2.53', port='502')

client.connect()

read=client.read_holding_registers(address = 8193, count = 1, slave = 1) 


data=read.registers[0]

print("DEC: " , data , ", HEX: " , hex(data))

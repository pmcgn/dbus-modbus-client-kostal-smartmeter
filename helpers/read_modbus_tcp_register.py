from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
import ipaddress
from pymodbus.exceptions import ConnectionException, ModbusIOException

ksemIP = input("IP (v4) Address of your KOSTAl SMart Energy Meter (KSEM): ")

try:
    if ipaddress.IPv4Address(ksemIP):
        client = ModbusClient(method='tcp', host=ksemIP, port=502)
        
        try:
            client.connect()
            
            try:
                read=client.read_holding_registers(address = 0x2001, count = 1, slave = 1) 
                
                for value in read.registers:
                    print("KSEM Device ID (Decimal): ", value)
                    # print("DEC: ", value, ", HEX: ", hex(value))

            except ModbusIOException as modbus_io_exception:
                print(f"Modbus error while reading the register: {modbus_io_exception}")

        except ConnectionException as connection_exception:
            print(f"TCP connection can't be established. Check KSEM IP. Check if Modbus Server is enabled on the KSEM.")

        finally:
            client.close()

    else:
        print(f"The provided address {ksemIP} is not a valid IPv4 address. Aborting.")
        exit(1)

except ValueError as value_error:
    print(f"Invalid IP address format: {value_error}")
    exit(1)

# Use KOSTAL Smart Energy Meter with Victron Systems

This project enables the use of KOSTAL Smart Energy Meters (KSEM) within an Victron Envrionment. After installing this module on an VenusOS Device (like the Cerbo GX), the GX device will be able to identify and use the data of a KSEM. For example, an existing Kostal Photovoltaic System shall be extenden with a battery, controlled by a Multiplus II, there is no need of an additional Energy Meter, as the live values from the Kostal System can be used inside the Victron System.

![Kostal Smart Energy Meter detected by Cerbo GX](pictures/ksem_in_victronui.png?raw=true)

## Getting Started

To be able to communicate with the KSEM, the KSEM must be directly connected to the local network via it's LAN port. It is not enough, that the PV Inverter is connected via LAN. Make sure that the Modbus TCP port is open (on the Webinterface of the KSEM: Settings -> Modbus TCP Settings -> Slave -> Enable TCP Slave = ON). Also, please ensure the the KSEM has always the same IP (either static IP or statically assigned by DHCP server!).
In addition, you need root access to the GX device. The procedure is descibed in the [Venus OS Documentation](https://www.victronenergy.com/live/ccgx:root_access).
This readme assumes, that you are familiar with basic file operations and SSH usage. I may improve the description later.

### Installation

 1. SSH into the GX device
 2. Navigate to the modbus client folder: `cd /opt/victronenergy/dbus-modbus-client`
 3. Download the module: `wget https://raw.githubusercontent.com/pmcgn/dbus-modbus-client-kostal-smartmeter/main/Kostal_SmartEnergyMeter.py`
 4. Open the file dbus-modbus-client.py in a text editor: `vi dbus-modbus-client.py`
 5. Add the instruction `import Kostal_SmartEnergyMeter` behind the other imports (before typing, press `i` to switch to input mode
 6. Save and exit vi: Press `ESC` then type `:wq` and press `Enter`
 7. Delete python cache: `rm /opt/victronenergy/dbus-modbus-client/__pycache__/dbus-modbus-client.cpython-38.pyc`
 8. Restart the GX device via `reboot`

## Usage

Open the GX Webinterface and navigate to Settings -> Modbus TCP Devices and trigger a Scan. It should now be able to find the KSEM. If the automatic detection does not work, go to Devices and press Add, to add the KSEM IP manually.

## Known Limitations

 1. Serial number not shown in victron. This is an Issue of the KSEM, as it does not provide a correct value for the serial number.
 2. Power precision is 10W. This is a limitation of the used SunSpec register. There are internal registers which provide higher precision, but they don't propagate positive and negative values on the same register.

## Troubleshooting

 - Check that the file Kostal_SmartEnergyMeter.py exists and that it is placed into the correct dorectory
 - Check if the import instruction in the file dbus-modbus-client.py has been saved
 - Check if the KSEM IP is reachable from the local network
 - Check if the Modbus TCP Service is running on the KSEM (either by checking the configuration or using Modbus TCP test tools).
 - Ensure that the IP of the KSEM does not change after adding it to the GX device. Otherwise the communication will fail after a while.
 - Check logfile `/var/log/dbus-modbus-client/current` on VenusOS device. Expectation is to see a line containing `Found KOSTAL_KSEM at tcp:<ksem-ip>:502:1`
 - It seems that KOSTAL is changing the identifier of the KSEM with some updates. This identifier is used by Victron to ensure that the target device is really a Kostal Smart Energy Meter. To check if you are affected by the change, please execute the following steps:
   - Install python on your computer via https://www.python.org/downloads/ (Sorry, currently the next script does not run directly on VenusOS, Pull requests are welcome)
   - Download the helper script `https://raw.githubusercontent.com/pmcgn/dbus-modbus-client-kostal-smartmeter/main/helpers/read_modbus_tcp_register.py` to your windows machine
   - Execute it with `python <path-to-script>\read_modbus_tcp_register.py`
   - The script will ask for the KSEM IP Address, enter it and hit enter
   - If everything is ok, the script will tell you the Identifier of your KSEM (`KSEM Device ID (Decimal):  18498`)
   - Open the file Kostal_SmartEnergyMeter.py on the KSEM (Downloaded during installation), and make sure that the identifier from the previous step is listed at the end. For Example: `models = { 18498: ...`
   - If your identifier does not appear here, change the default of 18498 to the value from the helper script
   - Reboot the VenusOS device after changing the identifier
   - If it works, please let me know your identifier. The easiest way is to create a github issue (mention your value!).

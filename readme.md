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
 7. Restart the GX device via `reboot`

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
# VenusOS module for support of KOSTAL Smart Energy Meter
# Community contribution by Philipp Mahler

import logging
import device
import probe
from register import *

log = logging.getLogger()

class Kostal_SmartEnergyMeter(device.EnergyMeter):
    productid = 0x00
    productname = 'KOSTAL Smart Energy Meter'
    min_timeout = 0.5

    def __init__(self, *args):
        super(Kostal_SmartEnergyMeter, self).__init__(*args)

        self.info_regs = [
            Reg_u16(0x2002, '/HardwareVersion'),
            Reg_u16(0x2003, '/FirmwareVersion'),
            Reg_text(0x2024, 4, '/Serial'),
        ]

    def device_init(self):
        self.read_info()

        regs = [
            Reg_u32b(0x001A, '/Ac/Frequency',         1000,  '%.1f Hz'),
            Reg_u64b(0x0200, '/Ac/Energy/Forward',    10000, '%.1f kWh'),
            Reg_u64b(0x0204, '/Ac/Energy/Reverse',    10000, '%.1f kWh'),
            
            Reg_u32b(0x003E, '/Ac/L1/Voltage',        1000,  '%.1f V'),
            Reg_u32b(0x003C, '/Ac/L1/Current',        1000,  '%.3f A'),
            Reg_u64b(0x0250, '/Ac/L1/Energy/Forward', 10000, '%.1f kWh'),
            Reg_u64b(0x0254, '/Ac/L1/Energy/Reverse', 10000, '%.1f kWh'),

            Reg_u32b(0x0066, '/Ac/L2/Voltage',        1000,  '%.1f V'),
            Reg_u32b(0x0064, '/Ac/L2/Current',        1000,  '%.3f A'),
            Reg_u64b(0x02A0, '/Ac/L2/Energy/Forward', 10000, '%.1f kWh'),
            Reg_u64b(0x02A4, '/Ac/L2/Energy/Reverse', 10000, '%.1f kWh'),

            Reg_u32b(0x008E, '/Ac/L3/Voltage',        1000,  '%.1f V'),
            Reg_u32b(0x008C, '/Ac/L3/Current',        1000,  '%.3f A'),
            Reg_u64b(0x02F0, '/Ac/L3/Energy/Forward', 10000, '%.1f kWh'),
            Reg_u64b(0x02F4, '/Ac/L3/Energy/Reverse', 10000, '%.1f kWh'),

            # Power data from KSEM internal registers, different ones for pos/neg values

            Reg_u32b(0x0000, '/Ac/Power',             10,    '%.1f W'),  # positive value register total power
            Reg_u32b(0x0002, '/Ac/Power',             -10,   '%.1f W'),  # negative value register total power
            Reg_u32b(0x0028, '/Ac/L1/Power',          10,    '%.1f W'),  # positive value register L1 power
            Reg_u32b(0x002A, '/Ac/L1/Power',          -10,   '%.1f W'),  # negative value register L1 power
            Reg_u32b(0x0050, '/Ac/L2/Power',          10,    '%.1f W'),  # positive value register L2 power
            Reg_u32b(0x0052, '/Ac/L2/Power',          -10,   '%.1f W'),  # negative value register L2 power
            Reg_u32b(0x0078, '/Ac/L3/Power',          10,    '%.1f W'),  # positive value register L3 power
            Reg_u32b(0x007A, '/Ac/L3/Power',          -10,   '%.1f W'),  # negative value register L3 power

            # Power data from SunSpec registers alternatively
            #
            # Drawbacks:
            # - lower resolution (10W instead of 0.1W)
            # - requires consideration of power scale factor (e.g. -1 to shift decimal point one to the left, see SunSpec specification section 4.2.8)

            # Reg_u16(0x9C9C, '/Ac/PowerFactor'),
            # Reg_s16(0x9C98, '/Ac/Power',    1, '%.0f W'),
            # Reg_s16(0x9C99, '/Ac/L1/Power', 1, '%.0f W'),
            # Reg_s16(0x9C9A, '/Ac/L2/Power', 1, '%.0f W'),
            # Reg_s16(0x9C9B, '/Ac/L3/Power', 1, '%.0f W'),
        ]
        
        self.data_regs = regs

    def get_ident(self):
        return 'cg_%s' % self.info['/Serial']


models = {
    18498: {
        'model':    'KOSTAL_KSEM',
        'handler':  Kostal_SmartEnergyMeter,
    },
    18514: {
        'model':    'KOSTAL_KSEM',
        'handler':  Kostal_SmartEnergyMeter,
    },
    18530: {
        'model':    'KOSTAL_KSEM',
        'handler':  Kostal_SmartEnergyMeter,
    },
}



#VenusOS < 2.92
#probe.add_handler(probe.ModelRegister(0x2001, models, methods=['tcp'], units=[1]))

#VenusOS >= 2.92
probe.add_handler(probe.ModelRegister(Reg_u16(0x2001), models, methods=['tcp'], units=[1]))


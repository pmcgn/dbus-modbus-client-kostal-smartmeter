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
            Reg_u16(0x2033, '/Serial'), # not populated correctly by KSEM, therefore reading it as uInt instad of String
        ]


    def device_init(self):
        self.read_info()

        regs = [
            Reg_s16(0x9C98,  '/Ac/Power',             10,   '%.0f W'),     # Using SunSpec register with lower resolution (10W instead of 0.1W)
            Reg_u32b(0x001A, '/Ac/Frequency',         1000,  '%.1f Hz'),
            Reg_u64b(0x0200, '/Ac/Energy/Forward',    10000, '%.1f kWh'),
            Reg_u64b(0x0204, '/Ac/Energy/Reverse',    10000, '%.1f kWh'),
            
            Reg_u32b(0x003E, '/Ac/L1/Voltage',        1000,  '%.1f V'),
            # Reg_u32b(0x003C, '/Ac/L1/Current',        1000,  '%.3f A'),   # KSEM internal register. Higher Resolution but pos/neg on different registers
            Reg_s16(0x9C89,  '/Ac/L1/Current',        100,   '%.2f A'),     # Using SunSpec register with lower resolution
            Reg_s16(0x9C99,  '/Ac/L1/Power',          10,   '%.0f W'),     # Using SunSpec register with lower resolution
            Reg_u64b(0x0250, '/Ac/L1/Energy/Forward', 10000, '%.1f kWh'),
            Reg_u64b(0x0254, '/Ac/L1/Energy/Reverse', 10000, '%.1f kWh'),

            Reg_u32b(0x0066, '/Ac/L2/Voltage',        1000,  '%.1f V'),
            # Reg_u32b(0x0064, '/Ac/L2/Current',        1000,  '%.3f A'),   # KSEM internal register. Higher Resolution but pos/neg on different registers
            Reg_s16(0x9C8A,  '/Ac/L2/Current',        100,   '%.2f A'),     # Using SunSpec register with lower resolution
            Reg_s16(0x9C9A,  '/Ac/L2/Power',          10,   '%.0f W'),     # Using SunSpec register with lower resolution
            Reg_u64b(0x02A0, '/Ac/L2/Energy/Forward', 10000, '%.1f kWh'),
            Reg_u64b(0x02A4, '/Ac/L2/Energy/Reverse', 10000, '%.1f kWh'),

            Reg_u32b(0x008E, '/Ac/L3/Voltage',        1000,  '%.1f V'),
            # Reg_u32b(0x008C, '/Ac/L3/Current',        1000,  '%.3f A'),   # KSEM internal register. Higher Resolution but pos/neg on different registers
            Reg_s16(0x9C8B,  '/Ac/L3/Current',        100,   '%.2f A'),     # Using SunSpec register with lower resolution
            Reg_s16(0x9C9B,  '/Ac/L3/Power',          10,   '%.0f W'),     # Using SunSpec register with lower resolution
            Reg_u64b(0x02F0, '/Ac/L3/Energy/Forward', 10000, '%.1f kWh'),
            Reg_u64b(0x02F4, '/Ac/L3/Energy/Reverse', 10000, '%.1f kWh'),
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


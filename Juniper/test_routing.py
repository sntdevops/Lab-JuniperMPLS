import napalm
import os
from pprint import pprint

MPLS_Devices ={'RT-EDGE-01':{'IP':'172.16.209.104','username':'automation', 'password':'auto1234'},
               'RT-EDGE-02':{'IP':'172.16.209.105','username':'automation', 'password':'auto1234'},
               'RT-CORE-01':{'IP':'172.16.209.101','username':'automation', 'password':'auto1234'},
               'RT-CORE-02':{'IP':'172.16.209.102','username':'automation', 'password':'auto1234'},
               'RT-CORE-03':{'IP':'172.16.209.103','username':'automation', 'password':'auto1234'},
               'RT-CORE-RR':{'IP':'172.16.209.106','username':'automation', 'password':'auto1234'},
               'RT-INTERNET-01':{'IP':'172.16.209.107','username':'automation', 'password':'auto1234'},
               'RT-INTERNET-02':{'IP':'172.16.209.108','username':'automation', 'password':'auto1234'}
}
MPLS_Devices_Loopback ={'RT-EDGE-01':'10.100.1.101',
               'RT-EDGE-02':'10.100.1.102',
               'RT-CORE-01':'10.100.1.1',
               'RT-CORE-02':'10.100.1.2',
               'RT-CORE-03':'10.100.1.3',
               'RT-CORE-RR':'10.100.1.201',
               'RT-INTERNET-01':'10.100.1.251',
               'RT-INTERNET-02':'10.100.1.252'
}


driver = napalm.get_network_driver('junos')
device = driver(hostname = MPLS_Devices['RT-EDGE-01']['IP'], username = MPLS_Devices['RT-EDGE-01']['username'], password = MPLS_Devices['RT-EDGE-01']['password'], optional_args={'port': 830})

device.open()

if device.is_alive():
    for key, value in MPLS_Devices_Loopback.items():
        result = device.ping(value, ttl=10, timeout=2, size=100, count=2)
        if result['success']:
            print("Pinging----->" + key + " IP:" + value + "\n\t\t\t\t\t\t------------------->*" + str(result['success']['rtt_avg']))
        else: print("Pinging----->" + key + " IP:" + value + "\n\t\t\t\t\t\t-------------------")


print("\n\n------All Done-----" )
device.close()
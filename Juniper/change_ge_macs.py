import napalm
import os
from pprint import pprint
import pyping

config_dir = os.path.join(os.path.dirname(__file__),'conf')

MPLS_Devices ={'RT-EDGE-01':{'IP':'172.16.209.101','username':'automation', 'password':'auto1234'},
               'RT-EDGE-02':{'IP':'172.16.209.102','username':'automation', 'password':'auto1234'},
               'RT-CORE-01':{'IP':'172.16.209.103','username':'automation', 'password':'auto1234'},
               'RT-CORE-02':{'IP':'172.16.209.104','username':'automation', 'password':'auto1234'},
               'RT-CORE-03':{'IP':'172.16.209.105','username':'automation', 'password':'auto1234'},
               'RT-CORE-RR':{'IP':'172.16.209.106','username':'automation', 'password':'auto1234'},
               'RT-INTERNET-01':{'IP':'172.16.209.107','username':'automation', 'password':'auto1234'}
               'RT-INTERNET-01':{'IP':'172.16.209.108','username':'automation', 'password':'auto1234'}
}

def MPLS_Device_alive(MPLS_Device):
    r = pyping.ping(MPLS_Device[IP])

    if r.ret_code == 0:
        print("Success")
    else:
        print("Failed with {}".format(r.ret_code))




driver = napalm.get_network_driver('junos')
device = driver(hostname='172.16.209.101', username='automation', password='auto1234', optional_args={'port': 830})
#device.close()
device.open()

print(device.username)

if device.is_alive():
    Interfaces=device.get_interfaces()

Int_List = {'em2','em3','em4','em5','em6'}

trailer = " }"

conf= "interfaces { "
print("\n")
pprint(Interfaces)
n=0
k = list(Interfaces.keys())
k.sort()
pprint(k)

for key,value in Interfaces.items():
    if key in Int_List:
        conf= conf + " " + "ge-0/0/" + str(int(key[2])-2) +  "{ mac " + str(value['mac_address'] ) + "}"
        print()
        n=n+1

conf = conf + trailer 
print(conf)

if device.is_alive():
    device.load_replace_candidate(filename=config_dir+'/juniper/RT-EDGE.01.conf')
    device.load_merge_candidate(config=conf)

diffs = device.compare_config()
print len(diffs)
if len(diffs) > 1:
    print(diffs)
    device.commit_config()
else:
    print('No changes needed')
    device.discard_config()

device.close()
import argparse
import napalm
import os
from pprint import pprint
from threading import Thread


def SendToDevice(DeviceName, DeviceConnInfo, config_dir):

    driver = napalm.get_network_driver('junos')
    device = driver(hostname = DeviceConnInfo['IP'], username = DeviceConnInfo['username'], password = DeviceConnInfo['password'], optional_args={'port': 830})
    #device.close()
    device.open()

    if device.is_alive():
        Interfaces=device.get_interfaces()

    Int_List = {'em2','em3','em4','em5','em6'}

    trailer = " }"

    conf= "interfaces { "
    n=0
    k = list(Interfaces.keys())
    k.sort()

    for key,value in Interfaces.items():
        if key in Int_List:
            conf= conf + " " + "ge-0/0/" + str(int(key[2])-2) +  "{ mac " + str(value['mac_address'] ) + "}"
            n=n+1

    conf = conf + trailer 

    if device.is_alive():
        device.load_replace_candidate(filename = config_dir + DeviceName + '.conf')
        device.load_merge_candidate(config=conf)
        device.load_merge_candidate(filename = config_dir + "RT-MPLS-Common.conf")

    diffs = device.compare_config()
    if len(diffs) > 1:
        print('--------' + DeviceName + '--------')
        print(diffs)
        print('----------------------------------')
        device.commit_config()
    else:
        print('No changes needed on ' + DeviceName)
        device.discard_config()

    device.close()
    print('-------- Finshed with ' + DeviceName + '--------')

def load_conf_2_all(config_dir):


    Devices ={'RT-EDGE-01':{'IP':'172.16.209.104','username':'automation', 'password':'auto1234'},
                'RT-EDGE-02':{'IP':'172.16.209.105','username':'automation', 'password':'auto1234'},
                'RT-CORE-01':{'IP':'172.16.209.101','username':'automation', 'password':'auto1234'},
                'RT-CORE-02':{'IP':'172.16.209.102','username':'automation', 'password':'auto1234'},
                'RT-CORE-03':{'IP':'172.16.209.103','username':'automation', 'password':'auto1234'},
                'RT-CORE-RR':{'IP':'172.16.209.106','username':'automation', 'password':'auto1234'},
                'RT-INTERNET-01':{'IP':'172.16.209.107','username':'automation', 'password':'auto1234'},
                'RT-INTERNET-02':{'IP':'172.16.209.108','username':'automation', 'password':'auto1234'}
    }

    threads = []

    for key, value in Devices.items():
        print("New Thread for " + key + " IP:" + value['IP'] )
        try:
            t = Thread(target=SendToDevice, args= (key, value, config_dir))
            threads.append(t)
        except Exception as e:
            print ("Error: unable to start thread")
            print(e)
    
    for x in threads:
        x.start()
    
    # Wait for all of them to finish
    for x in threads:
        x.join()
    
    print("\n\n--------- You Win ----------" )

 #   for key, value in MPLS_Devices.items():
 #       print("Trying----->" + key + " IP:" + value['IP'] )
 #       print(SendToDevice(key, value, config_dir))
 #       print("Done----->" + key + "\n\n")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', help='input directory with the configuration scripts')
    args = parser.parse_args()
    load_conf_2_all(args.source_dir)


if __name__ == '__main__':
    main()
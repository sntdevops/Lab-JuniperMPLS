import argparse
import napalm
import os
from threading import Thread
from pprint import pprint


def SendToDevice(DeviceName, DeviceConnInfo, config_dir):

    driver = napalm.get_network_driver('ios')
    device = driver(hostname = DeviceConnInfo['IP'], username = DeviceConnInfo['username'], password = DeviceConnInfo['password'], optional_args={'inline_transfer': 'True'}) 
    #device.close()
    device.open()

    if device.is_alive():
        Interfaces=device.get_interfaces()

    if device.is_alive():
        device.load_replace_candidate(filename = config_dir + DeviceName + '.ios')
        #device.load_merge_candidate(filename = config_dir + "CPE-Common.ios")
     
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

    Devices ={'CPE-PW-01':{'IP':'172.16.209.110','username':'automation', 'password':'auto1234'},
                'CPE-VPLS-01':{'IP':'172.16.209.111','username':'automation', 'password':'auto1234'},
                'CPE-VPLS-02':{'IP':'172.16.209.112','username':'automation', 'password':'auto1234'},
                'CPE-PW-02':{'IP':'172.16.209.113','username':'automation', 'password':'auto1234'},
                'CPE-VPLS-03':{'IP':'172.16.209.114','username':'automation', 'password':'auto1234'},
                'CPE-VPLS-04':{'IP':'172.16.209.115','username':'automation', 'password':'auto1234'},
                'CPE-L3VPN-01':{'IP':'172.16.209.116','username':'automation', 'password':'auto1234'},
                'CPE-L3VPN-02':{'IP':'172.16.209.117','username':'automation', 'password':'auto1234'},
                'CPE-L3VPN-03':{'IP':'172.16.209.118','username':'automation', 'password':'auto1234'},
                'CPE-L3VPN-04':{'IP':'172.16.209.119','username':'automation', 'password':'auto1234'}
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

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', help='input directory with the configuration scripts')
    args = parser.parse_args()
    load_conf_2_all(args.source_dir)


if __name__ == '__main__':
    main()
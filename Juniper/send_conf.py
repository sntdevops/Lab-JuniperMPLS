import napalm
import os
#import jinja2

from pprint import pprint as pp

config_dir = os.path.join(os.path.dirname(__file__),'conf')

driver = napalm.get_network_driver('junos')
device = driver(hostname='172.16.209.101', username='automation', password='auto1234', optional_args={'port': 830})
#device.close()
device.open()

print(device.username)

if device.is_alive():
    device.load_replace_candidate(filename=config_dir+'/juniper/RT-EDGE.01.conf')

diffs = device.compare_config()
print len(diffs)
if len(diffs) > 1:
    print(diffs)
    device.commit_config()
else:
    print('No changes needed')
    device.discard_config()

device.close()

#device.discard_config()
import napalm
import os
import jinja2

config_dir = os.path.join(os.path.dirname(__file__),'conf')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(config_dir),autoescape=True)
 
from pprint import pprint

driver = napalm.get_network_driver('junos')
device = driver(hostname='172.16.209.101', username='automation', password='auto1234', optional_args={'port': 830})
#device.close()
device.open()

print(device.username)

if device.is_alive():
    #pprint(device.get_facts())
    Lst_interface=device.get_interfaces()
    print(Lst_interface)

#for
pprint(Lst_interface.get('ge-0/0/0'))

mapping_interfaces = {'em2': 'ge-0/0/0','em3': 'ge-0/0/1','em4': 'ge-0/0/2','em5': 'ge-0/0/3','em6': 'ge-0/0/4','em7': 'ge-0/0/5',}
test_lst = {id:0,mac:'50:00:00:07:00:02',id:1,mac:'50:00:00:07:00:03'}

template = jinja_env.get_template('/juniper/update_macs.jinja2')
print(template)
pprint(template.render(macs=test_lst))

for idx, val in enumerate(ints):
    print(idx, val)

Lst_interface.get('em2','notfound')['mac_address']
Lst_interface.get('em3','notfound')['mac_address']
Lst_interface.get('em4','notfound')['mac_address']
Lst_interface.get('em5','notfound')['mac_address']
Lst_interface.get('em6','notfound')['mac_address']
Lst_interface.get('em7','notfound')['mac_address']
Lst_interface.get('em8','notfound')['mac_address']

device.close()
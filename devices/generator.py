from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import os


def generator(model,  hostname, mgmt_vlan, ip, mask, gw, snmp_location):
    """
    Detects device model and call right function to generate config. And return complete config as string.
    Assumes that IP addresses and VLAN numbers are correct

    :param model: str, device model from request
    :param hostname: str, hostname from request
    :param mgmt_vlan: str, MGMT Vlan number from request
    :param ip: str, MGMT IP from request
    :param mask: str, MGMT Mask from request
    :param gw: str, MGMT gateway from request
    :param snmp_location: str, SNMP location from request
    :return: str, FULL config
    """
    config = ""
    if model == 'hp1910-8':
        config = generate_hp1910('8', hostname, mgmt_vlan, ip, mask, gw, snmp_location)
    if config:
        return config
    else:
        return "Error: Config for {} was not generated.".format(model)


def generate_hp1910(ports, hostname, mgmt_vlan, ip, mask, gw, snmp_location):
    ACCESS_PORTS = ('Ethernet1/0/' + str(i+1) for i in range(8))
    UPLINK_PORTS = ('GigabitEthernet1/0/' + str(i) for i in range(9, 11))
    env = Environment()
    env.loader = FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/config_templates')
    template = env.get_template('hp1910_details.j2')
    # with open('config_templates/hp1910_details.j2', 'r') as file:
    #     temp = file.read()
    # template = Template(temp)
    variables = {
        'hostname': hostname,
        'ports': ports,
        'mgmt_vlan': mgmt_vlan,
        'ip': ip,
        'mask': mask,
        'gw': gw,
        'snmp_location': snmp_location,
        'ACCESS_PORTS': ACCESS_PORTS
    }
    return template.render(variables)


# print(generate_hp1910('8', 'testhostname', '24', '1.1.1.1', '2.2.2.2', '3.3.3.3', 'test snmp loc'))

# print(generator('hp1910', '8', 'testhostname', '24', '1.1.1.1', '2.2.2.2', '3.3.3.3', 'test snmp loc'))
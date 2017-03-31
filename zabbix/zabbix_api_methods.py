import sys
from pyzabbix.api import ZabbixAPI
from secrets.secrets import *

# Connect to ZabbixAPI
try:
    zapi = ZabbixAPI(url=ZABBIX_URL, user=ZABBIX_USERNAME, password=ZABBIX_PASSWORD)
except Exception as e:
    print("Failed to connect to Zabbix: " + str(e))
    sys.exit(0)


def zabbix_find_group(group_name):
    """
    Find Group ID by Group name.

    :param group_name:
    :return: group ID or 0 if group does not exist
    """
    group_filter = {
        'filter': {
            'name': group_name
        }
    }
    try:
        search_result = zapi.do_request('hostgroup.get', group_filter)  # Send request to Zabbix
    except Exception as error:
        print('Error while searching group:' + str(error))
        return 0
    # Check if group exists
    if search_result['result']:
        return search_result['result'][0]['groupid']
    else:
        return 0


def zabbix_list_groups():
    """
    List all Zabbix Group names.
    :return: list of tuples (GroupID, GroupName) or 0 if error
    """
    result = []
    try:
        search_result = zapi.do_request('hostgroup.get')  # Send request to Zabbix
    except Exception as error:
        print('Error while searching group:' + str(error))
        return 0
    for group in search_result['result']:
        result.append((group['groupid'], group['name']))
    return result


def zabbix_find_template(template_name):
    """
    Find Template ID by Template name.

    :param template_name: Must be exactly as in Zabbix
    :return: template ID or 0 if template does not exist
    """
    template_filter = {
        'filter': {
            'name': template_name
        }
    }
    try:
        search_result = zapi.do_request('template.get', template_filter)  # Send request to Zabbix
    except Exception as error:
        print('Error while search template: ' + str(error))
        return 0
    # Check if template exists
    if search_result['result']:
        return search_result['result'][0]['templateid']
    else:
        return 0


def map_template_names(raw_name):
    """
    Map convinient template name with Zabbix template names. For often used templates only.
    :param raw_name: name from input
    :return: name from Zabbix or False if name is not in list
    """
    template_names_map = {
        'juniper': 'JuniperT SNMP Device',
        'cisco': 'Cisco SNMP Device___T',
        'dlink': 'DLink SNMP Device macro',
        'mikrotik': 'Mikrotik SNMP Device T',
        'qtech': 'QTECH SNMP Device',
        'cisco asa': 'Cisco ASA',
        'moxa': 'Moxa SNMP Device',
        'hp5800': 'HP 58xx SNMP Device',
        'hp5500': 'HP 5500 SNMP Device',
        'hp5120': 'HP 5120 SNMP Device',
        'hp1950': 'HP 1950 SNMP Device',
        'hp1920': 'HP 1920 SNMP Device',
        'ping loss': 'Ping_Loss'
    }
    if str(raw_name).lower().strip() in template_names_map.keys():
        return template_names_map[str(raw_name).lower().strip()]
    else:
        print("Name is not in list, use(" + ", ".join(template_names_map.keys()) + ")")
        return False


def zabbix_add_host(hostname, ip_address, groups_list, template_name, snmp_community=DEFAULT_SNMP_COMMUNITY, status=ENABLED):
    """
    Add host to zabbix. do_request method in ZabbixAPI use 2 arguments:
        method - see full list on https://www.zabbix.com/documentation/3.2/manual/api
        parameters - parameters of host

    :param hostname: str, hostname of host
    :param ip_address: str, ip address of host
    :param groups_list: list of tuples (GroupID, GroupName) from zabbix where host belongs to
    :param template_name: name of template for host
    :param snmp_community: str, SNMP community string, if not specified it is DEFAULT_SNMP_COMMUNITY
    :param status: int, 0 - enabled, 1 - disabled
    :return: True if host added, Error message if not
    """
    gr_list = []
    for group in groups_list:
        gr_list.append({'groupid': group[0]})

    if snmp_community == '':
        snmp_community = DEFAULT_SNMP_COMMUNITY

    if status:
        device_status = 0
    else:
        device_status = 1

    template_name_mapped = map_template_names(template_name)
    template_id = zabbix_find_template(template_name_mapped)

    if not groups_list or not template_id:
        print('Host does not added')
        return False
    print('Adding host...')
    parameters = {
        'host': hostname,
        'interfaces': [
            {
                'type': 2,  # 1 - Zabbix Agent, 2 - SNMP
                'main': 1,
                'useip': 1,
                'ip': ip_address,
                'dns': '',
                'port': '161'   # SNMP port
            }
        ],
        'groups': gr_list,
        'templates': [
            {
                'templateid': template_id
            }
        ],
        'macros': [
            {
                'macro': '{$SNMP_COMMUNITY}',
                'value': snmp_community
            }
        ],
        'status': device_status,
        }
    try:
        zapi.do_request('host.create', parameters)
    except Exception as error:
        print('Can not add host: ' + str(error))
        return str(error)
    print('Done')
    return True

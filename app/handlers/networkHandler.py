import netifaces

from OuiLookup import OuiLookup


# Все это действо - обертка над библиотекой Netifaces
# А OuiLookup для информации о производителе по MAC
def get_interfaces():
	return netifaces.interfaces()


def get_gateways():
	return netifaces.gateways()


def get_default_gateway():
	try:
		return netifaces.gateways()["default"][netifaces.AF_INET]

	except KeyError:
		return False


def get_interface_mac(interface):
	try:
		return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]

	except ValueError:
		return False

	except KeyError:
		return False


def get_interface_ipv4(interface):
	try:
		return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["addr"]

	except ValueError:
		return False

	except KeyError:
		return False


def mac_lookup(mac):
	address = mac.upper().replace(':', '')
	result = OuiLookup().query(address)[0]
	
	if result[address]:
		return result[address].title()

	else:
		return "Not Found"

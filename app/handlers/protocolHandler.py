import re
import socket
import binascii


# ARP-файлик
ARP_FILE = "/proc/net/arp"
"""
Далее все очень сложно, но быстро.
"""


class ProtocolType:
	IPV4 = socket.htons(0x0800)


class ProtocolPacket:
	ARP = b'\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01'  # Байты протокола ARP, https://ru.wikipedia.org/wiki/ARP


class ARP:
	def __packet_generate(sender_mac, target_mac, sender_ip, target_ip, destination_mac = None):  # Генерация ETH-ARP пакета
		sha = ARP.__encode_mac(sender_mac)
		tha = ARP.__encode_mac(target_mac)

		spa = socket.inet_aton(sender_ip)
		tpa = socket.inet_aton(target_ip)

		if destination_mac: destination = ARP.__encode_mac(destination_mac)
		else: destination = tha

		return destination + sha + ProtocolPacket.ARP + sha + spa + tha + tpa

	def __encode_mac(address):  # Кодирование MAC-адреса
		return binascii.unhexlify(address.strip().replace(':', ''))

	def send(sender_mac, target_mac, sender_ip, target_ip, destination_mac = None):
		connect = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, ProtocolType.IPV4)
		connect.bind((interface, ProtocolType.IPV4))

		packet = ARP.__packet_generate(sender_mac, target_mac, sender_ip, target_ip, destination_mac)
		connect.send(packet)

	def table(ssh_connect = None):  # Получение таблицы двумя способами
		result = []
		arp_result = None

		try:
			if ssh_connect is None:
				with open(ARP_FILE) as arp:
					arp_result = arp.read()

			else:
				arp_result = ssh_connect.execute("arp -an")

			for line in arp_result.split('\n'):
				ip = re.search(r'\d+\.\d+\.\d+\.\d+', line)
				mac = re.search(r'(?:[0-9a-fA-F]:?){12}', line)

				if ip and mac and mac.group(0) != "00:00:00:00:00:00":
					result.append((ip.group(0), mac.group(0)))

		except Exception as e:
			print(e, '\nError, system exit!')
			raise SystemExit

		return result

import asyncio

from socket import getservbyport


TIMEOUT = 0.6
PORTS = [*range(1,1025),*range(25500,25600),
		*range(19100,19200),*range(5900, 6000),
		1117,1119,1900,1600,1700,1801,1433,5432,5433,5434,
		2020,2021,2022,2120,2121,2222,8080,8443,1984,1521,
		2100,2200,2500,2525,3000,3001,3002,3003,3128,3129,
		3168,3071,3300,3322,3325,3333,3351,3367,3737,1830,
		4000,4001,4002,4003,4004,4005,4006,3826,3827,3828,
		5221,5222,5500,5555,5560,5631,5633,5959,5984,5985,
		6666,6969,7000,7001,7002,7627,7676,7741,7777,7778,
		7004,7007,7019,7025,7070,7100,7103,7106,7800,7911,
		8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,
		8020,8021,8022,8042,8045,8093,8099,8100,8180,8181,
		8200,8222,8300,8333,8383,8400,8500,8600,8800,8900,
		8888,8899,8994,9000,9001,9002,9003,9009,9010,9011,
		9040,9050,9071,9080,9081,9090,9091,9099,9111,9200,
		9500,9300,9400,10000,11719,30000,40000,50000,60000,
		1434,1435,7210,7574,8983,28015,29015,8098,6379,2869,
		7473,7474,9042,8529,8005,8006,8007,8008,8009,3528,
		3529,9443,4712,9990,9993,6443,2181,2888,3888,20002,
		1058,11111,22222,33333,44444,55555,20000,10243,5357]  # Основные порты для сканирования, ~1500


async def get_port(address, port):
	try:
		connect = asyncio.open_connection(address, port)  # Открываем соединение на порте для проверки доступности порта
		await asyncio.wait_for(connect, timeout=TIMEOUT)

		return port

	except asyncio.TimeoutError:
		return False

	except ConnectionRefusedError:
		return False

	except OSError:
		return False


async def get_open_ports(address, ports = PORTS):
	port_arrays = split(ports, 550)
	response = []

	for array in port_arrays:
		tasks = (get_port(address, port) for port in array)
		response += await asyncio.gather(*tasks, return_exceptions=True)

	opens = []
	for output in response:
		if output:
			opens.append((output, get_port_name(output), "TCP"))

	return opens


def get_port_name(port):  # Получением имени порта (например HTTP или SMTP)
	try:
		return getservbyport(port)

	except:
		return "Unknown"


def split(array, size):  # Еще немного говнокода для разделения всего блока портов на части, чтобы не упороться в порог открытых соединений машины
	arrays = []

	while len(array) > size:
		pice = array[:size]
		arrays.append(pice)
		array = array[size:]

	arrays.append(array)
	return arrays

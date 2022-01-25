from aiohttp import web

from os.path import join
from os.path import dirname
from os.path import abspath

from datetime import datetime, timedelta, timezone

from .handlers.templateHandler import TemplateHandler
from .handlers.protocolHandler import ARP
from .handlers.portScannerHandler import get_open_ports

from .handlers.networkHandler import get_default_gateway
from .handlers.networkHandler import get_interface_mac
from .handlers.networkHandler import get_interface_ipv4
from .handlers.networkHandler import mac_lookup

from .handlers.pingHandler import ping


BASE_DIR = dirname(dirname(abspath(__file__)))
TEMPLATES_DIR = join(BASE_DIR, "templates")
ASSETS_DIR = join(TEMPLATES_DIR, "static")

handle = TemplateHandler(TEMPLATES_DIR)
ssh = None
config = None


async def assets(request: web.Request):  # Определяем каталог ассетов
	return web.FileResponse(join(ASSETS_DIR, request.path[1:]))


@handle.template("index.html")  # Для основной страницы
async def index(request: web.Request): ...


@handle.template("client.html")  # Для страницы просмотра информации об утсройстве
async def client(request: web.Request): ...


async def api_client(request: web.Request):  # Функция-обработчик для страницы /client/ (client.html)
	if 'ipv4' in request.rel_url.query: 
		ipv4 = request.rel_url.query['ipv4']  # Получаем GET параметр ipv4
		table = ARP.table(ssh)

		gateway_ip, interface = get_default_gateway()  # Дефолтные данные о шлюзе из netifaces
		data = dict()  # Response Information of Client (IPv4)

		found = False
		if ipv4 == get_interface_ipv4(interface):  # IPv4 интерфейса
			data["mac"] = get_interface_mac(interface)  # Мак-адрес интерфейса
			found = True

		else:
			for client in table:
				if client[0] == ipv4:
					data["mac"] = client[1]

					found = True
					break

		if found:  # Заполняем словарь данными
			data["ipv4"] = ipv4
			data["lookup"] = mac_lookup(data["mac"])
			data["interface"] = interface
			data["ports"] = await get_open_ports(ipv4)

			return response(data)  # И отправляем

	return response()



async def api_check_network(request: web.Request):  # Для проверки наличия связи со шлюзом
	if get_default_gateway():
		return response(True)  # Возвращаем True, если дефолтный шлюз найден

	return response()


async def api_interval(request: web.Request):  # Для получения интервала сканирования из конфига
	data = config.get()  # data - наш словарь конфига
	return response(data["interval"])


async def api_clients(request: web.Request):  # Функция-обработчик для главной страницы
	clients = {}
	data = config.get()
	dt = get_current_time(data["timezone"]).strftime("%d %B, %I:%M%p")  # Форматируем полученную дату
	macs = []

	for index, device in enumerate(data["devices"]):  # enumerate возвращает индекс и элемент из списка в for
		mac = device["mac"]  # Далее снова заполняем данными
		macs.append(mac)

		clients[mac] = device
		clients[mac]["online"] = False
		if device["device"] == "":
			clients[mac]["device"] = mac_lookup(device["mac"])  # Определение компании-производителя устройства по MAC

		data["devices"][index]["last_check"] = dt
		clients[mac]["last_check"] = dt
		clients[mac]["ipv4"] = ""

	for subnet in data["subnets"]:  # Пингуем все подсети из конфига
		await ping(subnet, subnet=True)

	for client in ARP.table(ssh):  # И снова заполняем данными
		if client[1] in macs:
			dict_id = search_id(data["devices"], "mac", client[1])  # Даже тут без говнокода не обошлось

			clients[client[1]]["ipv4"] = client[0]
			clients[client[1]]["online"] = True
			clients[client[1]]["last_discovery"] = dt

			data["devices"][dict_id]["last_discovery"] = dt
			data["devices"][dict_id]["ipv4"] = client[0]

	config.set(data)  # Перезаписываем конфиг (именно из-за этого нельзя его редактировать при работе программы)
	return response(clients)  # Возвращаем список клиентов


def response(data = None):  # Обертка для ответов. Если данные переданы, то они отдаются пользователю, если нет, то пользователю отдаем False
	if data:
		return web.json_response({"data": data})

	else:
		return web.json_response({"data": False})


def search_id(dicts_list, field, value):  # Говнокод говорю же, для поиска ключа по значению в словаре
	the_id = None
	index = 0

	for i in dicts_list:
		if i[field] == value:
			the_id = index
			break

		index += 1

	return the_id


def get_current_time(hours):  # Получаем текущее время, учитывая часовой пояс из конфига
    delta = timedelta(hours=hours, minutes=0)
    return datetime.now(timezone.utc) + delta

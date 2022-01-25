import asyncio
import aioping


async def ping(host, subnet = False, timeout = 2):  # Обертка над библиотекой для ping (aioping)
	if subnet:
		mask = '.'.join(host.split('.')[:-1])
		tasks = [asyncio.create_task(ping(f"{mask}.{net}")) for net in range(1, 255)]  # Создаем таски на все адреса в подсети

		await asyncio.wait(tasks)

	else:
		try:
			r = await aioping.ping(host, timeout)  # Пингуем с заданным временем ожидания

		except:
			pass

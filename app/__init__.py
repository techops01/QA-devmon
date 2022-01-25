from . import views

from .handlers.configHandler import Config
from .handlers.sshHandler import SSH

from os.path import exists


def setup(app, args):
	# Arguments, их инициализация
	if args.config and exists(args.config): 
		views.config = Config(args.config)

		if args.ssh: 
			views.ssh = SSH(views.config.get()["ssh"])

	else: 
		print("[WARNING] Config file not specified!")
		raise SystemExit

	# Pages, все что ниже это связывание страниц и функций-обработчиков
	app.router.add_get("/", views.index)
	app.router.add_get("/client/{ipv4}", views.client)

	# Assets
	app.router.add_get("/assets/{path:.*}", views.assets)

	# Application Programming Interface
	app.router.add_get("/api/interval", views.api_interval)
	app.router.add_get("/api/client", views.api_client)
	app.router.add_get("/api/clients", views.api_clients)
	app.router.add_get("/api/check_network", views.api_check_network)

import re

from aiohttp import web
from os.path import join


"""
Все что ниже это собственный декоратор для вывода пользователю HTML-файла
Но к тому же обработка синтаксиса {% sidebar.html %} и подобного, чтобы импортировать внутрь этого файлы дополнительные файлы

Вообще для этого есть jinja2 и aiohttp_jinja2, но я не стал нести с собой такую махину и просто написал отдельную функцию
И единственную, которая пригодилась бы мне из jinja2
"""


class Pattern:  # Регулярные выражения (regexp; re)
	INCLUDE = r'\{%\s*(\w+\.\w+)\s*%\}'


class TemplateHandler:
	def __init__(self, templates_directory):
		self.templates_directory = templates_directory

	def template(self, filename):
		def function(handler):
			def wrapper(*args, **kwargs):
				result = open(join(self.templates_directory, filename)).read()

				# {% file.html %} - include files
				includes = re.findall(Pattern.INCLUDE, result)
				for i in includes:
					ifile = join(self.templates_directory, i)
					result = re.sub(get_pattern_file(i), open(ifile).read(), result)

				return web.Response(text=result, content_type='text/html')

			return wrapper

		return function


def get_pattern_file(name):
	return '\{%\s*' + name.replace('.', '\.') + '+\s*%\}'

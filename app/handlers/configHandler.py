import json


# А это действо для удобного считывания конфиг-файла
class Config:
    def __init__(self, config_file):
        self.file = config_file

    def get(self):
        try:
            with open(self.file) as file:
                return json.loads(file.read())  # Считываем и возвращаем конфиг в виде словаря

        except:
            print("[ERROR] Config file not readable, system exit!")
            raise SystemExit

    def set(self, content):
        try:
            with open(self.file, 'w') as file:  # Открываем файл для чтения
                file.write(json.dumps(content, indent=4))  # Перезаписываем конфиг-файл; indent=4 для красивых отступов

        except:
            print("[ERROR] Config file not writable, system exit!")
            raise SystemExit  # Вызываем исключение SystemExit для завершения программы (аналогично sys.exit())

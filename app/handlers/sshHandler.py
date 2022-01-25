import paramiko


class SSH:  # Обертка над Paramiko
	def __init__(self, data):
		self.hostname = data["host"]
		self.port = data["port"]
		self.username = data["user"]
		self.password = data["passwd"]

	def execute(self, command):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

		stdin, stdout, stderr = ssh.exec_command(command)

		out = stdout.read()
		err = stderr.read()

		result = out if out else err
		result = result.decode(encoding="utf-8")

		ssh.close()

		return result

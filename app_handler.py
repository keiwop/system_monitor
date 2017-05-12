
class AppHandler:
	def __init__(self, app):
		self.app = app
	
	def update_proc_network_info(self, pid, iface, rx, tx):
		#print(f"Handling: {pid} - {iface} - {rx} - {tx}")
		self.app.pmon.update_proc_network(pid, iface, rx, tx)

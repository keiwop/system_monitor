
class AppHandler:
	def __init__(self, app):
		self.app = app
	
	def update_proc_network_info(self, pid, iface, rx, tx):
		#print(f"Handling: {pid} - {iface} - {rx} - {tx}")
		p = self.app.pmon.get_proc(pid)
		p.net.set_tmp_data(iface, rx, tx)
		self.app.pmon.update_proc(p)

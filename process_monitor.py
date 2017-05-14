from system_info import SystemInfo
from formatting import Formatting
from process_info import Process
import psutil
import time


f = Formatting()



class ProcessMonitor:
	proc_dict = {}
	proc_list = []
	virtual_proc_list = []
	info = None
	
	def __init__(self, init_time=0.01):
		self.info = SystemInfo()
		for proc in psutil.process_iter():
			proc.cpu_percent(interval=0.0)
		time.sleep(init_time)
	
	
	def update(self):
		self.update_proc_dict()
		self.info.update()
	
	def update_proc(self, p):
		self.proc_dict[p.pid] = p
	
	def get_proc(self, pid):
		if pid in self.proc_dict and psutil.pid_exists(pid):
			return self.proc_dict[pid]
		else:
			return Process(pid)
	
	
	def update_proc_dict(self):
		self.info.reset()
		
		for pid in list(self.proc_dict):
			if not psutil.pid_exists(pid):
				self.proc_dict.pop(pid, None)
		
		for proc in psutil.process_iter():
			if proc.pid in self.proc_dict:
				p = self.proc_dict[proc.pid]
			else:
				p = Process(proc.pid)
			
			p.update(proc)
			self.info.add_proc_data(p)
			
			self.proc_dict[p.pid] = p
	
	
	def create_virtual_proc_dict(self):
		self.virtual_proc_dict = {}
		# Creating a virtual process allows to regroup all the processes sharing the same name
		for pid, p in self.proc_dict.items():
			if p.name not in self.virtual_proc_dict:
				self.virtual_proc_dict[p.name] = Process(is_virtual=True, name=p.name)
			self.virtual_proc_dict[p.name].add_proc_data(p)
	
	
	def get_proc_list(self, nb_proc=4, order_by="mem"):
		self.create_virtual_proc_dict()
		proc_list = self.virtual_proc_dict.values()
		sort_keys = {	"mem": lambda p: p.mem.used,
						"cpu": lambda p: p.cpu.used,
						"rx": lambda p: p.net.rx,
						"tx": lambda p: p.net.tx,
						"disk_read": lambda p: p.disk.read,
						"disk_write": lambda p: p.disk.write}
		if order_by in sort_keys:
			sort_key = sort_keys[order_by]
		return sorted(proc_list, key=sort_key, reverse=True)[:nb_proc]

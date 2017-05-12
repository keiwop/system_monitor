from formatting import Formatting
import psutil
import time

f = Formatting()

class Process:
	pid = None
	name = ""
	used_mem = 0
	used_cpu = 0
	rx = 0
	tx = 0
	iface = None
	is_virtual = False
	
	def __init__(self, pid=-1, is_virtual=False):
		self.pid = pid
		self.is_virtual = is_virtual
	
	def kill(self):
		if is_virtual:
			for proc in psutil.process_iter():
				if proc.name() == self.name:
					print(f"Killing process {proc.pid}: {self.name}")
					proc.kill()
		else:
			print(f"Killing process {self.pid}: {self.name}")
			proc = psutil.Process(self.pid)
			proc.kill()
			


class ProcessMonitor:
	proc_dict = {}
	proc_list = []
	total_mem = 0
	total_mem_used = 0
	total_cpu_used = 0
	total_rx = 0
	total_tx = 0
	cpu_count = 0
	#nb_proc = 0
	
	def __init__(self, init_time=0.01):
		self.total_mem = psutil.virtual_memory().total
		self.cpu_count = psutil.cpu_count()
		for proc in psutil.process_iter():
			proc.cpu_percent(interval=0.0)
		time.sleep(init_time)
	
	
	def get_total_mem(self):
		return self.total_mem
	
	def get_used_mem(self):
		return self.total_mem_used
	
	def get_free_mem(self):
		return self.total_mem - self.get_used_mem()
	
	def get_used_mem_perc(self):
		return (self.get_used_mem() / self.total_mem * 100)
	
	def get_free_mem_perc(self):
		return 100 - self.get_used_mem_perc()
	
	
	def get_used_cpu(self):
		return self.total_cpu_used
	
	def get_used_cpu_percent(self):
		if self.total_cpu_used <= 0:
			return psutil.cpu_percent()
		return self.total_cpu_used / self.cpu_count
	
	
	def get_str_mem(self):
		return f"{f.size(self.get_used_mem(), show_unit=False)} / {f.size(self.total_mem, unit='B')} ({self.get_used_mem_perc():.1f}% used)"
	
	def get_str_cpu(self):
		return f"{self.get_used_cpu():.1f} / {int(self.cpu_count * 100)}"
	
	def get_str_cpu_perc(self):
		return f"{self.get_used_cpu()/self.cpu_count:.1f}%"
	
	def get_str_net_rx(self):
		return f"{f.speed(self.total_rx)} ({f.speed(self.total_rx*8, unit='bps')})"
	
	def get_str_net_tx(self):
		return f"{f.speed(self.total_tx)} ({f.speed(self.total_tx*8, unit='bps')})"
	
	
	def get_proc_from_pid(self, pid):
		if psutil.pid_exists(pid):
			#print("PID EXISTS")
			proc = psutil.Process(pid)
			if proc.name() in self.proc_dict:
				for index, p in enumerate(self.proc_dict[proc.name()]):
					if p.pid == pid:
						return (p, index)
		return None
	
	
	def update_proc_mem(self, p, proc):
		p.used_mem = proc.memory_info().rss
	
	def update_proc_cpu(self, p, proc):
		p.used_cpu = proc.cpu_percent(interval=0.0)
	
	def update_proc_network(self, pid, iface, rx, tx):
		#p = Process(pid)
		proc_info = self.get_proc_from_pid(pid)
		if proc_info is not None:
			p, index = proc_info
			p.iface = iface
			p.rx = rx
			p.tx = tx
			self.proc_dict[p.name][index] = p
	
	
	def update_proc_dict(self):
		#self.proc_dict = {}
		self.total_mem_used = 0
		self.total_cpu_used = 0
		self.total_rx = 0
		self.total_tx = 0
		for proc in psutil.process_iter():
			# FIXME: Can be coded in a better way, because it's quite ugly at the moment
			proc_info = self.get_proc_from_pid(proc.pid)
			index = 0
			if proc_info is None:
				p = Process(proc.pid)
				p.name = str(proc.name())
			else:
				p, index = proc_info

			self.update_proc_mem(p, proc)
			self.update_proc_cpu(p, proc)
				
			self.total_mem_used += p.used_mem
			self.total_cpu_used += p.used_cpu
			self.total_rx += p.rx
			self.total_tx += p.tx
			
			if p.name not in self.proc_dict:
				self.proc_dict[p.name] = []
			if proc_info is None:
				self.proc_dict[p.name].append(p)
			else:
				self.proc_dict[p.name][index] = p
	
	
	def update_proc_list(self):
		self.update_proc_dict()
		self.proc_list = []
		# Creating a virtual process allows to regroup all the processes sharing the same name
		for name, p_list in self.proc_dict.items():
			virtual_proc = Process(is_virtual=True)
			virtual_proc.name = name
			virtual_proc.iface = p_list[0].iface
			for p in p_list:
				virtual_proc.used_mem += p.used_mem
				virtual_proc.used_cpu += p.used_cpu
				virtual_proc.rx += p.rx
				virtual_proc.tx += p.tx
			self.proc_list.append(virtual_proc)
	
	
	def get_proc_list(self, nb_proc=4, order_by="mem"):
		self.update_proc_list()
		proc_list = []
		if order_by == "mem":
			sort_key = lambda p: p.used_mem
		elif order_by == "cpu":
			sort_key = lambda p: p.used_cpu
		elif order_by == "rx":
			sort_key = lambda p: p.rx
		elif order_by == "tx":
			sort_key = lambda p: p.tx
			
		#for proc in sorted(self.proc_list, key=sort_key, reverse=True)[:nb_proc]:
			##proc.used_mem = f"{int(proc.used_mem / (1024*1024))}M"
			#proc.used_mem = f.size(proc.used_mem, unit="iec")
			#proc.used_cpu = f"{proc.used_cpu:.1f}%"
			#proc_list.append(proc)
		#return proc_list
		return sorted(self.proc_list, key=sort_key, reverse=True)[:nb_proc]

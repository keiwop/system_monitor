import psutil
import time



class Process:
	pid = None
	name = ""
	used_mem = 0
	used_cpu = 0
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
	#nb_proc = 0
	
	def __init__(self, init_time=0.01):
		self.total_mem = psutil.virtual_memory().total
		for proc in psutil.process_iter():
			proc.cpu_percent(interval=0.0)
		time.sleep(init_time)
	
	def get_used_mem(self):
		return self.total_mem_used
	
	def get_free_mem(self):
		return psutil.virtual_memory().total - self.get_used_mem()
	
	def get_used_mem_perc(self):
		return (self.get_used_mem() / self.total_mem * 100)
	
	def get_free_mem_perc(self):
		return 100 - self.get_used_mem_perc()
	
	def get_used_cpu(self):
		return self.total_cpu_used
	
	def get_used_cpu_percent(self):
		if self.total_cpu_used <= 0:
			return psutil.cpu_percent()
		return self.total_cpu_used / psutil.cpu_count()
	
	
	# TODO: recode this function to not use smem (memory_full_info()) if possible, because it's quite slow
	def update_proc_mem(self, p, proc):
		try:
			p.used_mem = proc.memory_full_info().pss
		except:
			# HACK: FIXME
			# Without root access, we can't get the pss memory info from some processes
			p.used_mem = proc.memory_info().rss
			if p.name in self.proc_dict and len(self.proc_dict[p.name]):
				p.used_mem -= proc.memory_info().shared
	
	def update_proc_cpu(self, p, proc):
		p.used_cpu = proc.cpu_percent(interval=0.0)
	
	
	def update_proc_dict(self):
		self.proc_dict = {}
		self.total_mem_used = 0
		self.total_cpu_used = 0
		for proc in psutil.process_iter():
			p = Process(proc.pid)
			#with p.oneshot():
			p.name = str(proc.name())
			self.update_proc_mem(p, proc)
			self.update_proc_cpu(p, proc)
				
			self.total_mem_used += p.used_mem
			self.total_cpu_used += p.used_cpu
			
			if p.name not in self.proc_dict:
				self.proc_dict[p.name] = []
			self.proc_dict[p.name].append(p)
	
	
	def update_proc_list(self):
		self.update_proc_dict()
		self.proc_list = []
		# Creating a virtual process allows to regroup all the processes sharing the same name
		for name, p_list in self.proc_dict.items():
			virtual_proc = Process(is_virtual=True)
			virtual_proc.name = name
			for p in p_list:
				virtual_proc.used_mem += p.used_mem
				virtual_proc.used_cpu += p.used_cpu
			self.proc_list.append(virtual_proc)
	
	
	def get_proc_list(self, nb_proc=4, order_by="mem"):
		self.update_proc_list()
		proc_list = []
		if order_by == "mem":
			sort_key = lambda p: p.used_mem
		elif order_by == "cpu":
			sort_key = lambda p: p.used_cpu
		for proc in sorted(self.proc_list, key=sort_key, reverse=True)[:nb_proc]:
			proc.used_mem = f"{int(proc.used_mem / (1024*1024))}M"
			proc.used_cpu = f"{proc.used_cpu:.1f}%"
			proc_list.append(proc)
		return proc_list

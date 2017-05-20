from formatting import Formatting
import psutil


f = Formatting()



class MemInfo:
	def __init__(self):
		self.total = psutil.virtual_memory().total
		self.used = 0
		self.used_perc = 0
		self.free = 0
		self.free_perc = 0
	
	def update(self, proc=None):
		if proc is not None:
			self.used = proc.memory_info().rss
		self.used_perc = ((self.used / self.total) * 100)
		self.free = self.total - self.used
		self.free_perc = 100 - self.used_perc
	
	def reset(self):
		self.used = 0
		self.update()



class CpuInfo:
	count = 0
	used = 0
	used_perc = 0
	
	def __init__(self):
		self.count = psutil.cpu_count()
	
	def update(self, proc=None):
		if proc is not None:
			self.used = proc.cpu_percent(interval=0.0)
		self.used_perc = self.used / self.count
	
	def reset(self):
		self.used = 0
		self.update()



class DiskInfo:
	read = 0
	write = 0
	old_read = 0
	old_write = 0
	
	def update(self, proc=None):
		if proc is not None:
			# TODO: calculate the disk io each second instead of each update
			read = proc.io_counters().read_bytes
			write = proc.io_counters().write_bytes
			self.read = max(read - self.old_read, 0)
			self.write = max(write - self.old_write, 0)
			self.old_read = read
			self.old_write = write
	
	def reset(self):
		self.read = 0
		self.write = 0
		self.update()



class NetInfo:
	iface = ""
	rx = 0
	tx = 0
	tmp_rx = 0
	tmp_tx = 0
	
	def update(self, proc=None):
		if proc is not None:
			self.rx = self.tmp_rx
			self.tx = self.tmp_tx
	
	def set_tmp_data(self, iface, rx, tx):
		self.iface = iface
		self.tmp_rx = rx
		self.tmp_tx = tx
	
	def reset(self):
		self.rx = 0
		self.tx = 0
		self.update()



class Process:
	def __init__(self, pid=-1, name="", is_virtual=False):
		self.proc = None
		self.pid = pid
		self.name = name
		self.is_virtual = is_virtual
		self.mem = MemInfo()
		self.cpu = CpuInfo()
		self.disk = DiskInfo()
		self.net = NetInfo()	
	
	def update(self, proc=None):
		if proc is not None:
			self.proc = proc
			if self.name is None or self.name == "":
				self.name = self.proc.name()
		self.mem.update(proc)
		self.cpu.update(proc)
		self.disk.update(proc)
		self.net.update(proc)
	
	def reset(self):
		self.mem.reset()
		self.cpu.reset()
		self.disk.reset()
		self.net.reset()
	
	def add_proc_data(self, p):
		self.mem.used += p.mem.used
		self.cpu.used += p.cpu.used
		self.disk.read += p.disk.read
		self.disk.write += p.disk.write
		self.net.rx += p.net.rx
		self.net.tx += p.net.tx
		self.update()
	
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
	

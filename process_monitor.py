from formatting import Formatting
import psutil
import time

f = Formatting()

class Process:
	pid = -1
	proc = None
	name = ""
	used_mem = 0
	used_cpu = 0
	rx = 0
	tx = 0
	iface = ""
	old_disk_read = 0
	old_disk_write = 0
	disk_read = 0
	disk_write = 0
	is_virtual = False
	
	def __init__(self, pid=-1, is_virtual=False):
		self.pid = pid
		self.is_virtual = is_virtual
	
	def update(self, proc):
		self.proc = proc
		self.update_mem()
		self.update_cpu()
		self.update_disk()
	
	def update_mem(self):
		self.used_mem = self.proc.memory_info().rss
	
	def update_cpu(self):
		self.used_cpu = self.proc.cpu_percent(interval=0.0)
	
	def update_disk(self):
		# TODO: calculate the disk io each second instead of each update
		read = self.proc.io_counters().read_bytes
		write = self.proc.io_counters().write_bytes
		self.disk_read = max(read - self.old_disk_read, 0)
		self.disk_write = max(write - self.old_disk_write, 0)
		self.old_disk_read = read
		self.old_disk_write = write
	
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

			
class MemInfo:
	total = 0
	used = 0
	used_perc = 0
	free = 0
	free_perc = 0
	
	def __init__(self):
		self.total = psutil.virtual_memory().total
	
	def update(self):
		self.used_perc = ((self.used / self.total) * 100)
		self.free = self.total - self.used
		self.free_perc = 100 - self.used_perc
	
	def reset(self):
		self.used = 0


class DiskInfo:
	read = 0
	write = 0
	
	def update(self):
		pass
	
	def reset(self):
		self.read = 0
		self.write = 0


class CpuInfo:
	count = 0
	used = 0
	used_perc = 0
	
	def __init__(self):
		self.count = psutil.cpu_count()
	
	def update(self):
		self.used_perc = self.used / self.count
	
	def reset(self):
		self.used = 0


class NetInfo:
	iface = ""
	rx = 0
	tx = 0
	
	def update(self):
		pass
	
	def reset(self):
		self.rx = 0
		self.tx = 0


class SystemInfo:
	mem = MemInfo()
	cpu = CpuInfo()
	disk = DiskInfo()
	net = NetInfo()
	
	def update(self):
		self.mem.update()
		self.cpu.update()
		self.disk.update()
		self.net.update()
	
	def update_proc_data(self, p):
		self.mem.used += p.used_mem
		self.cpu.used += p.used_cpu
		self.disk.read += p.disk_read
		self.disk.write += p.disk_write
		self.net.rx += p.rx
		self.net.tx += p.tx
	
	def reset(self):
		self.mem.reset()
		self.cpu.reset()
		self.disk.reset()
		self.net.reset()
	
	def str_mem(self):
		return f"{f.size(self.mem.used, show_unit=False)} / {f.size(self.mem.total, unit='B')} ({self.mem.used_perc:.1f}% used)"
	
	def str_cpu(self):
		return f"{self.cpu.used:.1f} / {int(self.cpu.count * 100)}"
	
	def str_cpu_perc(self):
		return f"{self.cpu.used/self.cpu.count:.1f}%"
	
	def str_net_rx(self):
		return f"{f.speed(self.net.rx)} ({f.speed(self.net.rx*8, unit='bps')})"
	
	def str_net_tx(self):
		return f"{f.speed(self.net.tx)} ({f.speed(self.net.tx*8, unit='bps')})"
	
	def str_disk_read(self):
		return f"{f.speed(self.disk.read)}"
	
	def str_disk_write(self):
		return f"{f.speed(self.disk.write)}"


class ProcessMonitor:
	proc_dict = {}
	proc_list = []
	info = None
	
	def __init__(self, init_time=0.01):
		self.info = SystemInfo()
		for proc in psutil.process_iter():
			proc.cpu_percent(interval=0.0)
		time.sleep(init_time)

	
	def get_proc_from_pid(self, pid):
		if psutil.pid_exists(pid):
			proc = psutil.Process(pid)
			if proc.name() in self.proc_dict:
				for index, p in enumerate(self.proc_dict[proc.name()]):
					if p.pid == pid:
						return (p, index)
		return None
	
	
	def update(self):
		self.update_proc_dict()
		self.update_proc_list()
		self.info.update()

	def update_proc_network(self, pid, iface, rx, tx):
		proc_info = self.get_proc_from_pid(pid)
		if proc_info is not None:
			p, index = proc_info
			p.iface = iface
			p.rx = rx
			p.tx = tx
			self.proc_dict[p.name][index] = p

	
	def update_proc_dict(self):
		self.info.reset()
		
		for proc in psutil.process_iter():
			# FIXME: Can be coded in a better way, because it's quite ugly at the moment
			proc_info = self.get_proc_from_pid(proc.pid)
			index = 0
			if proc_info is None:
				p = Process(proc.pid)
				p.name = str(proc.name())
			else:
				p, index = proc_info

			p.update(proc)
			self.info.update_proc_data(p)
			
			if p.name not in self.proc_dict:
				self.proc_dict[p.name] = []
			if proc_info is None:
				self.proc_dict[p.name].append(p)
			else:
				self.proc_dict[p.name][index] = p
	
	
	def update_proc_list(self):
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
				virtual_proc.disk_read += p.disk_read
				virtual_proc.disk_write += p.disk_write
			self.proc_list.append(virtual_proc)
	
	
	def get_proc_list(self, nb_proc=4, order_by="mem"):
		proc_list = []
		sort_keys = {	"mem": lambda p: p.used_mem,
						"cpu": lambda p: p.used_cpu,
						"rx": lambda p: p.rx,
						"tx": lambda p: p.tx,
						"disk_read": lambda p: p.disk_read,
						"disk_write": lambda p: p.disk_write}
		if order_by in sort_keys:
			sort_key = sort_keys[order_by]
		return sorted(self.proc_list, key=sort_key, reverse=True)[:nb_proc]

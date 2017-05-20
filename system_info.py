from process_info import MemInfo, CpuInfo, DiskInfo, NetInfo
from formatting import Formatting
import os

f = Formatting()


class OSInfo:
	def __init__(self):
		self.name = os.uname().sysname
		self.hostname = os.uname().nodename
		self.kver = os.uname().release
		self.arch = os.uname().machine
		self.load = os.getloadavg()
	
	def update(self):
		self.load = os.getloadavg()

class SystemInfo:
	def __init__(self):
		self.os = OSInfo()
		self.mem = MemInfo()
		self.cpu = CpuInfo()
		self.disk = DiskInfo()
		self.net = NetInfo()
	
	def update(self):
		self.os.update()
		self.mem.update()
		self.cpu.update()
		self.disk.update()
		self.net.update()
	
	def add_proc_data(self, p):
		self.mem.used += p.mem.used
		self.cpu.used += p.cpu.used
		self.disk.read += p.disk.read
		self.disk.write += p.disk.write
		self.net.rx += p.net.rx
		self.net.tx += p.net.tx
	
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
	

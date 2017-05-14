from formatting import Formatting
import config
import time
import os


f = Formatting()



class TextUI:
	def __init__(self, sysmon):
		self.sysmon = sysmon
		self.continue_loop = False
	
	def start(self):
		self.continue_loop = True
		while self.continue_loop:
			time_before = time.time()
			self.update()
			time.sleep(max(1.0 - (time.time() - time_before), 0))
	
	def stop(self):
		self.continue_loop = False
	
	def update(self):
		self.sysmon.update()
		pmon = self.sysmon.pmon
		
		if config.fast_clear:
			print("\033\143")
		else:
			os.system("clear")
		
		for p in pmon.get_proc_list(nb_proc=8, sort=config.sort_proc):
			print(f"{f.size(p.mem.used):10} - {p.cpu.used:6.1f}% - {f.speed(p.net.rx):>12} (rx) - {f.speed(p.net.tx):>12} (tx) - {f.speed(p.disk.read):>12}(dr) - {f.speed(p.disk.write):>12}(dw) -> {p.name}")
		
		print("")
		print(f"{'Memory usage: ':>16}{pmon.info.str_mem()}")
		print(f"{'CPU usage: ':>16}{pmon.info.str_cpu()}")
		print(f"{'CPU usage: ':>16}{pmon.info.str_cpu_perc()}")
		print(f"{'Network rx: ':>16}{pmon.info.str_net_rx()}")
		print(f"{'Network tx: ':>16}{pmon.info.str_net_tx()}")
		print(f"{'Disk read: ':>16}{pmon.info.str_disk_read()}")
		print(f"{'Disk write: ':>16}{pmon.info.str_disk_write()}")
		

class CursesUI:
	def __init__(self, sysmon):
		self.sysmon = symon
		self.continue_loop = False
	
	def start(self):
		self.continue_loop = True
		while self.continue_loop:
			time_before = time.time()
			self.update()
			time.sleep(max(1.0 - (time.time() - time_before), 0))
	
	def stop(self):
		self.continue_loop = False
	
	def update(self):
		self.sysmon.update()
		pmon = self.sysmon.pmon
		pass

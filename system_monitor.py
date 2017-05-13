#! /usr/bin/env python3

from process_monitor import ProcessMonitor
from wrapper_nethogs import NethogsMonitor
from app_handler import AppHandler
from formatting import Formatting
import signal
import psutil
import time
import sys
import os

f = Formatting()

class SystemMonitor:
	handler = None
	pmon = None
	nhmon = None
	continue_loop = True
	
	def __init__(self):
		self.handler = AppHandler(self)
		self.pmon = ProcessMonitor()
		self.nhmon = NethogsMonitor(self.handler)
		
	def main_loop(self):
		while self.continue_loop:
			self.print_info()
			time.sleep(1)
	
	def stop(self):
		self.nhmon.stop()
	
	def print_info(self):
		os.system("clear")
		print("")
		self.pmon.update()
		for p in self.pmon.get_proc_list(nb_proc=8, order_by="disk_write"):
			print(f"{f.size(p.used_mem):10} - {p.used_cpu:6.1f}% - {f.speed(p.rx):>12} (rx) - {f.speed(p.tx):>12} (tx) - {f.speed(p.disk_read):>12}(dr) - {f.speed(p.disk_write):>12}(dw) -> {p.name}")
		
		print("")
		print(f"Memory usage: {self.pmon.info.str_mem()}")
		print(f"CPU usage: {self.pmon.info.str_cpu()}")
		print(f"CPU usage: {self.pmon.info.str_cpu_perc()}")
		print(f"Network rx: {self.pmon.info.str_net_rx()}")
		print(f"Network tx: {self.pmon.info.str_net_tx()}")
		print(f"Disk read: {self.pmon.info.str_disk_read()}")
		print(f"Disk write: {self.pmon.info.str_disk_write()}")
	

def signal_handler(signal, *args):
	print(f"Signal {signal} received, exiting")
	sysmon.stop()
	sys.exit()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	
	sysmon = SystemMonitor()
	sysmon.main_loop()

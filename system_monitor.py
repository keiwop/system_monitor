#! /usr/bin/env python3

from process_monitor import ProcessMonitor
from formatting import Formatting
import psutil
import time


class NetworkMonitor:
	iface_dict = {}
	
	def __init__(self):
		pass
	
	


if __name__ == "__main__":
	pmon = ProcessMonitor()
	f = Formatting()
	#print()
	
	continue_loop = True
	
	while continue_loop:
		print("")
		for p in pmon.get_proc_list(nb_proc=8, order_by="mem"):
			print(f"{p.used_mem:6} - {p.used_cpu:6} -> {p.name}")
		
		print(f"{pmon.get_used_mem()}");
		print("===")
		print(f.size(pmon.get_used_mem(), unit="iec"))
		print("====")
		print(pmon.get_used_mem_perc());
		print(pmon.get_free_mem_perc());
		print(pmon.get_used_cpu());
		print(pmon.get_used_cpu_percent());
		print(psutil.cpu_percent());
		
		time.sleep(1)

	#for proc in psutil.process_iter():
		#if "chrome" in proc.name():
			##print(dir(proc))
			#print(proc.io_counters())
		#if "Xorg" in proc.name():
			#print(f"{proc.pid} -> {proc.cpu_percent(interval=0.0)}")
		

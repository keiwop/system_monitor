from formatting import Formatting
from color import Color, printc
import config
import shutil
import time
import os


f = Formatting()
c = Color()


class TextUI:
	def __init__(self, sysmon):
		self.sysmon = sysmon
		self.continue_loop = False
		self.term_size = (0, 0)
	
	def start(self):
		self.continue_loop = True
		while self.continue_loop:
			time_before = time.time()
			self.update()
			time.sleep(max(config.refresh_time - (time.time() - time_before), 0))
	
	def stop(self):
		self.continue_loop = False
	
	def update(self):
		self.sysmon.update()
		pmon = self.sysmon.pmon
		self.term_size = shutil.get_terminal_size((80, 20))
		
		if config.fast_clear:
			print("\033\143", end="")
		else:
			os.system("clear")
		
		self.print_sys_info(pmon)
		self.print_proc_info(pmon)
		#print("")
		#print(f"{'Memory usage':^16}{pmon.info.str_mem()}")
		#print(f"{'CPU usage':^16}{pmon.info.str_cpu()}")
		#print(f"{'CPU usage':^16}{pmon.info.str_cpu_perc()}")
		#print(f"{'Network rx':^16}{pmon.info.str_net_rx()}")
		#print(f"{'Network tx':^16}{pmon.info.str_net_tx()}")
		#print(f"{'Disk read':^16}{pmon.info.str_disk_read()}")
		#print(f"{'Disk write':^16}{pmon.info.str_disk_write()}")
	
	def print_proc_info(self, pmon):
		proc_list = pmon.get_proc_list(nb_proc=config.nb_proc, sort=config.sort_proc)
		self.print_array(config.proc_info_dict, proc_list)
	
	def print_sys_info(self, pmon):
		self.print_array(config.sys_info_dict, [pmon.info])
	
	def print_array(self, array_dict, array_data):
		self.print_line(array_dict, header=True, color=array_dict["header_color"](c))
		for i, line_data in enumerate(array_data):
			if i % 2 and config.altern_color_odd_line:
				color = array_dict["data_odd_color"](c)
			else:
				color = array_dict["data_color"](c)
			self.print_line(array_dict, line_data, color=color)
	
	def print_line(self, line_dict, line_data=None, header=False, color=Color.reset):
		line_str = ""
		for i, key in enumerate(line_dict["order"]):
			text_width = line_dict[key][0]
			if header:
				text = line_dict[key][1]
				align = config.align_header
			else:
				text = line_dict[key][2](f, line_data)
				align = config.align_data
			
			is_last = True if i == len(line_dict["order"]) - 1 else False
			text_size = self.get_text_size(line_str, text_width, is_last=is_last)
			text = self.truncate_text(text, text_size)
			line_str += f"{text:{align}{text_size}}" + config.column_delimiter
		
		#printc((255, 0, 255), line_str)
		printc(color, line_str)
	
	def get_text_size(self, line_str, perc, is_last=False):
		text_size = int((self.term_size.columns / 100) * perc)
		if config.fill_end_proc_info and is_last:
			text_size += max(self.term_size.columns - (len(line_str) + text_size + 1), 0)
		return text_size
	
	def truncate_text(self, text, max_size):
		if len(text) >= max_size:
			return f"{text[:max_size-2]}.."
		return text



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

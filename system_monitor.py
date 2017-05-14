#! /usr/bin/env python3

from process_monitor import ProcessMonitor
from wrapper_nethogs import NethogsMonitor
from text_ui import TextUI, CursesUI
from app_handler import AppHandler
from formatting import Formatting
import config
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
	ui = None
	continue_loop = True
	
	def __init__(self):
		self.handler = AppHandler(self)
		self.pmon = ProcessMonitor()
		self.nhmon = NethogsMonitor(self.handler)
		self.choose_ui()
	
	def choose_ui(self):
		if config.type_ui == "text":
			self.ui = TextUI(self)
		elif config.type_ui == "curses":
			self.ui = CursesUI(self)
			
	def main_loop(self):
		while self.continue_loop:
			self.ui.start()
	
	def stop(self):
		self.ui.stop()
		self.nhmon.stop()
		self.continue_loop = False
	
	def update(self):
		self.pmon.update()



def signal_handler(signal, *args):
	print(f"Signal {signal} received, exiting")
	sysmon.stop()
	sys.exit()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	
	sysmon = SystemMonitor()
	sysmon.main_loop()

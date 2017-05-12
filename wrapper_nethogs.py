import ctypes
import datetime
import threading

# This code is mainly the orignal from:
# https://github.com/raboof/nethogs/blob/master/contrib/python-wrapper.py
# The main things modified are the callback sending data back to another class and the main functions of this wrapper have been regrouped in a class


# This is a Python 3 demo of how to interact with the Nethogs library via Python. The Nethogs
# library operates via a callback. The callback implemented here just formats the data it receives
# and prints it to stdout. This must be run as root (`sudo python3 python-wrapper.py`).
# By Philip Semanchuk (psemanchuk@caktusgroup.com) November 2016
# Copyright waived; released into public domain as is.

# The code is multi-threaded to allow it to respond to SIGTERM and SIGINT (Ctrl+C).  In single-
# threaded mode, while waiting in the Nethogs monitor loop, this Python code won't receive Ctrl+C
# until network activity occurs and the callback is executed. By using 2 threads, we can have the
# main thread listen for SIGINT while the secondary thread is blocked in the monitor loop.


# LIBRARY_NAME has to be exact, although it doesn't need to include the full path.
# The version tagged as 0.8.5 (download link below) builds a library with this name.
# https://github.com/raboof/nethogs/archive/v0.8.5.tar.gz
LIBRARY_NAME = 'libnethogs.so.0.8.5'

# Here are some definitions from libnethogs.h
# https://github.com/raboof/nethogs/blob/master/src/libnethogs.h
# Possible actions are NETHOGS_APP_ACTION_SET & NETHOGS_APP_ACTION_REMOVE
# Action REMOVE is sent when nethogs decides a connection or a process has died. There are two
# timeouts defined, PROCESSTIMEOUT (150 seconds) and CONNTIMEOUT (50 seconds). AFAICT, the latter
# trumps the former so we see a REMOVE action after ~45-50 seconds of inactivity.
class Action():
    SET = 1
    REMOVE = 2
    MAP = {SET: 'SET', REMOVE: 'REMOVE'}

class LoopStatus():
    """Return codes from nethogsmonitor_loop()"""
    OK = 0
    FAILURE = 1
    NO_DEVICE = 2
    MAP = {OK: 'OK', FAILURE: 'FAILURE', NO_DEVICE: 'NO_DEVICE'}

# The sent/received KB/sec values are averaged over 5 seconds; see PERIOD in nethogs.h.
# https://github.com/raboof/nethogs/blob/master/src/nethogs.h#L43
# sent_bytes and recv_bytes are a running total
class NethogsMonitorRecord(ctypes.Structure):
    """ctypes version of the struct of the same name from libnethogs.h"""
    _fields_ = (('record_id', ctypes.c_int),
                ('name', ctypes.c_char_p),
                ('pid', ctypes.c_int),
                ('uid', ctypes.c_uint32),
                ('device_name', ctypes.c_char_p),
                ('sent_bytes', ctypes.c_uint32),
                ('recv_bytes', ctypes.c_uint32),
                ('sent_kbs', ctypes.c_float),
                ('recv_kbs', ctypes.c_float),
                )


class NethogsMonitor:
	def __init__(self, app_handler, lib=None):
		self.handler = app_handler
		self.lib = lib
		if lib is None:
			self.lib = ctypes.CDLL(LIBRARY_NAME)
		self.monitor_thread = threading.Thread(target=self.run_monitor_loop)
		self.monitor_thread.start()
	
	def stop(self):
		self.lib.nethogsmonitor_breakloop()
	
	def run_monitor_loop(self):
		CALLBACK_FUNC_TYPE = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(NethogsMonitorRecord))
		rc = self.lib.nethogsmonitor_loop(CALLBACK_FUNC_TYPE(self.network_activity_callback))
	
	def network_activity_callback(self, action, data):
		action_type = Action.MAP.get(action, 'Unknown')
		if "SET" in action_type:
			self.handler.update_proc_network_info(data.contents.pid, data.contents.device_name.decode("ascii"), int(data.contents.recv_kbs*1000), int(data.contents.sent_kbs*1000))
	

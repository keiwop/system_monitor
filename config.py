
# Can have the value "text", "curses", "graphical"
type_ui = "text"

fast_clear = True
refresh_time = 1.0

# "cpu", "mem", "rx", "tx", "disk_read", "disk_write"
sort_proc = "mem"
nb_proc = 8
fill_end_proc_info = True

# Show the base unit when the value reads 0
show_unit_for_zero = True

column_delimiter = "|"
align_header = "^"
align_data = ">"

altern_color_odd_line = True
enable_256_colors = True

fallback_colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

rgb_palette = {"black":(0,0,0), "red":(244,67,54), "green":(76,175,80), "yellow":(255,235,59), "blue":(33,150,243), "magenta":(156,39,176), "cyan":(0,188,212), "white":(255,255,255),
			   "grey":(158,158,158), "orange":(255,152,0), "brown":(121,85,72), "teal":(0,150,136), "indigo":(63,81,181), "pink":(233,30,99)}


shade_offset = 10

color_shades = {
				"": 0,
				"dark_": -1,
				"darker_": -2,
				"darkest_": -3,
				"light_": 1,
				"lighter_": 2,
				"lightest_": 3,
				}

proc_info_dict = {
	#"mem": 			[14, "MEMORY", lambda f, p: f"({f.perc(p.mem.used_perc)}) {f.size(p.mem.used)}"],
	"mem": 			[14, "MEMORY", lambda f, p: f.size(p.mem.used)],
	"cpu": 			[8, "CPU", lambda f, p: f.perc(p.cpu.used)],
	"rx": 			[14, "NET RX", lambda f, p: f.speed(p.net.rx)],
	"tx": 			[14, "NET TX", lambda f, p: f.speed(p.net.tx)],
	"disk_read": 	[14, "DISK READ", lambda f, p: f.speed(p.disk.read)],
	"disk_write": 	[14, "DISK WRITE", lambda f, p: f.speed(p.disk.write)],
	"name": 		[14, "PROGRAM", lambda f, p: p.name],
	"order": 		["mem", "cpu", "rx", "tx", "disk_read", "disk_write", "name"],
	#"color": 		lambda c: f"{c.white_bright}{c.blue_bg}",
	"header_color": lambda c: f"{c.white}{c.blue_bg}",
	"data_color": 	lambda c: f"{c.darkest_blue}{c.darker_white_bg}",
	"data_odd_color": lambda c: f"{c.light_blue}{c.darkest_white_bg}",
}


sys_info_dict = {
	"mem": 			[14, "MEMORY", lambda f, s: f.size(s.mem.used)],
	"cpu": 			[8, "CPU", lambda f, s: f.perc(s.cpu.used)],
	"rx": 			[14, "NET RX", lambda f, s: f.speed(s.net.rx)],
	"tx": 			[14, "NET TX", lambda f, s: f.speed(s.net.tx)],
	"disk_read": 	[14, "DISK READ", lambda f, s: f.speed(s.disk.read)],
	"disk_write": 	[14, "DISK WRITE", lambda f, s: f.speed(s.disk.write)],
	"load": 		[14, "LOAD", lambda f, s: str(s.os.load).replace("(","").replace(")","")],
	"order": 		["mem", "cpu", "rx", "tx", "disk_read", "disk_write", "load"],
	"header_color": lambda c: f"{c.white}{c.pink_bg}",
	"data_color": 	lambda c: f"{c.darkest_pink}{c.darker_white_bg}",
	"data_odd_color": lambda c: f"{c.light_pink}{c.darkest_white_bg}",
	#"data_color": 	lambda c: f"{c.rgb((255, 255, 255))}{c.rgb((0, 0, 255), bg=True)}",
}


	#"machine": 		[14, "MACHINE", lambda f, s: f"{s.os.hostname} - {s.os.kver}"],

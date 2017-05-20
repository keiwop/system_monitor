import config



class Color:
	# For each value in config.colors, a few attributes will be created using setattr.
	# It's then possible to get fo example the colors Color.red, Color.magenta_bg or Color.white_bright
	# If config.enable_256_colors is True, the colors are selected from config.rgb_palette. Else, it's just the standard 16 colors which are used
	base_fg = 30
	base_bg = 40
	reset = "\033[0m"
	
	def __init__(self):
		if config.enable_256_colors:
			for color, rgb_value in config.rgb_palette.items():
				for shade, offset in config.color_shades.items():
					setattr(self, f"{shade}{color}", self.rgb(rgb_value, offset=offset))
					setattr(self, f"{shade}{color}_bg", self.rgb(rgb_value, offset=offset, bg=True))
		else:
			for i, color in enumerate(config.fallback_colors):
				setattr(self, color, f"\033[{self.base_fg + i}m")
				setattr(self, f"{color}_bg", f"\033[{self.base_bg + i}m")
				setattr(self, f"{color}_bright", f"\033[{self.base_fg + i};1m")
	
	@staticmethod
	def rgb(color, bg=False, offset=0):
		color = tuple(min(max(c + (config.shade_offset*offset), 0), 255) for c in color)
		if bg:
			return f"\033[48;2;{color[0]};{color[1]};{color[2]}m"
		else:
			return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def printc(color, *args, bg=False):
	#print("COLOR:", repr(color))
	if type(color) is str:
		print(color, end="")
	elif type(color) is tuple and config.enable_256_colors:
		print(Color.rgb(color, bg=bg), end="")
	print(*args)
	print(Color.reset, end="")
